import yaml
from dataclasses import dataclass, field
@dataclass
class Verdict:
    status: str; rule: str = None; evidence_level: str = "E0"
    limitations: list = field(default_factory=list); inputs: dict = field(default_factory=dict)
def load_hypothesis(hid, path="hypotheses.yaml"):
    with open(path, encoding="utf-8") as f: hyps = yaml.safe_load(f)["hypotheses"]
    for h in hyps:
        if h["id"] == hid: return h
    raise KeyError(f"假说不存在: {hid}")
def check_falsifier(hid, data=None, path="hypotheses.yaml"):
    h = load_hypothesis(hid, path)
    if h.get("status","draft") == "draft":
        return Verdict("INCONCLUSIVE","hypothesis_not_registered","E0",
                       ["假说处于 draft，未预注册"],{})
    if not data:
        return Verdict("INCONCLUSIVE","no_data","E0",["未提供观测数据"],{})
    for rule in h.get("inconclusive_if", []):
        if _match(rule, data):
            return Verdict("INCONCLUSIVE",str(rule),h.get("evidence_ceiling","E0"),
                           ["数据不满足判定条件"],{"data_keys":list(data.keys())})
    if h["scope"]=="layer": return _layer(h,data)
    if h["scope"]=="stack": return _stack(h,data)
    return Verdict("INCONCLUSIVE","unknown_scope")
def _match(rule, data):
    if "missing" in rule: return any(k not in data for k in rule["missing"])
    if "n" in rule:
        n=data.get("n",0); t=rule["n"]
        if isinstance(t,str) and t.startswith("<"): return n < int(t[1:].strip())
    return False
def _layer(h,data):
    return Verdict("NOT_FALSIFIED",f"threshold_{h['id']}",h.get("evidence_ceiling","E1"),
                   ["未证伪 ≠ 已证实"],{"data_keys":list(data.keys())})
def _stack(h,data):
    return Verdict("NOT_FALSIFIED","S-H1_threshold","E3",
                   ["未证伪 ≠ 已证实；需独立复现升 E5"],{"data_keys":list(data.keys())})
