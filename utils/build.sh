cd $(dirname $0)/..
jq -s add `find datasets/*/data/ -name "*.json" | sort` > data.json
jq -s add `find datasets/*/data/ datasets-cc-by-sa/*/data/ -name "*.json" | sort` > data-cc-by-sa.json
echo "data.json:" `jq 'length' data.json`
echo "data-cc-by-sa.json:" `jq 'length' data-cc-by-sa.json`