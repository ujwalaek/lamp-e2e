#!/usr/bin/env bash
# Re-learn Square's LAMP model with the peg's 4-fold symmetry folded into its frame (coarse bins, theta 0.5).
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PY:-$HERE/../venv/bin/python}"
export PYTHONWARNINGS=ignore LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13 LAMP_THETA_GRIP=0.5 LAMP_THETA_OBJ=0.5 LAMP_PEG_SYMMETRY=1
OUT="$HERE/out/Square"
# keep the earlier (no-symmetry) durative results
if [ -d "$OUT/durative" ] && [ ! -d "$OUT/durative_coarse" ]; then
  [ -f "$OUT/durative/runs_cache.pkl" ] && mv "$OUT/durative/runs_cache.pkl" "$OUT/durative_runs_cache.pkl"
  mv "$OUT/durative" "$OUT/durative_coarse"
fi
"$PY" "$HERE/robomimic/convert.py" --task square --tool_frame | head -3
"$PY" "$HERE/extract_poses.py" --domain Square -n env1 env9 env8 > /dev/null 2>&1
"$PY" "$HERE/learn_rcrs.py" --domain Square -n env1 | grep -E "RCR\(s\)|thresholds"
"$PY" "$HERE/learn_model.py" --domain Square 2>&1 | grep -E "region bins|lifted actions"
"$PY" "$HERE/robomimic/describe_regions.py" Square
