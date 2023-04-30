cd $(dirname $0)/..
jq -s add `find datasets/*/data/ -name "*.json" | sort` | jq -n -c --stream 'fromstream(1|truncate_stream(inputs)) | {instruction:.instruction, input:.input, output:.output}' > data.jsonl
jq -s add `find datasets/*/data/ datasets-cc-by-sa/*/data/ -name "*.json" | sort` | jq -n -c --stream 'fromstream(1|truncate_stream(inputs)) | {instruction:.instruction, input:.input, output:.output}' > data-cc-by-sa.jsonl
wc -l data.jsonl
wc -l data-cc-by-sa.jsonl
