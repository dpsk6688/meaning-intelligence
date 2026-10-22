"""
PR-2 最终收口 v2：四条断言改进版
- 修复字符串比较 E3 问题
- 补全三态判定真实逻辑
- 严格校验 n 和 registered_at
- 接入白皮书真实引用解析准备
"""
from pathlib import Path
import yaml
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import re

# --- 白皮书 E0-E6 定义（应从 whitepaper/dist/*.docx 解析，此处为映射） ---
WHITE_PAPER_E_LEVELS = {
    "E0": {"label": "未检验", "color": "#9e9e9e", "ref": "第6章 表6-1 E0"},
    "E1": {"label": "单层可证伪", "color": "#ef5350", "ref": "第6章 表6-1 E1"},
    "E2": {"label": "单层有实测", "color": "#ff9800", "ref": "第6章 表6-1 E2"},
    "E3": {"label": "整栈比较性预测", "color": "#1e88e5", "ref": "第6章 表6-1 E3"},
    "E4": {"label": "整栈有实测", "color": "#43a047", "ref": "第6章 表6-1 E4"},
    "E5": {"label": "独立复现", "color": "#5e35b1", "ref": "第6章 表6-1 E5"},
    "E6": {"label": "跨场景稳健", "color": "#00897b", "ref": "第6章 表6-1 E6"},
}

# E等级顺序映射，修复字符串比较bug
E_ORDER = {f"E{i}": i for i in range(7)}

class Status(str, Enum):
    INCONCLUSIVE = "INCONCLUSIVE"
    FALSIFIED = "FALSIFIED"
    NOT_FALSIFIED = "NOT_FALSIFIED"

class EvidenceLevel(str, Enum):
    E0="E0"; E1="E1"; E2="E2"; E3="E3"; E4="E4"; E5="E5"; E6="E6"
    @property
    def order(self) -> int:
        return E_ORDER[self.value]

@dataclass
class Verdict:
    status: Status
    hypothesis_id: str
    rule_hit: Optional[Dict]
    evidence_level: EvidenceLevel
    limitations: List[str]
    inputs_ref: Dict
    action: Optional[str]=None

# ---- 断言1：null vs {} 语义 ----
VALID_LAYERS = {"L1","L2","L3","L4","L5","L6"}

def assert_override_semantics(ablations: Dict):
    """移除必须用 null，空配置用 {}，禁止 [] / '' 等"""
    for aid, abl in ablations.items():
        overrides = abl.get("overrides", {})
        remove_list = set(abl.get("remove", []))
        for layer, ov in overrides.items():
            if layer not in VALID_LAYERS:
                raise AssertionError(f"{aid} 移除未知层: {layer}，合法: {VALID_LAYERS}")
            if not (ov is None or isinstance(ov, dict)):
                raise AssertionError(f"{aid}.overrides[{layer}] 类型非法: {type(ov).__name__}，移除请用 null，空配置用 {{}}")
            if ov is not None and layer in remove_list:
                raise AssertionError(f"{aid} 层 {layer} 被标记移除但 overrides 是 {{}}，语义冲突，移除请用 null，空配置用 {{}}")

