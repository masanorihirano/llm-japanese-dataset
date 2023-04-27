import gzip
import os.path
import json
import pandas as pd

file_dir = os.path.dirname(__file__)
tar_file = gzip.open(os.path.join(file_dir, "examples.utf.gz"), "r")
df = pd.read_csv(tar_file, sep="\t", header=None)
df = df.rename(columns={0: "ja", 1: "en"})
df = df[df["ja"].apply(lambda x: "A: " in x)]
df["ja"] = df["ja"].apply(lambda x: x.replace("A: ", ""))
df["en"] = df["en"].apply(lambda x: x.split("#")[0])
df["instruction"] = "次の日本語を英語に翻訳してください。"
df["index"] = "F" + df.index.astype(str)
df["input"] = df["ja"]
df["output"] = df["en"]
data_list = df[["index", "instruction", "input", "output"]].to_dict(orient="records")
forward_n = len(data_list) // 1000 + 1
for i in range(forward_n):
    file_name = os.path.join(file_dir, "data", f"{i:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )
df["instruction"] = "次の英語を日本語に翻訳してください。"
df["index"] = "F" + df.index.astype(str)
df["input"] = df["en"]
df["output"] = df["ja"]
data_list = df[["index", "instruction", "input", "output"]].to_dict(orient="records")
reverse_n = len(data_list) // 1000 + 1
for i in range(reverse_n):
    file_name = os.path.join(file_dir, "data", f"{i + forward_n:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )
