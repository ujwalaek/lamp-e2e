#!/usr/bin/env bash
# Sweep LAMP's criticality threshold theta on a robomimic task (demos and poses must already exist:
# run run_task.sh first). For each theta, saves RCR counts, ground-truth match and monitor rates.
#   usage: sweep.sh Square|ToolHang "1.0 0.9 0.7 0.5 0.3"
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PY:-$HERE/../venv/bin/python}"
export PYTHONWARNINGS=ignore
D="$1"; THETAS="${2:-1.0 0.9 0.7 0.5 0.3}"
OUT="$HERE/out/$D"; MISC="$HERE/../lamp/Data/$D/misc"
for t in $THETAS; do
  export LAMP_THETA_GRIP="$t" LAMP_THETA_OBJ="$t"
  S="$OUT/sweep/theta_$t"; mkdir -p "$S"
  echo "===== $D theta=$t ($(date +%T))"
  "$PY" "$HERE/learn_rcrs.py" --domain "$D" -n env1 > "$S/learn_rcrs.log" 2>&1 || { echo "learn_rcrs failed"; continue; }
  timeout 3000 "$PY" "$HERE/learn_model.py" --domain "$D" > "$S/learn_model.log" 2>&1 || { echo "learn_model failed/timeout"; tail -3 "$S/learn_model.log"; continue; }
  for e in env9 env8; do
    timeout 3000 "$PY" "$HERE/predict.py" --domain "$D" --train_envs env1 --test_env "$e" --quiet > "$S/predict_$e.log" 2>&1 || echo "predict $e failed"
  done
  "$PY" "$HERE/robomimic/evaluate.py" --domain "$D" --envs env9 > "$S/evaluate.log" 2>&1 || echo "evaluate failed"
  cp "$MISC/rcr_summary.json" "$OUT"/monitor_env9.json "$OUT"/monitor_env8.json "$OUT"/gt_eval.json "$OUT"/abstract_demos.txt "$S"/ 2>/dev/null
  cp "$HERE/../lamp/Domains/$D/domain.pddl" "$S"/ 2>/dev/null
  grep -E "RCR\(s\)" "$S/learn_rcrs.log"; grep -E "lifted actions" "$S/learn_model.log"
  grep -E "^  (nominal|drop|miss)" "$S/predict_env9.log" "$S/predict_env8.log" | sed 's/.*log://'
done
"$PY" "$HERE/robomimic/summarize_sweep.py" "$OUT/sweep"
