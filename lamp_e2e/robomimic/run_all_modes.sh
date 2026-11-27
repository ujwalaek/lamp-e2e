#!/usr/bin/env bash
# Evaluate every monitor variant on one task with the same tolerance rule (max over normal demos, capped).
#   usage: run_all_modes.sh square|tool_hang [suffix]
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PY:-$HERE/../venv/bin/python}"
export LAMP_TOL_PCT=100
TASK="$1"; SUF="${2:-}"
case "$TASK" in square) D=Square; BASE=pegsym ;; tool_hang) D=ToolHang; BASE=coarse ;; esac
LAMP_SCORE=bins     LAMP_DILATE=0 bash "$HERE/robomimic/run_gmm.sh" "$TASK" "_d0${SUF}"
LAMP_SCORE=bins     LAMP_DILATE=1 bash "$HERE/robomimic/run_gmm.sh" "$TASK" "_d1${SUF}"
LAMP_SCORE=gmm      LAMP_DILATE=0 bash "$HERE/robomimic/run_gmm.sh" "$TASK" "${SUF}"
LAMP_SCORE=density  LAMP_DILATE=1 bash "$HERE/robomimic/run_gmm.sh" "$TASK" "${SUF}"
LAMP_SCORE=combined LAMP_DILATE=1 bash "$HERE/robomimic/run_gmm.sh" "$TASK" "${SUF}"
"$PY" "$HERE/robomimic/durative_summary.py" "$D" "${BASE}_bins_d0${SUF}" "${BASE}_bins_d1${SUF}" "${BASE}_gmm${SUF}" \
    "${BASE}_density${SUF}" "${BASE}_combined${SUF}" 2>&1 | grep -v -i warning
