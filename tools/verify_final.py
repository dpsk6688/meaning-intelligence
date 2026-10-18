import json, sys, yaml
VALID_LAYERS = {"L1","L2","L3","L4","L5","L6"}
def assert_override_semantics(ablations):
    for aid, abl in ablations.items():
        for layer, ov in abl.get("overrides", {}).items():
            assert ov is None or isinstance(ov, dict), f"{aid}.overrides[{layer}] 类型非法: {type(ov).__name__}"
            if ov is None: assert layer in VALID_LAYERS, f"{aid} 移除未知层: {layer}"
            else: assert abl.get("remove") != [layer], f"{aid} 层 {layer} 语义冲突，移除请用 null"
def assert_registration_state(hyps):
    for h in hyps["hypotheses"]:
        st = h.get("status", "draft")
        assert st in {"draft", "registered"}, f"{h['id']} status 非法: {st}"
        if st == "registered":
            n_rule = next((r for r in h.get("inconclusive_if", []) if "n" in r), None)
            assert n_rule is not None, f"{h['id']} registered 但缺 n 阈值规则"
            n = n_rule["n"]
            if isinstance(n, str):
                assert n.startswith("<") and n[1:].strip().isdigit(), \
                    f"{h['id']} n 格式非法: {n!r}"
            else:
                assert isinstance(n, int) and n > 0, f"{h['id']} n 非数字: {n!r}"
            assert n_rule.get("registered_at"), f"{h['id']} registered 但 registered_at 空"

def assert_evidence_level_label_source(cfg):
    for eid, spec in cfg["control_loop"].get("evidence_levels", {}).items():
        assert "label" not in spec, f"evidence_levels[{eid}] 含 label，违反单一真相源"
        assert spec.get("whitepaper_ref"), f"evidence_levels[{eid}] 缺 whitepaper_ref"
        assert spec.get("color","").startswith("#"), f"evidence_levels[{eid}] 缺颜色"
def assert_stack_hypotheses_referenced(cfg, hyps):
    abls = cfg["control_loop"].get("ablation", {})
    stack_ids = {h["id"] for h in hyps["hypotheses"] if h["scope"]=="stack"}
    ref = {h for a in abls.values() for h in a.get("hypotheses", [])}
    assert not (stack_ids - ref), f"stack 假说未被引用: {stack_ids - ref}"
    for a in abls.values():
        for h in a.get("hypotheses", []):
            assert h in stack_ids, f"引用了非 stack 假说: {h}"
def run_negative():
    ok = []
    try: assert_override_semantics({"X":{"overrides":{"L3":{}},"remove":["L3"]}}); ok.append(("[FAIL] {L3:{}}",False))
    except AssertionError as e: ok.append((f"[OK] 语义冲突: {e}",True))
    try: assert_override_semantics({"X":{"overrides":{"L3":[]}}}); ok.append(("[FAIL] []",False))
    except AssertionError as e: ok.append((f"[OK] 类型非法: {e}",True))
    try: assert_evidence_level_label_source({"control_loop":{"evidence_levels":{"E3":{"label":"x"}}}}); ok.append(("[FAIL] label",False))
    except AssertionError as e: ok.append((f"[OK] label 文本: {e}",True))
    try: assert_stack_hypotheses_referenced({"control_loop":{"ablation":{"A":{"hypotheses":["S-H1"]}}}},
            {"hypotheses":[{"id":"S-H1","scope":"stack"},{"id":"S-H2","scope":"stack"}]}); ok.append(("[FAIL] 孤儿",False))
    except AssertionError as e: ok.append((f"[OK] 孤儿: {e}",True))
    for m,p in ok: print(m)
    return all(p for _,p in ok)
def check_config(cfg_path, hyps_path):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    hyps = yaml.safe_load(open(hyps_path, encoding="utf-8"))
    assert_override_semantics(cfg["control_loop"].get("ablation", {}))
    assert_registration_state(hyps)
    assert_evidence_level_label_source(cfg)
    assert_stack_hypotheses_referenced(cfg, hyps)
    print("[OK] 四条断言全部通过")
if __name__=="__main__":
    if "--negative" in sys.argv: sys.exit(0 if run_negative() else 1)
    check_config("msi/config.json","hypotheses.yaml")
