import json, warnings
VALID_LAYERS = {"L1","L2","L3","L4","L5","L6"}
def load_config(path):
    with open(path, encoding="utf-8") as f: cfg = json.load(f)
    if "control_loop" in cfg:
        _validate_new(cfg); return cfg
    if isinstance(cfg.get("stack"), list) or "layers" in cfg:
        warnings.warn("旧结构 config 已自动迁移")
        return _migrate_old(cfg)
    raise ValueError(f"无法识别的 config 结构: {list(cfg.keys())}")
def _validate_new(cfg):
    abls = cfg["control_loop"].get("ablation", {})
    for aid, abl in abls.items():
        for layer, ov in abl.get("overrides", {}).items():
            if not (ov is None or isinstance(ov, dict)):
                raise ValueError(f"{aid}.overrides[{layer}] 类型非法: {type(ov).__name__}")
            if ov is None and layer not in VALID_LAYERS:
                raise ValueError(f"{aid} 移除未知层: {layer}")
    for eid, spec in cfg["control_loop"].get("evidence_levels", {}).items():
        if "label" in spec:
            raise ValueError(f"evidence_levels[{eid}] 含 label，违反单一真相源")
        if not spec.get("whitepaper_ref"):
            raise ValueError(f"evidence_levels[{eid}] 缺 whitepaper_ref")
def _migrate_old(cfg):
    return {"schema_version":"0.3.0","control_loop":{"can_rewrite_lower":["meta"],"evidence_levels":{},"ablation":{},"_migrated_from":"old"},**cfg}
