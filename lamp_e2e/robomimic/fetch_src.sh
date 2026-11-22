#!/usr/bin/env bash
# Fetch robosuite env sources (read-only reference) to learn the layout of obs/object.
set -euo pipefail
D="$(cd "$(dirname "$0")/../.." && pwd)/datasets/robosuite_src"; mkdir -p "$D"
for f in nut_assembly tool_hang; do
  curl -sSL --fail -o "$D/$f.py" "https://raw.githubusercontent.com/ARISE-Initiative/robosuite/v1.5.1/robosuite/environments/manipulation/$f.py"
done
ls -la "$D"
