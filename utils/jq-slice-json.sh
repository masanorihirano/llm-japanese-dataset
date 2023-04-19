#!/bin/bash
cat - | jq -n --stream 'fromstream(1|truncate_stream(inputs))' | bash $(dirname ${0})/jq-slice-jsonl.sh
