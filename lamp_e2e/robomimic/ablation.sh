#!/usr/bin/env bash
# "Does the relative-pose method work by itself?"  Start from pure LAMP with the fully learned monitor
# (eval_learned.py: no hand-written stages, predicate names or task rules), then add one hand-made piece at a time.
#   usage: ablation.sh square|tool_hang [first_step]
# Each step re-learns LAMP's regions with that step's settings, then evaluates on the same test runs.
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PY:-$HERE/../venv/bin/python}"
export PYTHONWARNINGS=ignore LAMP_GRASP=motion LAMP_DURATION_CHECK=1 LAMP_COND_QS="0.98 0.95 0.9 0.8"
TASK="$1"; FIRST="${2:-0}"
D=$([ "$TASK" = square ] && echo Square || echo ToolHang)

# step name | settings added on top of LAMP's defaults (35 position bins, 61 angle bins, theta 1.0 for every pair)
if [ "$TASK" = square ]; then
  STEPS=(
    "A0_pure|"
    "A1_coarse_bins|LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13"
    "A2_theta|LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13 LAMP_THETA_GRIP=0.5 LAMP_THETA_OBJ=0.5"
    "A3_peg_symmetry|LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13 LAMP_THETA_GRIP=0.5 LAMP_THETA_OBJ=0.5 LAMP_PEG_SYMMETRY=1"
    "A4_mixed_operators|LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13 LAMP_THETA_GRIP=0.5 LAMP_THETA_OBJ=0.5 LAMP_PEG_SYMMETRY=1 LAMP_MH_TRAIN=1"
    # generic alternative to the symmetry fix: low theta so each of the 4 seatings can become its own region, and the
    # learned monitor's automatic region unions can combine them (no peg knowledge)
    "A5_low_theta_no_symmetry|LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13 LAMP_THETA_GRIP=0.2 LAMP_THETA_OBJ=0.2"
  )
  EXTRA="--mh"
else
  STEPS=(
    "A0_pure|"
    "A1_coarse_bins|LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13"
    "A2_theta|LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13 LAMP_THETA_GRIP=0.9 LAMP_THETA_OBJ=0.9"
    "A3_tool_frame|LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13 LAMP_THETA_GRIP=0.9 LAMP_THETA_OBJ=0.9 LAMP_TOOL_CANON=1"
    "A4_frame_tool_theta|LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13 LAMP_THETA_GRIP=0.9 LAMP_THETA_OBJ=0.9 LAMP_TOOL_CANON=1 LAMP_THETA_FRAME_TOOL=0.3"
    # generic check: the same low theta for EVERY pair, no tool-frame fix (is the per-pair tuning needed?)
    "A5_uniform_theta_0.3|LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13 LAMP_THETA_GRIP=0.3 LAMP_THETA_OBJ=0.3"
  )
  EXTRA=""
fi

TAGS=""
for i in "${!STEPS[@]}"; do
  NAME="${STEPS[$i]%%|*}"; SET="${STEPS[$i]#*|}"
  for q in 98 95 90 80; do TAGS="$TAGS learned_${NAME}_q$q"; done
  [ "$i" -lt "$FIRST" ] && continue
  echo "===== $D $NAME: ${SET:-LAMP defaults} ($(date +%T))"
  (
    unset LAMP_GRIP_BINS LAMP_ANG_BINS LAMP_THETA_GRIP LAMP_THETA_OBJ LAMP_THETA_FRAME_TOOL LAMP_PEG_SYMMETRY \
          LAMP_TOOL_CANON LAMP_MH_TRAIN
    for kv in $SET; do export "$kv"; done
    rm -f "$HERE/../lamp/Data/$D/misc/latest_prefix.txt"
    # re-learning with LAMP's fine default bins needs a lot of memory: one task at a time (lock shared by both runs)
    (
      flock 9
      "$PY" "$HERE/robomimic/convert.py" --task "$TASK" --tool_frame | grep -E "saved env1|added"
      "$PY" "$HERE/extract_poses.py" --domain "$D" -n env1 2>&1 | grep -E "Error|Killed|Traceback"
      "$PY" "$HERE/learn_rcrs.py" --domain "$D" -n env1 2>&1 | grep -E "RCR\(s\)|Error|Killed|Traceback"
      "$PY" "$HERE/learn_model.py" --domain "$D" 2>&1 | grep -E "lifted actions|Error|Killed"
    ) 9> /tmp/lamp_relearn.lock
    [ -f "$HERE/../lamp/Data/$D/misc/latest_prefix.txt" ] || { echo "!! re-learning failed for $NAME"; exit 0; }
    "$PY" "$HERE/robomimic/describe_regions.py" "$D" 2>&1 | grep -v -i warning
    "$PY" "$HERE/robomimic/eval_learned.py" --task "$TASK" --tag "learned_$NAME" $EXTRA 2>&1 \
        | grep -v -i warn
  )
done
echo "===== summary ($(date +%T))"
"$PY" "$HERE/robomimic/ablation_summary.py" "$D"
