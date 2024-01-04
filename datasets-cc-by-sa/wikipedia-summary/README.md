# Wikipedia Summary
## 作成方法
https://dumps.wikimedia.org/

```
wget https://dumps.wikimedia.org/jawiki/20240101/jawiki-20240101-pages-articles.xml.bz2
poetry run python -m wikiextractor.WikiExtractor jawiki-20240101-pages-articles.xml.bz2
poetry run python generate.py
```

## ライセンス
CC-BY-SA 3.0
