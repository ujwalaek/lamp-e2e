#!/usr/bin/env bash
# Run the LAMP pipeline on a robomimic task.
#   usage: run_task.sh square|tool_hang [skip_convert]
# Thresholds/bins can be overridden via LAMP_THETA_GRIP, LAMP_THETA_OBJ, LAMP_GRIP_BINS (see domains.py).
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PY:-$HERE/../venv/bin/python}"
export PYTHONWARNINGS=ignore
TASK="$1"
case "$TASK" in square) D=Square ;; tool_hang) D=ToolHang ;; *) echo "unknown task $TASK"; exit 1 ;; esac
OUT="$HERE/out/$D"; mkdir -p "$OUT"
if [ "${2:-}" != "skip_convert" ]; then
  echo "== [1/5] convert robomimic -> LAMP demos"; "$PY" "$HERE/robomimic/convert.py" --task "$TASK"
  echo "== [2/5] relative poses";  "$PY" "$HERE/extract_poses.py" --domain "$D" -n env1 env9 env8 2>&1 | grep -v '%|' | grep -v 'example binned'
fi
echo "== [3/5] critical regions";   "$PY" "$HERE/learn_rcrs.py" --domain "$D" -n env1
echo "== [4/5] predicates + model"; "$PY" "$HERE/learn_model.py" --domain "$D" 2>&1 | grep -v 'it/s'
echo "== [5/5] predict + monitor"
"$PY" "$HERE/predict.py" --domain "$D" --train_envs env1 --test_env env9 --quiet 2>&1 | grep -v 'it/s\|generating clusters' | tee "$OUT/predict_env9_log.txt"
"$PY" "$HERE/predict.py" --domain "$D" --train_envs env1 --test_env env8 --quiet 2>&1 | grep -v 'it/s\|generating clusters' | tee "$OUT/predict_env8_log.txt"
