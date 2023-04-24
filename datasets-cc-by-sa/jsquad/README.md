# JSQuAD
## 作成方法
https://github.com/yahoojapan/JGLUE から取得
```
curl https://raw.githubusercontent.com/yahoojapan/JGLUE/main/datasets/jsquad-v1.1/train-v1.1.json > train.json
curl https://raw.githubusercontent.com/yahoojapan/JGLUE/main/datasets/jsquad-v1.1/valid-v1.1.json > valid.json
python generate.py
cat data.jsonl | bash ../../utils/jq-slice-jsonl.sh
```
**注意：データセットにはほぼ同じ質問・ほぼ同じ答えのペアが含まれている**


## ライセンス
CC-BY-SA 4.0
