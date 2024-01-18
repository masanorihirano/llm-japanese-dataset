import os.path
import pandas as pd
from zipfile import ZipFile
import json

file_dir = os.path.dirname(__file__)

zip_file = ZipFile(os.path.join(file_dir, "ALT-Parallel-Corpus-20191206.zip"), mode="r")
df_ja = pd.read_csv(zip_file.open("ALT-Parallel-Corpus-20191206/data_ja.txt"), sep="\t", header=None).reset_index(drop=True)
df_ja = df_ja.rename(columns={0: "index", 1: "ja"})
df_en = pd.read_csv(zip_file.open("ALT-Parallel-Corpus-20191206/data_en.txt"), sep="\t", header=None).reset_index(drop=True)
df_en = df_en.rename(columns={0: "index", 1: "en"})
df = pd.merge(df_ja, df_en, on="index")
df = df[(df["ja"].notnull()) & (df["en"].notnull())]
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
