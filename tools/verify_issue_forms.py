"""按 GitHub Issue Forms 的官方结构约束校验模板。

为什么要自己写：GitHub 的 /issues/new 页面是纯客户端渲染的，
HTTP 抓取永远是同一个空壳（有效与无效模板返回的 HTML 无法区分），
所以只能做结构校验 —— 而结构错误恰恰是让表单静默失效的常见原因
（例如 type 拼错、id 重复、markdown 元素带了 id）。

校验规则来源：GitHub Docs — Syntax for GitHub's form schema。
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent   # 仓库根（tools/ 的上一级）
TPL_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"

VALID_TOP = {"name", "description", "title", "labels", "assignees", "body", "projects"}
VALID_TYPES = {"markdown", "input", "textarea", "dropdown", "checkboxes"}
# 这些类型必须有 id；markdown 必须没有 id
NEEDS_ID = {"input", "textarea", "dropdown", "checkboxes"}
VALID_INPUT_TYPES = {"text", "textarea", "date", "datetime-local", "email",
                     "month", "number", "password", "tel", "time", "url", "week"}
VALID_VALIDATION_KEYS = {"required"}

errors, warns = [], []


def check_form(path: Path, doc: dict):
    tag = path.name
    unknown = set(doc) - VALID_TOP
    if unknown:
        errors.append(f"{tag}: 顶层出现未知字段 {sorted(unknown)}")
    for req in ("name", "description", "body"):
        if req not in doc:
            errors.append(f"{tag}: 缺少必填顶层字段 `{req}`")
    if not isinstance(doc.get("body"), list):
        errors.append(f"{tag}: `body` 必须是数组")
        return

    seen_ids = set()
    for i, el in enumerate(doc["body"]):
        where = f"{tag} body[{i}]"
        if not isinstance(el, dict):
            errors.append(f"{where}: 必须是对象")
            continue
        t = el.get("type")
        if t not in VALID_TYPES:
            errors.append(f"{where}: type={t!r} 不在 {sorted(VALID_TYPES)}")
            continue
        if t in NEEDS_ID:
            eid = el.get("id")
            if not eid:
                errors.append(f"{where}: type={t} 必须有 `id`")
            elif not isinstance(eid, str) or not eid.replace("_", "").replace("-", "").isalnum():
                errors.append(f"{where}: id={eid!r} 只能含字母数字与 _ -")
            elif eid.lower() in seen_ids:
                errors.append(f"{where}: id={eid!r} 与前面的元素重复（id 必须唯一）")
            else:
                seen_ids.add(eid.lower())
        if t == "markdown":
            if "id" in el:
                errors.append(f"{where}: markdown 元素不能带 `id`")
            if not (el.get("attributes") or {}).get("value"):
                errors.append(f"{where}: markdown 必须有 attributes.value")

        attrs = el.get("attributes") or {}
        if not isinstance(attrs, dict):
            errors.append(f"{where}: attributes 必须是对象")
            continue
        if t == "input":
            it = attrs.get("format")
            if it is not None and it not in VALID_INPUT_TYPES:
                warns.append(f"{where}: format={it!r} 不是 GitHub 文档列出的取值之一")
        if t in ("dropdown", "checkboxes"):
            opts = attrs.get("options")
            if not isinstance(opts, list) or not opts:
                errors.append(f"{where}: type={t} 必须有非空 attributes.options")
        if t == "input" and attrs.get("label") is None:
            warns.append(f"{where}: input 没有 label，表单里会显示为空标题")
        v = el.get("validations")
        if v is not None:
            if not isinstance(v, dict):
                errors.append(f"{where}: validations 必须是对象")
            else:
                bad = set(v) - VALID_VALIDATION_KEYS
                if bad:
                    errors.append(f"{where}: validations 含未知键 {sorted(bad)}（只支持 required）")
    # description 长度
    for field in ("name", "description"):
        val = doc.get(field, "")
        if isinstance(val, str) and len(val) > 200:
            warns.append(f"{tag}: {field} 超过 200 字符（{len(val)}）")


def check_config(path: Path, doc: dict):
    tag = path.name
    if "blank_issues_enabled" in doc and not isinstance(doc["blank_issues_enabled"], bool):
        errors.append(f"{tag}: blank_issues_enabled 必须是布尔值")
    links = doc.get("contact_links")
    if links is not None:
        if not isinstance(links, list):
            errors.append(f"{tag}: contact_links 必须是数组")
        else:
            for i, l in enumerate(links):
                miss = {"name", "url", "about"} - set(l or {})
                if miss:
                    errors.append(f"{tag}: contact_links[{i}] 缺少 {sorted(miss)}")


print(f"检查目录 {TPL_DIR}\n")
n = 0
for p in sorted(TPL_DIR.glob("*.yml")) + sorted(TPL_DIR.glob("*.yaml")):
    n += 1
    try:
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"{p.name}: YAML 解析失败 —— {e}")
        continue
    if not isinstance(doc, dict):
        errors.append(f"{p.name}: 顶层必须是对象")
        continue
    if p.name == "config.yml":
        check_config(p, doc)
    else:
        check_form(p, doc)
    print(f"  ✓ {p.name}  ({len(doc.get('body', []) or [])} 个 body 元素)")

print(f"\n共 {n} 个模板")
if warns:
    print("\n警告：")
    for w in warns:
        print("  ⚠", w)
if errors:
    print("\n错误：")
    for e in errors:
        print("  ✗", e)
print("\nRESULT:", "PASS" if not errors else f"FAIL ({len(errors)})")
sys.exit(0 if not errors else 1)
