#!/usr/bin/env bash
# Run one representation variant end to end (convert -> poses -> theta sweep) and keep its results
# in out/<Domain>/sweep_<variant>/.
#   variants:  base      LAMP as-is (eef frame, 35 position bins, 61 angle bins)
#              toolframe gripper frame rotated 180 deg about x (avoids the rotation-vector flip at 180 deg)
#              coarse    toolframe + 10 position bins (~3 cm) for gripper pairs + 13 angle bins (~30 deg)
#   usage: run_variant.sh square|tool_hang base|toolframe|coarse "0.9 0.7 0.5"
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PY:-$HERE/../venv/bin/python}"
export PYTHONWARNINGS=ignore
TASK="$1"; V="$2"; THETAS="${3:-1.0 0.9 0.7 0.5 0.3}"
case "$TASK" in square) D=Square ;; tool_hang) D=ToolHang ;; esac
FLAGS=""
unset LAMP_GRIP_BINS LAMP_ANG_BINS
case "$V" in
  base) ;;
  toolframe) FLAGS="--tool_frame" ;;
  coarse) FLAGS="--tool_frame"; export LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13 ;;
esac
echo "##### $D variant=$V ($(date +%T))"
"$PY" "$HERE/robomimic/convert.py" --task "$TASK" $FLAGS | head -3
"$PY" "$HERE/extract_poses.py" --domain "$D" -n env1 env9 env8 > /dev/null 2>&1
bash "$HERE/robomimic/sweep.sh" "$D" "$THETAS"
rm -rf "$HERE/out/$D/sweep_$V"; mv "$HERE/out/$D/sweep" "$HERE/out/$D/sweep_$V"
