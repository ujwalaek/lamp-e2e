#!/usr/bin/env bash
# End-to-end LAMP pipeline on a small synthetic Packing dataset.
#   demos -> relative poses -> RCRs -> predicates + action model -> predictions / monitoring
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PY="${PY:-$HERE/../venv/bin/python}"
export PYTHONWARNINGS=ignore

echo "== [1/5] generate demos";               "$PY" "$HERE/gen_demos.py" "$@"
echo "== [2/5] extract relative poses";       "$PY" "$HERE/extract_poses.py" 2>&1 | grep -v '%|'
echo "== [3/5] learn relational critical regions"; "$PY" "$HERE/learn_rcrs.py"
echo "== [4/5] learn predicates + PDDL model"; "$PY" "$HERE/learn_model.py" 2>&1 | grep -v 'it/s'
echo "== [5/5] predict predicates on test demos + monitor"
"$PY" "$HERE/predict.py" 2>&1 | grep -v 'it/s\|generating clusters' | tee "$HERE/out/predict_log.txt"
