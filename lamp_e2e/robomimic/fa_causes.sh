#!/usr/bin/env bash
# first-firing rule on normal demos for the main ablation results
cd "$(dirname "$0")/../.."
for x in "Square learned_A5_low_theta_no_symmetry_q95" "ToolHang learned_A5_uniform_theta_0.3_q95" \
         "Square learned_A4_mixed_operators_q95"; do
  echo "### $x"
  venv/bin/python lamp_e2e/robomimic/why_missed_learned.py $x | awk '/first alarm/{f=1} /failure happens/{f=0} f'
done
