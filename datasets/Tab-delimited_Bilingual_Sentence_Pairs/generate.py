import os.path
import pandas as pd
from zipfile import ZipFile
import json

file_dir = os.path.dirname(__file__)

zip_file = ZipFile(os.path.join(file_dir, "jpn-eng.zip"), mode="r")
df = pd.read_csv(zip_file.open("jpn.txt"), sep="\t").reset_index(drop=True)
df.columns = ["en", "ja", "none1"]
df["instruction"] = "次の入力を日本語に翻訳してください。"
df["input"] = df["en"]
df["output"] = df["ja"]

data_list = df[["instruction", "input", "output"]].to_dict(orient="records")
forward_n = len(data_list) // 1000 + 1
for i in range(forward_n):
    file_name = os.path.join(file_dir, "data", f"{i:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )

df["instruction"] = "次の入力を英語に翻訳してください。"
df["input"] = df["ja"]
df["output"] = df["en"]

data_list = df[["instruction", "input", "output"]].to_dict(orient="records")
reverse_n = len(data_list) // 1000 + 1
for i in range(reverse_n):
    file_name = os.path.join(file_dir, "data", f"{i + forward_n:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )
