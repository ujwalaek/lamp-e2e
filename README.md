# LAMP end-to-end pipeline (for execution monitoring)

A working Python 3 pipeline for [LAMP (arXiv:2402.11871)](https://arxiv.org/abs/2402.11871). It goes demos → relative poses →
relational critical regions → predicates + PDDL action model → per-state predicate prediction, plus a simple execution monitor.

- `lamp/`: the authors' repo [aair-lab/lamp](https://github.com/aair-lab/lamp) as a git submodule, pinned to `998428c` and not modified.
- `lamp_e2e/`: my scripts, which run LAMP's own learning code with a numpy stand-in for their OpenRAVE simulator.
  **See [lamp_e2e/README.md](lamp_e2e/README.md)** for the paper ↔ code ↔ script mapping, implementation details, results and caveats.
- `lamp_e2e/out/`: results from the reference run (seed 0).
- `lamp_e2e/robomimic/`: the same pipeline applied to **robomimic Square and Tool Hang**, using real human demos.
  **See [lamp_e2e/robomimic/README.md](lamp_e2e/robomimic/README.md)** for the results and what they mean for execution monitoring.

## Setup and run

```bash
git clone --recursive <this-repo-url> lamp_work && cd lamp_work
python3 -m venv venv && venv/bin/pip install numpy scipy scikit-learn tqdm networkx
# (if ensurepip is missing: python3 -m venv --without-pip venv &&
#  python3 -m pip --python venv/bin/python install numpy scipy scikit-learn tqdm networkx)
lamp_e2e/run_all.sh          # ~2 min on CPU
```
Generated data goes to `lamp/Data/Packing/misc/` and the learned domain to `lamp/Domains/Packing/domain.pddl`. Neither is committed.
