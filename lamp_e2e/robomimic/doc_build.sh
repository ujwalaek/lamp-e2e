#!/usr/bin/env bash
# print the revision of a saved read_doc result, then build the ablation tab batch for it
F="$1"; TAB="$2"
cd "$(dirname "$0")/../.."
REV=$(venv/bin/python -c "import json,sys; J=json.load(open(sys.argv[1])); print(J.get('content', J)['revisionId'])" "$F")
echo "revision $REV"
venv/bin/python lamp_e2e/robomimic/doc_ablation_tab.py "$TAB" "$REV" > /tmp/ablation_batch.json
venv/bin/python -c "import json; J=json.load(open('/tmp/ablation_batch.json')); print(len(J['requests']), 'requests,', len(open('/tmp/ablation_batch.json').read()), 'chars')"
