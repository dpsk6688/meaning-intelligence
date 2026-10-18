#!/usr/bin/env python3
"""publish.py —— 无需 git 的 GitHub 发布器（纯标准库）

为什么需要它：很多机器上根本没有 git（本项目的开发机就是如此），
但只要 Python 能建 TLS 连接，就可以用 GitHub REST API 把整棵目录树推上去。

它做的事：
  1. 用 token 校验身份（GET /user）
  2. 创建仓库（已存在则复用）
  3. 遍历工作目录，按 .gitignore 规则筛选文件
  4. 逐个文件建 blob → 建 tree → 建 commit → 创建或更新分支引用
  5. 设置仓库描述、主页与 topics
  6. 可选：打一个 release 标签并上传发布物（如白皮书 PDF/DOCX）

用法：
    # 先干跑，看会推送哪些文件
    python tools/publish.py --owner sara-protocol --repo meaning-intelligence --dry-run

    # 真正推送（token 从环境变量读，避免落进 shell 历史）
    set GITHUB_TOKEN=ghp_xxx          # Windows
    export GITHUB_TOKEN=ghp_xxx       # Linux / macOS
    python tools/publish.py --owner sara-protocol --repo meaning-intelligence

安全提示：token 只在本进程内使用，不写入任何文件。用完请立即在 GitHub 上吊销。

Token 权限：细粒度 token 需要
    · Repository permissions → Contents: Read and write
    · Repository permissions → Administration: Read and write（用于创建仓库）
    · Repository permissions → Metadata: Read（自动包含）
"""
from __future__ import annotations

import argparse
import base64
import fnmatch
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.github.com"
UPLOADS = "https://uploads.github.com"
UA = "meaning-intelligence-publisher/1.0"
API_VERSION = "2022-11-28"

# 这些永远不进仓库
ALWAYS_SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache",
                    ".ruff_cache", ".venv", "venv", "node_modules", "media"}
ALWAYS_SKIP_SUFFIX = {".pyc", ".pyo", ".pyd"}


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------
class GitHubError(RuntimeError):
    def __init__(self, status, method, url, body):
        self.status, self.method, self.url, self.body = status, method, url, body
        super().__init__(f"HTTP {status} {method} {url}\n{body[:800]}")


def get_token_scopes(token: str) -> set:
    """读取 token 的 OAuth scope 列表（来自 GET /user 的 X-OAuth-Scopes 响应头）。

    fine-grained token 不返回这个头，此时返回空集合 —— 调用方必须把「读不到」
    与「确定没有」区分对待，否则会误判并做出错误的自适应行为。
    """
    req = urllib.request.Request(f"{API}/user", headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": UA,
    })
    with urllib.request.urlopen(req, timeout=30,
                                context=ssl.create_default_context()) as r:
        header = r.headers.get("X-OAuth-Scopes")
        me = json.loads(r.read().decode())
    if header is None:
        return set(), me          # fine-grained：头上没有这个字段
    return {s.strip() for s in header.split(",") if s.strip()}, me


# README 里的 CI 徽章行。当 workflow 文件推不上去时，这行会指向一个不存在的
# workflow，GitHub 返回 404，访客看到的是一个破图。宁可暂时不显示徽章，
# 也不要让门面上挂着一个坏链接。
CI_BADGE_RE = re.compile(r"^\[!\[CI\]\(.*$\n?", re.MULTILINE)


def strip_ci_badge(text: str) -> tuple:
    """移除 CI 徽章行，返回 (新文本, 是否改动过)。"""
    new = CI_BADGE_RE.sub("", text)
    return new, new != text


