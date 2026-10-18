from meaning_intelligence.falsify import check_falsifier
def t(name, got, expect):
    ok = got == expect
    print(f"[{'OK' if ok else 'FAIL'}] {name}: {got} (期望 {expect})")
    return ok
r = []
v = check_falsifier("S-H1", None); r.append(t("S-H1 draft", v.status, "INCONCLUSIVE")); r.append(t("S-H1 rule", v.rule, "hypothesis_not_registered"))
v = check_falsifier("L1-H1", None); r.append(t("L1-H1 无数据", v.status, "INCONCLUSIVE")); r.append(t("L1-H1 rule", v.rule, "no_data"))
v = check_falsifier("L1-H1", {"n":5}); r.append(t("L1-H1 样本不足", v.status, "INCONCLUSIVE"))
v = check_falsifier("L1-H1", {"n":100,"treatment_data":[1],"control_data":[2]}); r.append(t("L1-H1 正常", v.status, "NOT_FALSIFIED"))
print(f"\n{sum(r)}/{len(r)} 通过")
