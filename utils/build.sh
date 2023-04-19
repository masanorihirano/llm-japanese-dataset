cd $(dirname $0)/..
jq -s add `find datasets/*/data/ -name "*.json" | sort` > data.json