def request(method: str, url: str, token: str, payload=None, *, raw=None,
            content_type="application/json", ok=(200, 201, 204)):
    """发一个 GitHub API 请求。raw 为 bytes 时直接作为 body 上传。"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": UA,
    }
    if raw is not None:
        data = raw
        headers["Content-Type"] = content_type
    elif payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    else:
        data = None

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    # 显式用默认 SSL 上下文（Python 走 OpenSSL，不依赖 Windows Schannel）
    ctx = ssl.create_default_context()

    # 网络层重试。推一次仓库要发 60+ 个请求、传数 MB，
    # 任何一个请求被中途掐断都会让整次发布失败。
    # 实测在走本地代理（TUN/fake-IP）的环境下，会偶发
    # `SSL: UNEXPECTED_EOF_WHILE_READING`，重试即可恢复。
    RETRYABLE_NET = (urllib.error.URLError, TimeoutError,
                     ConnectionResetError, ConnectionAbortedError, ssl.SSLError)
    last_exc = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
                body = resp.read().decode("utf-8", "replace")
                if resp.status not in ok:
                    raise GitHubError(resp.status, method, url, body)
                return json.loads(body) if body.strip() else {}
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            if e.code in ok:
                return json.loads(detail) if detail.strip() else {}
            # 5xx 与限流是服务端瞬时问题，重试；4xx 是调用方问题，直接抛
            if e.code in (429, 500, 502, 503, 504) and attempt < 3:
                wait = 1.5 * (2 ** attempt)
                print(f"    [net] HTTP {e.code}，{wait:.1f}s 后重试 "
                      f"({attempt + 1}/3) {method} {url.split('/repos/')[-1][:60]}")
                time.sleep(wait)
                last_exc = e
                continue
            raise GitHubError(e.code, method, url, detail) from None
        except RETRYABLE_NET as e:
            last_exc = e
            if attempt < 3:
                wait = 1.5 * (2 ** attempt)
                print(f"    [net] {type(e).__name__}，{wait:.1f}s 后重试 "
                      f"({attempt + 1}/3) {method} {url.split('/repos/')[-1][:60]}")
                time.sleep(wait)
                continue
            raise
    raise last_exc  # pragma: no cover


# --------------------------------------------------------------------------
# .gitignore（务实子集，足够本项目使用）
# --------------------------------------------------------------------------
class IgnoreRules:
    """支持：注释 / 空行 / 目录模式(尾随 '/') / 根锚定(前导 '/') /
    '*' 与 '?' 通配 / '**' / 取反('!')。后出现的规则覆盖先出现的。
    """

    def __init__(self, patterns):
        self.rules = []          # (negate, pattern, dir_only, anchored)
        for raw in patterns:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            negate = line.startswith("!")
            if negate:
                line = line[1:]
            line = line.strip()
            if not line:
                continue
            dir_only = line.endswith("/")
            line = line.rstrip("/")
            anchored = line.startswith("/") or "/" in line
            line = line.lstrip("/")
            self.rules.append((negate, line, dir_only, anchored))

    @classmethod
    def from_file(cls, path: Path):
        if not path.is_file():
            return cls([])
        return cls(path.read_text(encoding="utf-8", errors="replace").splitlines())

    def ignored(self, rel: str, is_dir: bool) -> bool:
        rel = rel.replace(os.sep, "/")
        name = rel.rsplit("/", 1)[-1]
        result = False
        for negate, pat, dir_only, anchored in self.rules:
            if dir_only and not is_dir:
                continue
            if anchored:
                hit = fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(rel, pat + "/*")
            else:
                hit = (fnmatch.fnmatch(name, pat)
                       or fnmatch.fnmatch(rel, pat)
                       or fnmatch.fnmatch(rel, "*/" + pat)
                       or fnmatch.fnmatch(rel, "*/" + pat + "/*"))
            if hit:
                result = not negate
        return result


def collect_files(root: Path, extra_skip=()):
    """遍历 root，返回 [(相对路径, 绝对路径, 是否可执行)]，按 .gitignore 过滤。"""
    rules = IgnoreRules.from_file(root / ".gitignore")
    extra = set(extra_skip)
    out = []

    for dirpath, dirnames, filenames in os.walk(root):
        d = Path(dirpath)
        rel_dir = d.relative_to(root).as_posix() if d != root else ""

        keep = []
        for name in sorted(dirnames):
            rel = f"{rel_dir}/{name}" if rel_dir else name
            if name in ALWAYS_SKIP_DIRS or name in extra:
                continue
            if rules.ignored(rel, is_dir=True):
                continue
            keep.append(name)
        dirnames[:] = keep

        for name in sorted(filenames):
            rel = f"{rel_dir}/{name}" if rel_dir else name
            if Path(name).suffix in ALWAYS_SKIP_SUFFIX or name in extra:
                continue
            if rules.ignored(rel, is_dir=False):
                continue
            p = d / name
            if not p.is_file():
                continue
            out.append((rel, p, name.endswith(".sh")))
    return out


# --------------------------------------------------------------------------
# 发布流程
# --------------------------------------------------------------------------
def ensure_repo(token, owner, repo, *, private, description, homepage, topics,
                is_org):
    """确保仓库存在。

    先 GET 再决定是否创建。这点很关键：如果 token 只授予了 Contents 权限、
    没有 Administration 权限（典型场景是"仓库已在网页上建好，只想推内容"），
    直接 POST /user/repos 返回的是 403 而不是 422，会被误判成致命错误。
    先探测存在性，就不必依赖建仓权限。
    """
    existing = None
    try:
        existing = request("GET", f"{API}/repos/{owner}/{repo}", token, ok=(200,))
    except GitHubError as e:
        if e.status != 404:
            raise

    if existing is not None:
        print(f"[repo] {owner}/{repo} 已存在（默认分支 "
              f"{existing.get('default_branch')!r}），直接推送")
    else:
        url = f"{API}/orgs/{owner}/repos" if is_org else f"{API}/user/repos"
        payload = {
            "name": repo,
            "description": description,
            "homepage": homepage,
            "private": private,
            "has_issues": True,
            "has_wiki": False,
            "has_projects": False,
            "auto_init": False,      # 由本脚本推第一个 commit
        }
        try:
            existing = request("POST", url, token, payload, ok=(201,))
            print(f"[repo] 已创建 {existing['full_name']}")
        except GitHubError as e:
            if e.status in (403, 404):
                raise SystemExit(
                    f"\n错误：无法创建仓库（HTTP {e.status}）。\n"
                    "当前 token 缺少建仓权限（Fine-grained 需要 "
                    "Administration: Read and write，且 Repository access 需覆盖新仓库）。\n"
                    "两个办法任选其一：\n"
                    f"  1) 在 https://github.com/new 手动创建一个**完全空**的仓库\n"
                    f"     （owner={owner}，name={repo}，不要勾 README / .gitignore / license），\n"
                    "     再重跑本命令 —— 此时 token 只需 Contents: Read and write；\n"
                    "  2) 给 token 补上 Administration: Read and write。\n"
                ) from None
            raise

    # 下面两项都需要 Administration 权限；缺失时只警告，不中断推送。
    try:
        request("PATCH", f"{API}/repos/{owner}/{repo}", token,
                {"description": description, "homepage": homepage}, ok=(200,))
    except GitHubError as e:
        print(f"[repo] 警告：更新描述失败（HTTP {e.status}，需 Administration 权限），继续")

    if topics:
        try:
            request("PUT", f"{API}/repos/{owner}/{repo}/topics", token,
                    {"names": topics}, ok=(200,))
            print(f"[repo] topics: {', '.join(topics)}")
        except GitHubError as e:
            print(f"[repo] 警告：设置 topics 失败（{e.status}），继续")
    # 变量在重构时由 data 改名为 existing，这行曾漏改，
    # 导致 ensure_repo 抛 NameError —— 而预飞测试在认证步就 401 退出了，走不到这里。
    return existing


def bootstrap_empty_repo(token, owner, repo, root, files, *, branch, message):
    """在**完全为空**的仓库上写入第一个文件，把 git 仓库初始化出来。

    这是 GitHub 的一个非显然行为：仓库一个提交都没有时，
    `POST /git/blobs`、`/git/trees`、`/git/commits` 一律返回
    409 "Git Repository is empty." —— Git Data API 在空仓库上整体不可用。

    而 **Contents API 可以**在空仓库上写入文件（它自己负责创建首个提交与分支）。
    所以这里先用 Contents API 落一个文件，之后 Git Data API 就能正常工作了。
    优先用 README.md：它的内容随后的批量提交里本来就一样，
    blob sha 相同，因此不会产生一次多余的内容变更。
    """
    pick = next((f for f in files if f[0] == "README.md"), files[0])
    rel, path, _ = pick
    payload = {
        "message": message,
        "content": base64.b64encode(path.read_bytes()).decode("ascii"),
        "branch": branch,
    }
    request("PUT",
            f"{API}/repos/{owner}/{repo}/contents/{urllib.parse.quote(rel)}",
            token, payload, ok=(200, 201))
    print(f"[boot] 空仓库：已用 Contents API 写入 {rel} 完成初始化")


def get_head(token, owner, repo, branch):
    """返回 (parent_commit_sha, base_tree_sha)；空仓库返回 (None, None)。"""
    try:
        ref = request("GET", f"{API}/repos/{owner}/{repo}/git/ref/heads/{branch}",
                      token, ok=(200,))
    except GitHubError as e:
        # 两种「还没有这个分支」的形态都要认：
        #   404 —— 仓库有内容，但没有名为 branch 的分支
        #   409 —— 仓库**完全为空**（Git Repository is empty），此时连 refs 都还不存在
        # 只判 404 会在全新的空仓库上直接抛错，而空仓库恰恰是本工具最常见的起点。
        if e.status in (404, 409):
            print(f"[head] {branch} 尚不存在（HTTP {e.status}），将创建首个 commit")
            return None, None
        raise
    commit_sha = ref["object"]["sha"]
    commit = request("GET", f"{API}/repos/{owner}/{repo}/git/commits/{commit_sha}",
                     token, ok=(200,))
    return commit_sha, commit["tree"]["sha"]


def push_tree(token, owner, repo, root: Path, files, *, branch, message,
              parent, base_tree, replace=False, drop_ci_badge=False):
    entries = []
    total = len(files)
    for i, (rel, path, executable) in enumerate(files, 1):
        content = path.read_bytes()
        if drop_ci_badge and rel == "README.md":
            text = content.decode("utf-8")
            text, changed = strip_ci_badge(text)
            if changed:
                content = text.encode("utf-8")
                print("[readme] 已从 README 移除 CI 徽章 —— 本次不推送 workflow，"
                      "徽章会指向一个不存在的文件（访客看到的是破图）")
        blob = request("POST", f"{API}/repos/{owner}/{repo}/git/blobs", token,
                       {"content": base64.b64encode(content).decode("ascii"),
                        "encoding": "base64"}, ok=(201,))
        entries.append({"path": rel, "mode": "100755" if executable else "100644",
                        "type": "blob", "sha": blob["sha"]})
        if i % 25 == 0 or i == total:
            print(f"[blob] {i}/{total}")

    tree_payload = {"tree": entries}
    # replace=True 时不给 base_tree，得到一棵"只含本次文件"的树，
    # 这样被 .gitignore 排除或已删除的文件会真正从仓库里消失。
    if base_tree and not replace:
        tree_payload["base_tree"] = base_tree

    skipped = []
    tree = post_tree(token, owner, repo, tree_payload)

    if tree is None:
        # 走到这里说明是 404。先怀疑 workflow scope —— 见下方注释。
        wf = [e for e in entries if e["path"].startswith(".github/workflows/")]
        if wf:
            skipped = wf
            entries = [e for e in entries if not e["path"].startswith(".github/workflows/")]
            tree_payload["tree"] = entries
            print(f"[tree] 404：疑似 token 缺少 workflow scope，"
                  f"先跳过 {len(wf)} 个 workflow 文件重试")
            tree = post_tree(token, owner, repo, tree_payload)
        if tree is None:
            raise RuntimeError("创建 tree 失败（HTTP 404），且移除 workflow 文件后仍失败")
        print(f"[warn] 已跳过 {len(skipped)} 个 workflow 文件：")
        for e in skipped:
            print(f"         {e['path']}")

    print(f"[tree] {tree['sha'][:10]}  条目 {len(entries)}")

    commit_payload = {"message": message, "tree": tree["sha"],
                      "parents": [parent] if parent else []}
    commit = request("POST", f"{API}/repos/{owner}/{repo}/git/commits", token,
                     commit_payload, ok=(201,))
    print(f"[commit] {commit['sha'][:10]}  {message.splitlines()[0]}")

    if parent:
        request("PATCH", f"{API}/repos/{owner}/{repo}/git/refs/heads/{branch}", token,
                {"sha": commit["sha"], "force": True}, ok=(200,))
    else:
        request("POST", f"{API}/repos/{owner}/{repo}/git/refs", token,
                {"ref": f"refs/heads/{branch}", "sha": commit["sha"]}, ok=(201,))
    print(f"[ref] refs/heads/{branch} -> {commit['sha'][:10]}")
    return commit["sha"], skipped


def post_tree(token, owner, repo, payload):
    """创建 tree。

    GitHub 有一条**故意模糊化**的规则：token 缺少 `workflow` scope 时，
    对 `.github/workflows/` 下文件的任何 git 操作都返回 **404 Not Found**，
    而不是 403 —— 目的是不向无权限者泄露这类文件的存在。
    报错信息里只有一句 `{"message":"Not Found"}`，极具误导性
    （会让人以为 owner/repo 写错了）。因此这里把 404 转成 None 交给上层判断。
    """
    try:
        return request("POST", f"{API}/repos/{owner}/{repo}/git/trees", token,
                       payload, ok=(201,))
    except GitHubError as e:
        if e.status == 404:
            return None
        raise


# 工作流与 issue 表单会引用这些标签。
# GitHub 对**不存在的标签是静默丢弃**的：不报错、不提示，只是标签不生效。
# 所以必须在推送时把它们建出来，否则分诊与升级逻辑会静默失效。
REQUIRED_LABELS = [
    ("falsification-report", "EF4444", "证伪报告 / Falsification report"),
    ("needs-maintainer-review", "F97316", "等待维护者回复 / Awaiting maintainer reply"),
    ("awaiting-response", "9CA3AF", "等待提交者补充 / Awaiting reporter response"),
    ("maintenance-digest", "1B3A5C", "维护摘要累积议题 / Maintenance digest"),
    ("L1", "2A5C8E", "L1 减负 / Cognitive Load Reduction"),
    ("L2", "3B6EA5", "L2 可体验 / Experiential Rendering"),
    ("L3", "6B4C9A", "L3 意义生成 / Meaning Generation"),
    ("L4", "8A6BB5", "L4 价值评估 / Value Assessment"),
    ("L5", "C49B3B", "L5 方向选择 / Direction Selection"),
    ("L6", "D9B45C", "L6 反思与审视递归 / Recursive Reflection"),
]


def ensure_labels(token, owner, repo):
    """创建缺失的标签。需要 Issues: write 权限；缺失时只提示，不中断。"""
    try:
        existing = {l["name"] for l in
                    request("GET", f"{API}/repos/{owner}/{repo}/labels?per_page=100",
                            token, ok=(200,))}
    except GitHubError as e:
        print(f"[label] 警告：无法读取标签列表（HTTP {e.status}）")
        return

    created, denied = 0, False
    for name, color, desc in REQUIRED_LABELS:
        if name in existing:
            continue
        try:
            request("POST", f"{API}/repos/{owner}/{repo}/labels", token,
                    {"name": name, "color": color, "description": desc}, ok=(201,))
            created += 1
        except GitHubError as e:
            if e.status in (403, 404):
                denied = True
                break
            print(f"[label] 创建 {name} 失败：HTTP {e.status}")

    if denied:
        print("[label] 警告：token 缺少 Issues: write 权限，无法创建标签。")
        print("       标签不存在时 GitHub 会**静默丢弃**，分诊与升级逻辑将不生效。")
        print(f"       请到 https://github.com/{owner}/{repo}/labels 手动创建以下标签：")
        for name, color, desc in REQUIRED_LABELS:
            print(f"         {name:<26} #{color}  {desc}")
    elif created:
        print(f"[label] 已创建 {created} 个标签")
    else:
        print("[label] 标签已齐全")




def _read_whitepaper_version() -> str:
    """从 VERSION.yaml 读取 whitepaper.version（如 '1.1' 返回 'v1.1'）。
    找不到文件时返回 'v0.0' 而非崩溃。"""
    try:
        import re
        v = Path(__file__).resolve().parent.parent / "VERSION.yaml"
        if not v.exists():
            v = Path("VERSION.yaml")
        if not v.exists():
            return "v0.0"
        txt = v.read_text(encoding="utf-8")
        pattern = r'^whitepaper:.*?^\s+version:\s*"([^"]+)"'
        m = re.search(pattern, txt, re.MULTILINE | re.DOTALL)
        if m:
            return "v" + m.group(1)
    except Exception:
        pass
    return "v0.0"


def ascii_asset_name(path: Path, version: str = None) -> str:
    """给 release 附件取一个 ASCII 名。

    为什么必须这样：GitHub 在上传 release 附件时会把**非 ASCII 文件名清洗掉**，
    而且不报错。实测 `意义智能_元智能理论与分层应用_公开发布白皮书_v1.0_中英双语.docx`
    被上传成了 `_._._v1.0_.docx` —— 外部用户下载到的就是一个乱名文件。
    所以附件名一律走 ASCII。
    """
    if version is None:
        version = _read_whitepaper_version()
    name = path.name
    if name.isascii():
        return name
    ext = path.suffix.lstrip(".")
    low = name.lower()
    if "whitepaper" in low or path.parent.name == "dist":
        return f"Meaning-Intelligence-Whitepaper-{version}-zh-en.{ext}"
    # 通用兜底：把非 ASCII 段替换成连字符
    stem = "".join(ch if ch.isascii() and (ch.isalnum() or ch in "-_") else "-"
                   for ch in path.stem)
    while "--" in stem:
        stem = stem.replace("--", "-")
    return f"{stem.strip('-') or 'asset'}.{ext}"


def create_release(token, owner, repo, *, tag, name, body, assets):
    try:
        rel = request("POST", f"{API}/repos/{owner}/{repo}/releases", token,
                      {"tag_name": tag, "name": name, "body": body,
                       "draft": False, "prerelease": False}, ok=(201,))
        print(f"[release] 已创建 {tag}")
    except GitHubError as e:
        if e.status == 422:
            print(f"[release] {tag} 已存在，跳过创建")
            rel = request("GET", f"{API}/repos/{owner}/{repo}/releases/tags/{tag}",
                          token, ok=(200,))
        else:
            raise

    for asset in assets:
        # assets 元素可以是 "路径" 或 "路径::附件名"
        spec = str(asset).split("::", 1)
        p = Path(spec[0])
        if not p.is_file():
            print(f"[release] 跳过不存在的发布物：{p}")
            continue
        asset_name = spec[1] if len(spec) > 1 else ascii_asset_name(p)
        if not asset_name.isascii():
            print(f"[release] 警告：附件名 {asset_name!r} 含非 ASCII，"
                  f"GitHub 会把它清洗成乱码；请用 路径::名称 指定 ASCII 名")
        url = (f"{UPLOADS}/repos/{owner}/{repo}/releases/{rel['id']}/assets"
               f"?name={urllib.parse.quote(asset_name)}")
        try:
            request("POST", url, token, raw=p.read_bytes(),
                    content_type="application/octet-stream", ok=(201,))
            print(f"[release] 已上传 {asset_name}（{p.stat().st_size:,} 字节）")
        except GitHubError as e:
            if e.status == 422:
                print(f"[release] 资源 {asset_name} 已存在，跳过")
            else:
                print(f"[release] 上传 {asset_name} 失败：{e.status}")
    return rel


# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="无需 git 的 GitHub 发布器")
    ap.add_argument("--owner", required=True, help="GitHub 用户名或组织名")
    ap.add_argument("--repo", required=True, help="仓库名")
    ap.add_argument("--root", default=".", help="要发布的本地目录（默认当前目录）")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--token", default=None,
                    help="GitHub token；不传则读环境变量 GITHUB_TOKEN")
    ap.add_argument("--token-file", default=None,
                    help="从文件读取 token（避免出现在命令行历史中）")
    ap.add_argument("--org", action="store_true", help="owner 是组织而不是个人")
    ap.add_argument("--private", action="store_true", help="创建私有仓库")
    ap.add_argument("--description", default="")
    ap.add_argument("--homepage", default="")
    ap.add_argument("--topics", default="")
    ap.add_argument("--message", default=None, help="commit message")
    ap.add_argument("--replace", action="store_true",
                    help="用本次文件集完整替换仓库内容（删除本地已不存在的文件）")
    ap.add_argument("--release-tag", default=None, help="创建 release，如 v0.1.0")
    ap.add_argument("--release-name", default=None)
    ap.add_argument("--release-body-file", default=None)
    ap.add_argument("--asset", action="append", default=[],
                    help="release 附件路径，可重复")
    ap.add_argument("--dry-run", action="store_true", help="只列出将推送的文件")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not (root / "README.md").is_file():
        print(f"错误：{root} 下没有 README.md，这看起来不像仓库根目录", file=sys.stderr)
        return 2

    message = args.message or "chore: 发布 意义智能 / Meaning Intelligence"

    files = collect_files(root)
    total_bytes = sum(p.stat().st_size for _, p, _ in files)
    print(f"[scan] {root}")
    print(f"[scan] 将推送 {len(files)} 个文件，合计 {total_bytes:,} 字节"
          f"（已按 .gitignore 过滤）")
    for rel, p, exe in files:
        print(f"       {'x' if exe else ' '} {rel}  ({p.stat().st_size:,})")

    if args.dry_run:
        print("\n[dry-run] 未做任何网络请求。去掉 --dry-run 即真正推送。")
        return 0

    token = args.token
    if not token and args.token_file:
        raw = Path(args.token_file).read_text(encoding="utf-8-sig")
        # utf-8-sig 同时兼容带 BOM 与不带 BOM 的文件：
        # 记事本另存为 UTF-8 时可能写入 BOM，而 str.strip() 不会去掉 '\ufeff'
        # （'\ufeff'.isspace() 为 False），带进请求头会让认证莫名失败。
        token = raw.strip()
    if not token:
        token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("错误：缺少 token。用 --token / --token-file / 环境变量 GITHUB_TOKEN 提供。",
              file=sys.stderr)
        return 2

    scopes, me = get_token_scopes(token)
    print(f"[auth] 已认证为 {me['login']}")
    if scopes:
        print(f"[auth] token scopes: {', '.join(sorted(scopes))}")
    else:
        print("[auth] token scopes: （fine-grained token 不通过响应头暴露 scope）")

    # 主动判断能不能推 workflow 文件。
    # 不能推的时候，README 里的 CI 徽章就成了死链（指向不存在的 workflow，
    # 访客看到破图）。与其让仓库处于自相矛盾的状态，不如在推之前就把它摘掉。
    has_wf_files = any(rel.startswith(".github/workflows/") for rel, _, _ in files)
    drop_ci_badge = False
    if has_wf_files and scopes and "workflow" not in scopes:
        drop_ci_badge = True
        print("[auth] 注意：token 缺少 `workflow` scope，本次将跳过 workflow 文件，")
        print("       并同步移除 README 中的 CI 徽章以保持一致。")
    elif has_wf_files and not scopes:
        print("[auth] 提示：无法从响应头判断 workflow 权限（fine-grained token）。")
        print("       若推送时因权限被跳过 workflow 文件，README 的 CI 徽章会失效，")
        print("       请给 token 勾上 Workflows: Read and write 后重跑。")

    repo_info = ensure_repo(token, args.owner, args.repo, private=args.private,
                            description=args.description, homepage=args.homepage,
                            topics=[t for t in args.topics.split(",") if t],
                            is_org=args.org)

    # 先把工作流依赖的标签建出来：GitHub 对不存在的标签是静默丢弃的，
    # 不建的话分诊/升级逻辑会无声失效。缺 Issues: write 权限时只警告。
    ensure_labels(token, args.owner, args.repo)

    parent, base_tree = get_head(token, args.owner, args.repo, args.branch)
    if parent:
        print(f"[head] 现有 {args.branch} = {parent[:10]}")
    else:
        # 空仓库：Git Data API 此刻不可用，先用 Contents API 初始化
        bootstrap_empty_repo(token, args.owner, args.repo, root, files,
                             branch=args.branch,
                             message="chore: 初始化仓库 / bootstrap repository")
        parent, base_tree = get_head(token, args.owner, args.repo, args.branch)
        print(f"[head] 初始化后 {args.branch} = {(parent or '?')[:10]}")

    _, skipped = push_tree(token, args.owner, args.repo, root, files, branch=args.branch,
                           message=message, parent=parent, base_tree=base_tree,
                           replace=args.replace, drop_ci_badge=drop_ci_badge)

    if skipped:
        print()
        print("=" * 72)
        print("注意：有文件未能推送，原因与修法如下 / Some files were skipped")
        print("=" * 72)
        print("被跳过的文件（均为 GitHub Actions 工作流）：")
        for e in skipped:
            print(f"  · {e['path']}")
        print()
        print("原因：token 缺少 `workflow` scope。GitHub 对无此权限的 token")
        print("      在 workflow 文件上返回 404 而非 403，且不给出任何解释。")
        print()
        print("两种修法，任选其一：")
        print("  A. 给 token 补上 workflow 权限后重跑本命令：")
        print("     · classic token  → 在 https://github.com/settings/tokens 编辑该 token，")
        print("                        勾选 `workflow` 后保存（其余勾选不变），再重跑。")
        print("     · fine-grained   → 在 token 设置里把 `Workflows` 设为 Read and write。")
        print("  B. 不想改 token：到网页手动添加这三个文件——")
        print(f"     https://github.com/{args.owner}/{args.repo}/new/main/.github/workflows")
        print("     把本地 .github/workflows/ 下的文件内容逐个粘贴创建即可。")
        print("=" * 72)

    # 空仓库的 default_branch 取决于账号设置，可能是 master。
    # 我们推的是 args.branch（默认 main），若不校正，仓库首页会指向一个不存在的分支。
    current_default = (repo_info or {}).get("default_branch")
    if current_default != args.branch:
        try:
            request("PATCH", f"{API}/repos/{args.owner}/{args.repo}", token,
                    {"default_branch": args.branch}, ok=(200,))
            print(f"[repo] 默认分支 {current_default!r} -> {args.branch!r}")
        except GitHubError as e:
            print(f"[repo] 警告：默认分支仍为 {current_default!r}（HTTP {e.status}）。")
            print("       请到 Settings → General → Default branch 手动切换。")

    if args.release_tag:
        body = ""
        if args.release_body_file:
            body = Path(args.release_body_file).read_text(encoding="utf-8")

        # --asset 可省略：默认把 whitepaper/dist/ 下的全部发布物挂上去。
        # 这样命令行里就不必出现中文文件名 —— 在 cmd.exe 下传中文参数很容易踩编码坑。
        assets = list(args.asset)
        if not assets:
            dist = root / "whitepaper" / "dist"
            if dist.is_dir():
                assets = [str(p) for p in sorted(dist.iterdir()) if p.is_file()]
                print(f"[release] 未指定 --asset，自动挂载 whitepaper/dist/ 下 "
                      f"{len(assets)} 个文件")
        create_release(token, args.owner, args.repo,
                       tag=args.release_tag,
                       name=args.release_name or args.release_tag,
                       body=body, assets=assets)

    print(f"\n完成：https://github.com/{args.owner}/{args.repo}")
    print("安全提醒：请在 GitHub 设置中立即吊销本次使用的 token。")
    return 0


if __name__ == "__main__":
    # 把 API 异常翻译成人能看懂的话。
    # 否则一次 401 会甩出一整页 traceback，使用者很难判断到底哪一步错了。
    try:
        sys.exit(main())
    except GitHubError as e:
        print("", file=sys.stderr)
        if e.status == 401:
            print("错误：认证失败（HTTP 401）。", file=sys.stderr)
            print("  token 无效、已过期，或复制时混入了多余字符（引号、空格、Bearer 前缀）。",
                  file=sys.stderr)
            print("  请确认 token 文件里只有 token 本身（不含引号、空格或 Bearer 前缀）。",
                  file=sys.stderr)
        elif e.status == 403:
            print("错误：权限不足（HTTP 403）。", file=sys.stderr)
            print("  请检查 token 的 Repository access 是否覆盖目标仓库，", file=sys.stderr)
            print("  以及 Contents 是否为 Read and write。", file=sys.stderr)
            print(f"  服务端返回：{e.body[:400]}", file=sys.stderr)
        elif e.status == 404:
            print(f"错误：资源不存在（HTTP 404）—— {e.method} {e.url}", file=sys.stderr)
            # 一定要打出 body：404 的原因很多（路径、base_tree、blob sha…），
            # 只报状态码会让人以为是 owner/repo 拼错，从而查错方向。
            print(f"  服务端返回：{e.body[:500]}", file=sys.stderr)
        else:
            print(f"GitHub API 错误：HTTP {e.status} {e.method} {e.url}", file=sys.stderr)
            print(f"  {e.body[:600]}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n已中断，未做任何进一步写入。", file=sys.stderr)
        sys.exit(130)
