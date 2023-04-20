# JCommonsenseQA
## 作成方法
https://github.com/yahoojapan/JGLUE から取得
```
curl https://raw.githubusercontent.com/yahoojapan/JGLUE/main/datasets/jcommonsenseqa-v1.1/train-v1.1.json > data.jsonl
curl https://raw.githubusercontent.com/yahoojapan/JGLUE/main/datasets/jcommonsenseqa-v1.1/valid-v1.1.json >> data.jsonl
python generate.py
cat generated_data.jsonl | bash ../../utils/jq-slice-jsonl.sh
```

## ライセンス
CC-BY-SA 4.0
