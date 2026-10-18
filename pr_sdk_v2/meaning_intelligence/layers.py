from typing import Any
def reduce_load(text: str) -> dict[str, Any]:
    """L1 减负：启发式文本压缩，非认知负荷测量。"""
    freq = {}
    for w in text.split(): freq[w] = freq.get(w, 0) + 1
    top = sorted(freq.items(), key=lambda x: -x[1])[:12]
    return {"type":"heuristic_demo","warning":"启发式结果，不可作为 L1-H1 证据",
            "nodes":[{"name":w,"freq":c} for w,c in top],"n_nodes":len(top)}
def render_experiential(nodes):
    return {"controls":len(nodes),"interactive":True,"limitations":"未做用户研究"}
def generate_meaning(nodes):
    b={"direction":[],"value":[],"boundary":[]}
    for i,n in enumerate(nodes): b[list(b)[i%3]].append(n)
    return {"buckets":b,"limitations":"启发式分桶"}
def assess_value(buckets):
    return {"scores":{k:{"evidence":"E1","n":len(v)} for k,v in buckets.items()},"limitations":"E 等级为占位"}
def select_direction(scores, user_preferences=None):
    if not user_preferences or "weights" not in user_preferences:
        return {"status":"inconclusive","rule":"missing_user_preferences.weights"}
    w=user_preferences["weights"]
    best=max(scores, key=lambda k: scores[k].get("n",0)*w.get(k,1))
    return {"selected":best,"limitations":"方向选择依赖显式偏好"}
def recursive_reflection(state, max_depth=3, depth=0):
    if depth>=max_depth: return {"status":"stopped","depth":depth,"reason":"max_depth_reached"}
    return {"status":"running","depth":depth+1,"state":state}
