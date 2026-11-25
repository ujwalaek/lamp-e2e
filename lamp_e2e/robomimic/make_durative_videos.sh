#!/usr/bin/env bash
# Stage-aware durative monitor videos (nominal = recorded human demo; drop/miss = physics rollouts).
#   usage: make_durative_videos.sh square|tool_hang ["nominal drop miss"] [demo] [tag]
set -uo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PY:-$HERE/../venv/bin/python}"
export PYTHONWARNINGS=ignore LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13 LAMP_DILATE=1
TASK="$1"; CASES="${2:-nominal drop miss}"
case "$TASK" in
  square)    export LAMP_PEG_SYMMETRY=1; DEMO="${3:-demo_5}";  TAG="${4:-pegsym_dilate1}"; SIZE=512 ;;
  tool_hang) DEMO="${3:-demo_36}"; TAG="${4:-coarse_dilate1}"; SIZE=640 ;;
esac
OUT="$HERE/out/videos/durative"; mkdir -p "$OUT"
for c in $CASES; do
  echo "== $TASK $DEMO $c ($(date +%T))"
  "$PY" "$HERE/robomimic/durative_video.py" --task "$TASK" --case "$c" --demo "$DEMO" --tag "$TAG" --size "$SIZE" \
      --out "$OUT/${TASK}_${c}${SUFFIX:-}.mp4" 2>&1 | grep -v -i warning | tail -2
done
