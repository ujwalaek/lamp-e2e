#!/usr/bin/env bash
# List robomimic v1.5 proficient-human (ph) files for the given tasks, with sizes.
for t in "${@:-square tool_hang}"; do
  curl -s "https://huggingface.co/api/datasets/robomimic/robomimic_datasets/tree/main/v1.5/$t/ph" |
    python3 -c 'import json,sys; [print(f["path"], round(f["size"]/1e6,1), "MB") for f in json.load(sys.stdin)]'
done
