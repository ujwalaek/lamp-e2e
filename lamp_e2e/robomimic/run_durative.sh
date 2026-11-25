#!/usr/bin/env bash
# Run the durative evaluation for a task with a list of region-widening values.
#   usage: run_durative.sh square|tool_hang "0 1" [extra-tag]
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PY:-$HERE/../venv/bin/python}"
export PYTHONWARNINGS=ignore LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13
TASK="$1"; KS="${2:-0 1}"; BASE="${3:-}"
case "$TASK" in square) D=Square; export LAMP_PEG_SYMMETRY=1; BASE="${BASE:-pegsym}" ;; tool_hang) D=ToolHang; BASE="${BASE:-coarse}" ;; esac
for k in $KS; do
  TAG="${BASE}_dilate${k}"
  echo "===== $D $TAG ($(date +%T))"
  LAMP_DILATE="$k" DURATIVE_TAG="$TAG" "$PY" "$HERE/robomimic/eval_durative.py" --task "$TASK" 2>&1 | \
    grep -E "self-test|false alarms|detected|^ +[0-9]+ +\(|data ready|labelled"
  "$PY" "$HERE/robomimic/durative_report.py" "$D" "$TAG" > /dev/null
done
