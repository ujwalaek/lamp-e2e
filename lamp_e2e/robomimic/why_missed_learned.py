"""For a learned-monitor result: in which stage does each injected failure happen, which rules does that stage have,
and was the failure caught / caught only early / missed?  Also: which rule fires first on false alarms.
usage: why_missed_learned.py <Domain> <tag>"""
import collections
import json
import os
import sys

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", sys.argv[1])
J = json.load(open(os.path.join(base, "durative_" + sys.argv[2], "durative_eval.json")))
rules = collections.defaultdict(list)
for c in J["conditions"]:
    rules[c["stage"]].append("{} {}{}".format(c["kind"], "" if c["pol"] else "not ", c["pred"]))
print("rules per stage:")
for st, rs in rules.items():
    print("  {:<14} {}".format(st, "; ".join(rs)))
for case, rs in J["results"].items():
    if case == "nominal" or case.startswith("mh_"):
        first = collections.Counter()
        for r in rs:
            if r["success"] and r["violations"]:
                v = min(r["violations"], key=lambda v: v["frame"])
                first["{} | {} {}{} | {}".format(v["stage"], v["kind"], "" if v["pol"] else "not ", v["pred"],
                                                 v.get("cause", ""))] += 1
        if first:
            print("\n{}: first alarm on normal demos".format(case))
            for k, n in first.most_common(6):
                print("  {:>3}  {}".format(n, k))
        continue
    tally = collections.Counter()
    for r in rs:
        if r["success"] and case != "stall":
            continue
        ev = r["event"] or 0
        st = next((s for s, a, b in r["stages"] if a <= ev < b), r["stages"][-1][0])
        frames = [v["frame"] for v in r["violations"]]
        res = "caught" if any(f >= ev - 1 for f in frames) else ("early only" if frames else "missed")
        tally[(st, res)] += 1
    print("\n{}: failure happens in stage -> outcome".format(case))
    for (st, res), n in sorted(tally.items()):
        print("  {:<14} {:<10} {}".format(st, res, n))
