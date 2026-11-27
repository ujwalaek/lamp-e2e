#!/usr/bin/env bash
# Final evaluation of all monitor versions with every improvement switched on:
#   motion-based grasp signal (LAMP re-learned with it), stage-duration check, all failure types,
#   and (Square) the 250 new multi-operator demos.
#   usage: final_eval.sh square|tool_hang [skip_relearn]
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PY:-$HERE/../venv/bin/python}"
export PYTHONWARNINGS=ignore LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13 LAMP_GRASP=motion LAMP_DURATION_CHECK=1 LAMP_TOL_PCT=100
export LAMP_AUTO_MAP=1
TASK="$1"
case "$TASK" in
  square)    D=Square; export LAMP_PEG_SYMMETRY=1; BASE=final; CASES="drop miss slip stall wrong_grasp wrong_peg"; EXTRA="--mh"
             export LAMP_THETA_GRIP=0.5 LAMP_THETA_OBJ=0.5 ;;
  tool_hang) D=ToolHang; BASE=final; CASES="drop miss slip stall wrong_grasp"; EXTRA=""
             export LAMP_THETA_GRIP=0.9 LAMP_THETA_OBJ=0.9 LAMP_TOOL_CANON=1 LAMP_THETA_FRAME_TOOL="${THETA_FT:-0.3}" ;;
esac
if [ "${2:-}" != "skip_relearn" ]; then
  echo "== re-learn $D LAMP model with the motion grasp signal ($(date +%T))"
  "$PY" "$HERE/robomimic/convert.py" --task "$TASK" --tool_frame | head -3
  "$PY" "$HERE/extract_poses.py" --domain "$D" -n env1 env9 env8 > /dev/null 2>&1
  "$PY" "$HERE/learn_rcrs.py" --domain "$D" -n env1 | grep -E "RCR\(s\)"
  "$PY" "$HERE/learn_model.py" --domain "$D" 2>&1 | grep -E "lifted actions"
  "$PY" "$HERE/robomimic/describe_regions.py" "$D"
fi
TAGS=""
for spec in "bins 0 bins_d0" "bins 1 bins_d1" "gmm 0 gmm" "density 1 density" "combined 1 combined"; do
  set -- $spec
  TAG="${BASE}_$3"; TAGS="$TAGS $TAG"
  echo "===== $D $TAG ($(date +%T))"
  LAMP_SCORE="$1" LAMP_DILATE="$2" DURATIVE_TAG="$TAG" "$PY" "$HERE/robomimic/eval_durative.py" --task "$TASK" \
      --cases "$CASES" $EXTRA 2>&1 | grep -E "multi-human|thresholds|false alarms|detected|labelled|Traceback|Error"
  "$PY" "$HERE/robomimic/durative_report.py" "$D" "$TAG" > /dev/null
done
"$PY" "$HERE/robomimic/durative_summary.py" "$D" $TAGS 2>&1 | grep -v -i warning
