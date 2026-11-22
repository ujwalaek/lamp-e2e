#!/usr/bin/env bash
# Download robomimic v1.5 proficient-human low-dim datasets (object poses, no images).
#   square    ~51 MB    tool_hang ~199 MB
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)/datasets/robomimic"
for t in "${@:-square tool_hang}"; do
  d="$ROOT/$t/ph"; mkdir -p "$d"
  f="$d/low_dim_v15.hdf5"
  if [ -s "$f" ]; then echo "exists: $f"; continue; fi
  curl -sSL --fail -o "$f.part" "https://huggingface.co/datasets/robomimic/robomimic_datasets/resolve/main/v1.5/$t/ph/low_dim_v15.hdf5"
  mv "$f.part" "$f"; ls -la "$f"
done
