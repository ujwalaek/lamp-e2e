"""Why does the monitor miss injected failures? For a sweep result: goal signature, and whether the
'holding -> not holding' transition already exists in the learned model (i.e. it is 'normal')."""
import json
import os
import re
import sys

d = sys.argv[1]   # e.g. out/Square/sweep_coarse/theta_0.5
m9 = json.load(open(os.path.join(d, "monitor_env9.json")))
print("goal signature:", m9.get("_goal_signature"))
pddl = open(os.path.join(d, "domain.pddl")).read()
actions = re.split(r"\(:action ", pddl)[1:]
print("#actions:", len(actions))
n_release_like = 0
for a in actions:
    eff = a.split(":effect", 1)[1]
    pre = a.split(":effect", 1)[0]
    loses = re.findall(r"\(not \((gripper_\w+_[1-9]) ", eff)
    if loses:
        n_release_like += 1
print("actions whose effect removes a 'gripper near object' predicate:", n_release_like)
ab = open(os.path.join(d, "abstract_demos.txt")).read().split("--- abstract demo")[1:]
lens = [int(re.search(r"\((\d+) abstract states\)", x).group(1)) for x in ab]
print("distinct abstract training demos:", len(ab), " abstract states per demo: min %d max %d" % (min(lens), max(lens)))
