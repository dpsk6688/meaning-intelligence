import argparse, json
from .config import load_config
from .layers import reduce_load, select_direction, recursive_reflection
from .falsify import check_falsifier
def main():
    p = argparse.ArgumentParser(prog="mi")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("config").add_argument("--path", default="msi/config.json")
    r = sub.add_parser("reduce"); r.add_argument("--text", required=True)
    f = sub.add_parser("falsify"); f.add_argument("--id", required=True); f.add_argument("--data", default=None)
    s = sub.add_parser("select"); s.add_argument("--text", required=True)
    rf = sub.add_parser("reflect"); rf.add_argument("--text", required=True); rf.add_argument("--depth", type=int, default=1)
    a = p.parse_args()
    if a.cmd=="config": print(json.dumps(load_config(a.path), ensure_ascii=False, indent=2))
    elif a.cmd=="reduce": print(json.dumps(reduce_load(a.text), ensure_ascii=False, indent=2))
    elif a.cmd=="falsify":
        d = json.load(open(a.data, encoding="utf-8")) if a.data else None
        print(json.dumps(check_falsifier(a.id, d).__dict__, ensure_ascii=False, indent=2))
    elif a.cmd=="select": print(json.dumps(select_direction({"x":{"n":1}}, None), ensure_ascii=False))
    elif a.cmd=="reflect": print(json.dumps(recursive_reflection({"t":a.text}, max_depth=3, depth=a.depth), ensure_ascii=False))
    else: p.print_help()
if __name__=="__main__": main()
