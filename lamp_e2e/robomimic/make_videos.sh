#!/usr/bin/env bash
# Render annotated rollout videos (nominal / drop / miss) for a robomimic task with LAMP's learned regions.
#   usage: make_videos.sh square|tool_hang ["nominal drop miss"] [demo]
# Uses the "coarse" representation (tool frame, 10 position bins, 13 angle bins), which must match the
# LAMP model currently stored in lamp/Data/<Domain>/misc (Square: coarse theta 0.5, ToolHang: coarse theta 0.9).
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PY:-$HERE/../venv/bin/python}"
export PYTHONWARNINGS=ignore LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13
TASK="$1"; CASES="${2:-nominal drop miss}"
case "$TASK" in
  square)    SWEEP=sweep_coarse/theta_0.5; FILE=square/ph/low_dim_v15.hdf5; SIZE=512 ;;
  tool_hang) SWEEP=sweep_coarse/theta_0.9; FILE=tool_hang/ph/low_dim_v15.hdf5; SIZE=640 ;;
esac
DEMO="${3:-$("$PY" - "$HOME/lamp_work/datasets/robomimic/$FILE" <<'EOF'
import sys, h5py
f = h5py.File(sys.argv[1], "r")
print(sorted([x.decode() for x in f["mask/valid"][:]], key=lambda s: int(s.split("_")[1]))[0])
EOF
)}"
OUT="$HERE/out/videos"; mkdir -p "$OUT"
for c in $CASES; do
  echo "== $TASK $DEMO $c ($(date +%T))"
  "$PY" "$HERE/robomimic/rollout_video.py" --task "$TASK" --case "$c" --demo "$DEMO" --tool_frame --size "$SIZE" \
      --gloss_sweep "$SWEEP" ${PUSH:+--push "$PUSH"} ${PUSH_STEPS:+--push_steps "$PUSH_STEPS"} \
      --out "$OUT/${TASK}_${c}${SUFFIX:-}.mp4" 2>&1 | grep -v -i warning | tail -2
done
