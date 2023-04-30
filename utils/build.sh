cd $(dirname $0)/..
jq -s add `find datasets/*/data/ -name "*.json" | sort` | jq -n --stream 'fromstream(1|truncate_stream(inputs)) | {instruction:.instruction, input:.input, output:.output}' | jq -s 'flatten' > data.json
jq -s add `find datasets/*/data/ datasets-cc-by-sa/*/data/ -name "*.json" | sort` | jq -n --stream 'fromstream(1|truncate_stream(inputs)) | {instruction:.instruction, input:.input, output:.output}' | jq -s 'flatten' > data-cc-by-sa.json
echo "data.json:" `jq '. | length' data.json`
echo "data-cc-by-sa.json:" `jq '. | length' data-cc-by-sa.json`
