# llm-japanese-dataset
LLM構築用の日本語データセット

DatasetはHugging Faceでも公開しています．

https://huggingface.co/datasets/izumi-lab/llm-japanese-dataset

## 問い合わせ等

 - データセットの追加申し出
 - 公開できないものの，CC-BY-SAで公開するモデルへのデータ組み込むが可能なデータの提供申し出

などを歓迎します．もし，ご相談等がございましたら，下記メールアドレスまでお知らせください．

izumi-llm@socsim.org

## フォルダー構成に関して
datasetsフォルダー内に，データの生成形式ごとにフォルダーを作成します．

各フォルダー内には，以下を含める必要があります．

 - `data/000000.json`: json形式のデータ．複数入れることができます．6桁の数字で，0から順に番号を振りますが，欠番は許容されます．この内容の詳細については下記で述べます
 - `README.md`: データの説明書です．作成方法や，ライセンスなどを記載してください．

それ以外については制約がありません．
## データ形式について
### json形式のデータ
 - jsonl形式ではなく，json形式とします．
 - 1ファイルのデータはおおよそ1Kを目安とします．1Kを超えるデータは，ナンバリングをして複数のJSONに分けることを推奨します．
 - jsonファイル内には，配列でDict形式で記載します．
   - 必須フィールド
     - `"instruction"`
     - `"input"`
     - `"output"`
   - 推奨フィールド
     - `"index"`: データセット内でのナンバリングを0から行います．なお，string形式にしてください．(e.g. `"1"`)
   - 準推奨フィールド
     - `"category"`: データセット内でも，カテゴリー分けしていると後で便利な場合があります．
  - 追加フィールドも許可します．

### README.mdのテンプレート
```
# {データセット名}
## 作成方法
{ここに作成方法を記述．どこかから取得したのであればその旨記載}

## ライセンス
{ここにライセンスを記載．あればURLを追加．}
```

### 組み込み可能なライセンスについて
原則として，再頒布可能なもののみを含むようにしてください．
そうでないものについては，組み込む前に要相談．

ただし，コピーレフトについては，許容しません．(作成したモデル自体もライセンス制約がついてしまうので)
また，商用不可も原則として不可

#### `datasets` に組み込み可能なライセンス
 - MIT License
 - BSD License (2-Cluse, 3-Cluse)
 - Apache License Version 2.0
 - CC-BY
 - Unlicense
 - スクレイピングにより取得したデータを加工したもの

#### `datasets-cc-by-sa` に組み込み可能なライセンス
 - CC-BY-SA
#### 組み込むか要検討なライセンス
 - 4-Clause BSD License (一般的でないため)
 
#### 組み込み不可能なライセンス
 - GNU GPL v2
 - GNU GPL v3
 - CC=BY-ND (改変不可なので含まないほうがよい)
 - CC-BY-NC (商用不可)
 - CC-BY-NC-SA (商用不可)
 - CC-BY-NC-ND (商用不可)
