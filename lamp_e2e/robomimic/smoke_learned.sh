#!/usr/bin/env bash
# quick check of eval_learned.py on the current Square model (final settings), 15 demos per set
cd "$(dirname "$0")/../.."
export LAMP_COND_QS="0.9 0.8" PYTHONWARNINGS=ignore LAMP_GRASP=motion LAMP_DURATION_CHECK=1 LAMP_GRIP_BINS=10 LAMP_ANG_BINS=13 \
       LAMP_THETA_GRIP=0.5 LAMP_THETA_OBJ=0.5 LAMP_PEG_SYMMETRY=1
venv/bin/python lamp_e2e/robomimic/eval_learned.py --task square --tag smoke --mh --quick 10 2>&1 | grep -v -i warn
venv/bin/python lamp_e2e/robomimic/durative_summary.py Square smoke_q90 smoke_q80 2>&1 | grep -v -i warning
