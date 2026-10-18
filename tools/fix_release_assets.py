"""通过 GitHub API 修复 Release 附件:删掉旧的乱码附件,上传 ASCII 名新附件。"""
import argparse
import json
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path

API = "https://api.github.com"


def req(method, path, token, data=None, raw=None, ok=(200, 201, 204)):
    url = path if path.startswith("http") else API + path
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "mi-release-asset-fix",
    }
    body = None
    if raw is not None:
        body = raw
        headers["Content-Type"] = "application/octet-stream"
    elif data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r) as resp:
            content = resp.read()
            return json.loads(content) if content.strip() else {}
    except urllib.error.HTTPError as e:
        b = e.read().decode("utf-8", "replace")
        raise SystemExit(f"HTTP {e.code} {method} {url}\n{b[:500]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--token-file", required=True)
    ap.add_argument("--delete-pattern", default="_._._",
                    help="删除匹配此片段的附件（默认匹配 _._._ 乱码）")
    ap.add_argument("--upload", nargs="+", default=[],
                    help="上传的本地文件（可多个）")
    args = ap.parse_args()

    token = Path(args.token_file).read_text(encoding="utf-8-sig").strip()

    # 1. 获取 release 及其现有附件
    rel = req("GET", f"/repos/{args.owner}/{args.repo}/releases/tags/{args.tag}", token)
    print(f"[release] id={rel['id']}  tag={rel['tag_name']}  现有附件 {len(rel['assets'])} 个:")
    for a in rel.get("assets", []):
        print(f"  - {a['name']}  ({a['size']} bytes)")

    # 2. 删除匹配乱码的附件
    deleted = 0
    for a in rel.get("assets", []):
        if args.delete_pattern in a["name"]:
            print(f"[delete] {a['name']}  (id={a['id']})")
            req("DELETE",
                f"/repos/{args.owner}/{args.repo}/releases/assets/{a['id']}",
                token)
            deleted += 1
    if deleted == 0:
        print(f"[delete] 没有匹配 '{args.delete_pattern}' 的附件")

    # 3. 上传 ASCII 名新附件
    upload_url = rel["upload_url"].replace("{?name,label}", "")
    for path_str in args.upload:
        p = Path(path_str)
        if not p.exists():
            print(f"⚠️ 未找到 {p},跳过")
            continue
        data = p.read_bytes()
        url = f"{upload_url}?name={urllib.parse.quote(p.name)}"
        print(f"[upload] {p.name}  ({len(data)} bytes)")
        req("POST", url, token, raw=data, ok=(201,))

    # 4. 复验
    rel2 = req("GET", f"/repos/{args.owner}/{args.repo}/releases/tags/{args.tag}", token)
    print(f"\n[verify] 最终 {len(rel2['assets'])} 个附件:")
    for a in rel2.get("assets", []):
        print(f"  ✅ {a['name']}  ({a['size']} bytes)")


if __name__ == "__main__":
    main()