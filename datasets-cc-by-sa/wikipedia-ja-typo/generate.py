import tarfile
import os.path
import json
import pandas as pd

file_dir = os.path.dirname(__file__)
tar_file = tarfile.open(os.path.join(file_dir, "JWTDv2.0.tar.gz"), "r")
file_names = [x.name for x in tar_file.getmembers() if x.isfile()]
dfs = []
for file_name in file_names:
    fp = tar_file.extractfile(file_name)
    _df = pd.read_json(fp, orient='records', lines=True)
    dfs.append(_df)
df = pd.concat(dfs)
df["instruction"] = "次の日本語には間違っている部分があります。その部分を直して、正しい日本語の文を出力してください。"
df["index"] = df.index.astype(str)
df["input"] = df["pre_text"]
df["output"] = df["post_text"]

data_list = df[["index", "instruction", "input", "output"]].to_dict(orient="records")
forward_n = len(data_list) // 1000 + 1
for i in range(forward_n):
    file_name = os.path.join(file_dir, "data", f"{i:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )
