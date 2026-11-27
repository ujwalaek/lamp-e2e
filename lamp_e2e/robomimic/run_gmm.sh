#!/usr/bin/env bash
# Durative monitor with graded GMM-likelihood predicates (thresholds learned from normal training demos).
#   usage: run_gmm.sh square|tool_hang [tag-suffix]
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PY:-$HERE/../venv/bin/python}"
export PYTHONWARNINGS=ignore LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13
export LAMP_SCORE="${LAMP_SCORE:-gmm}" LAMP_DILATE="${LAMP_DILATE:-0}"
TASK="$1"; SUF="${2:-}"
case "$TASK" in square) D=Square; export LAMP_PEG_SYMMETRY=1; TAG="pegsym_${LAMP_SCORE}${SUF}" ;; tool_hang) D=ToolHang; TAG="coarse_${LAMP_SCORE}${SUF}" ;; esac
echo "===== $D $TAG ($(date +%T))"
DURATIVE_TAG="$TAG" "$PY" "$HERE/robomimic/eval_durative.py" --task "$TASK" 2>&1 | \
  grep -E "thresholds|false alarms|detected|^ +[0-9]+ +\(|labelled|Traceback|Error"
"$PY" "$HERE/robomimic/durative_report.py" "$D" "$TAG" > /dev/null
