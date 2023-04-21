# Wikipedia Summary
## 作成方法
https://dumps.wikimedia.org/

```
wget https://dumps.wikimedia.org/jawiki/20230401/jawiki-20230401-pages-articles.xml.bz2
poetry run python -m wikiextractor.WikiExtractor jawiki-20230401-pages-articles.xml.bz2
poetry run python generate.py
```

## ライセンス
CC-BY-SA 3.0
