#!/usr/bin/env bash
# Sanity checks before rendering videos: stored LAMP models match the intended sweep runs.
cd "$(dirname "$0")/../.."
for D in Square ToolHang; do
  echo "== $D"
  ls -la --time-style=+%H:%M lamp/Data/$D/misc/*_${D}_0.pkl 2>/dev/null || echo "  model pickle MISSING"
  echo -n "  current rcr: "; cat lamp/Data/$D/misc/rcr_summary.json; echo
done
echo -n "  sweep Square coarse 0.5: "; cat lamp_e2e/out/Square/sweep_coarse/theta_0.5/rcr_summary.json; echo
echo -n "  sweep ToolHang coarse 0.9: "; cat lamp_e2e/out/ToolHang/sweep_coarse/theta_0.9/rcr_summary.json; echo
echo "== Square held-out demos whose last state is inside each nut_peg region"
for c in "nut_peg_1[bins]" "nut_peg_2[bins]"; do
  venv/bin/python lamp_e2e/robomimic/end_state_check.py lamp_e2e/out/Square/predictions_env9.csv "$c" \
    datasets/robomimic/square/ph/low_dim_v15.hdf5
done