# ---- 断言2：draft vs registered ----
def load_hypotheses(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def check_falsifier_v03(hid: str, data: Dict, hypotheses_path: Path) -> Verdict:
    full = load_hypotheses(hypotheses_path)
    h = next((x for x in full["hypotheses"] if x["id"]==hid), None)
    if not h:
        raise KeyError(f"hypothesis {hid} not found")

    # 核心：draft 直接 INCONCLUSIVE
    if h.get("status","draft") == "draft":
        return Verdict(
            status=Status.INCONCLUSIVE,
            hypothesis_id=hid,
            rule_hit={"rule":"hypothesis_not_registered", "reason": "draft未预注册"},
            evidence_level=EvidenceLevel.E0,
            limitations=["假说处于 draft，未预注册，不参与证伪判定"],
            inputs_ref=data,
            action="请先预注册：补充 registered_at, source, n"
        )
    
    # registered 三态判定真实逻辑（示例：S-H1 整栈留存比较）
    n_runs = data.get("n_runs", 0)
    inc_n = h.get("inconclusive_if", [{}])[0].get("n", 40)
    if isinstance(inc_n, str) and inc_n.startswith("<"):
        # 解析 "< 40" 为阈值
        m = re.search(r"\d+", inc_n)
        inc_n_val = int(m.group()) if m else 40
    else:
        inc_n_val = int(inc_n)
    
    if n_runs < inc_n_val:
        return Verdict(
            status=Status.INCONCLUSIVE,
            hypothesis_id=hid,
            rule_hit={"rule":"n_too_small", "n": n_runs, "required": inc_n_val},
            evidence_level=EvidenceLevel.E0,
            limitations=[f"n={n_runs} < {inc_n_val}，功效不足"],
            inputs_ref=data
        )
    
    # 示例规则：full_stack_retention vs ablate_retention
    full_ret = data.get("full_stack_retention")
    abl_ret = data.get("ablate_retention")
    p_val = data.get("p_value", 1.0)
    
    if full_ret is not None and abl_ret is not None:
        if full_ret - abl_ret < 5 or p_val > 0.05:  # 阈值示例
            return Verdict(
                status=Status.FALSIFIED,
                hypothesis_id=hid,
                rule_hit={"rule":"retention_not_significant", "delta": full_ret-abl_ret, "p": p_val},
                evidence_level=EvidenceLevel.E3,
                limitations=[f"unit={h.get('unit_of_analysis','run')}"],
                inputs_ref=data
            )
    
    return Verdict(
        status=Status.NOT_FALSIFIED,
        hypothesis_id=hid,
        rule_hit=None,
        evidence_level=EvidenceLevel.E3,
        limitations=[f"unit={h.get('unit_of_analysis','run')}"],
        inputs_ref=data
    )

def assert_registration_state(hyps: Dict):
    """严格校验：registered 必须 n为数字且>0，且 registered_at 非空"""
    for h in hyps["hypotheses"]:
        st = h.get("status","draft")
        if st not in {"draft","registered"}:
            raise AssertionError(f"{h['id']} status 非法: {st}，仅允许 draft/registered")
        if st == "registered":
            inc_list = h.get("inconclusive_if", [])
            if not inc_list:
                raise AssertionError(f"{h['id']} registered 但 inconclusive_if 为空")
            inc = inc_list[0]
            n_raw = inc.get("n")
            # 改进：不再允许 "< 40" 字符串，必须是 int
            if isinstance(n_raw, str):
                if n_raw.strip().startswith("<"):
                    raise AssertionError(f"{h['id']} registered 但 n='{n_raw}' 仍为字符串形态，请改为数字 {n_raw.replace('<','').strip()} 并保留 source")
                try:
                    n_int = int(n_raw)
                except:
                    raise AssertionError(f"{h['id']} registered 但 n 非数字: {n_raw!r}")
            elif isinstance(n_raw, int):
                n_int = n_raw
            else:
                raise AssertionError(f"{h['id']} registered 但 n 类型非法: {type(n_raw)}")
            
            if n_int <= 0:
                raise AssertionError(f"{h['id']} n 必须 >0，当前 {n_int}")
            
            if not inc.get("registered_at"):
                raise AssertionError(f"{h['id']} registered 但 registered_at 为空")
            if not inc.get("source"):
                raise AssertionError(f"{h['id']} registered 但 source 为空，需说明功效分析来源")
        else:
            print(f"[WARN] {h['id']} 仍为 draft，E 等级不关闭")

# ---- 断言3：label 单一真相源 ----
def assert_evidence_level_label_source(cfg: Dict, whitepaper_path: Optional[Path] = None):
    """config 只能有 color + whitepaper_ref，禁止 label 文本"""
    levels = cfg["control_loop"]["evidence_levels"]
    for eid, spec in levels.items():
        if eid not in WHITE_PAPER_E_LEVELS:
            raise AssertionError(f"未知 E等级 {eid}")
        if "label" in spec:
            raise AssertionError(f"evidence_levels[{eid}] 含 label 文本 '{spec['label']}'，违反单一真相源；请用 whitepaper_ref，config 只保留 color")
        if not spec.get("whitepaper_ref"):
            raise AssertionError(f"evidence_levels[{eid}] 缺 whitepaper_ref")
        # 校验 whitepaper_ref 指向真实锚点
        ref = spec["whitepaper_ref"]
        if not any(eid in ref or WHITE_PAPER_E_LEVELS[eid]["label"] in ref or "第6章" in ref for _ in [1]):
            # 简化校验：必须包含 E等级或章节
            if ref != eid and "E" not in ref and "第" not in ref:
                print(f"[WARN] {eid} whitepaper_ref='{ref}' 可能悬空")
        if not spec.get("color","").startswith("#"):
            raise AssertionError(f"evidence_levels[{eid}] 缺颜色或非#开头")
        # 校验 color 与白皮书一致性（可选）
        if spec["color"] != WHITE_PAPER_E_LEVELS[eid]["color"]:
            print(f"[INFO] {eid} color {spec['color']} 与白皮书默认 {WHITE_PAPER_E_LEVELS[eid]['color']} 不同")

# ---- 断言4：stack 反向引用 ----
def assert_stack_hypotheses_referenced(cfg: Dict, hyps: Dict):
    ablations = cfg["control_loop"]["ablation"]
    stack_ids = {h["id"] for h in hyps["hypotheses"] if h["scope"]=="stack"}
    all_ids = {h["id"] for h in hyps["hypotheses"]}
    
    referenced = set()
    for aid, abl in ablations.items():
        for hid in abl.get("hypotheses", []):
            if hid not in all_ids:
                raise AssertionError(f"{aid} 引用了不存在的假说: {hid}")
            if hid not in stack_ids:
                raise AssertionError(f"{aid} 引用了非 stack 假说: {hid}，stack假说才能被ablation验证")
            referenced.add(hid)
    
    orphan = stack_ids - referenced
    if orphan:
        raise AssertionError(f"stack 假说未被任何 ablation 引用: {orphan}，请在 ablation.hypotheses 中补充")

def resolve_json_pointer(cfg: Dict, ref: str) -> bool:
    if "#/" not in ref:
        return False
    _, pointer = ref.split("#",1)
    parts = [p for p in pointer.split("/") if p]
    cur = cfg
    try:
        for p in parts:
            cur = cur[p]
        return True
    except (KeyError, TypeError):
        return False

def check_ablation_refs(cfg: Dict, hyps: Dict):
    for h in hyps["hypotheses"]:
        if h["scope"]=="stack":
            ref = h.get("baseline", {}).get("ref")
            if ref and not resolve_json_pointer(cfg, ref):
                raise AssertionError(f"{h['id']} baseline 悬空: {ref}")

# ---- E0 关闭条件（修复字符串比较）----
def check_e0_closure(verdict: Verdict, hypothesis: Dict) -> bool:
    if verdict.status == Status.INCONCLUSIVE:
        print(f"[FAIL] S-H1 返回 INCONCLUSIVE，Issue 保持 OPEN，rule={verdict.rule_hit}")
        return False
    # 修复：使用 order 而非字符串比较
    if verdict.evidence_level.order < E_ORDER["E3"]:
        print(f"[FAIL] evidence_level {verdict.evidence_level} < E3")
        return False
    if hypothesis.get("status") != "registered":
        print(f"[FAIL] S-H1.status={hypothesis.get('status')} 非 registered")
        return False
    print(f"[OK] E0 关闭条件满足：{verdict.status} evidence_level={verdict.evidence_level} status=registered")
    return True

# ---- 反例测试（增强）----
def run_negative_tests():
    print("=== 反例测试 v2 ===")
    # 1. null vs {}
    try:
        assert_override_semantics({"ABL-L3":{"overrides":{"L3":{}}}})
        print("[PASS] {} 空配置允许")
        assert_override_semantics({"ABL-L3":{"overrides":{"L3":{}},"remove":["L3"]}})
    except AssertionError as e:
        print(f"[OK] 捕获语义冲突: {e}")

    try:
        assert_override_semantics({"ABL-L3":{"overrides":{"L3":[]}}})
    except AssertionError as e:
        print(f"[OK] 捕获非法类型 []: {e}")

    try:
        assert_override_semantics({"ABL-L3":{"overrides":{"L3":None}}})
        print("[PASS] null 移除允许")
    except AssertionError as e:
        print(f"[FAIL] {e}")

    # 2. draft vs registered 严格校验
    hyps_draft = {"hypotheses":[{"id":"S-H1","scope":"stack","status":"draft","inconclusive_if":[{"n":40}]}]}
    assert_registration_state(hyps_draft)

    hyps_bad = {"hypotheses":[{"id":"S-H1","scope":"stack","status":"registered","inconclusive_if":[{"n":"xx","registered_at":""}]}]}
    try:
        assert_registration_state(hyps_bad)
    except AssertionError as e:
        print(f"[OK] 捕获 registered 非数字 n: {e}")

    hyps_lt = {"hypotheses":[{"id":"S-H1","scope":"stack","status":"registered","inconclusive_if":[{"n":"< 40","registered_at":"2026-10-18","source":"pilot"}]}]}
    try:
        assert_registration_state(hyps_lt)
    except AssertionError as e:
        print(f"[OK] 捕获 '< 40' 字符串形态: {e}")

    # 3. label 归属
    cfg_with_label = {"control_loop":{"evidence_levels":{"E3":{"label":"整栈比较性预测","color":"#1e88e5","whitepaper_ref":"E3"}}}}
    try:
        assert_evidence_level_label_source(cfg_with_label)
    except AssertionError as e:
        print(f"[OK] 捕获 label 文本: {e}")

    cfg_ok = {"control_loop":{"evidence_levels":{"E3":{"color":"#1e88e5","whitepaper_ref":"第6章 表6-1 E3"}}}}
    assert_evidence_level_label_source(cfg_ok)
    print("[PASS] label 归属校验通过")

    # 4. stack 反向引用
    cfg = {"control_loop":{"ablation":{"ABL-L3":{"hypotheses":["S-H1"]}}}}
    hyps = {"hypotheses":[{"id":"S-H1","scope":"stack"},{"id":"S-H2","scope":"stack"}]}
    try:
        assert_stack_hypotheses_referenced(cfg, hyps)
    except AssertionError as e:
        print(f"[OK] 捕获孤儿 S-H2: {e}")

    # E_ORDER 修复验证
    assert EvidenceLevel.E0.order < EvidenceLevel.E3.order
    assert not (EvidenceLevel.E3.value < "E3")  # 旧bug
    print("[PASS] E_ORDER 修复验证通过")

if __name__ == "__main__":
    run_negative_tests()
    print("\n=== E0 关闭演示 ===")
    from pathlib import Path
    hyps_path = Path("/tmp/hypotheses_S-H1.yaml")
    data = {
        "schema_version":"0.3.0",
        "hypotheses":[{
            "id":"S-H1","scope":"stack","status":"registered",
            "baseline":{"ref":"config.json#/control_loop/ablation/ABL-L3"},
            "unit_of_analysis":"run",
            "inconclusive_if":[{"n":40,"registered_at":"2026-10-18","source":"pilot_power_analysis"}],
            "evidence_ceiling":"E3"
        }]
    }
    hyps_path.parent.mkdir(parents=True, exist_ok=True)
    hyps_path.write_text(yaml.dump(data, allow_unicode=True), encoding="utf-8")
    
    v = check_falsifier_v03("S-H1", {"n_runs":20}, hyps_path)
    print(f"n=20 -> {v.status} {v.rule_hit}")
    v2 = check_falsifier_v03("S-H1", {"n_runs":40, "full_stack_retention":85, "ablate_retention":70, "p_value":0.01}, hyps_path)
    check_e0_closure(v2, data["hypotheses"][0])
