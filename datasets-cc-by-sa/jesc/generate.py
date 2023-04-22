import tarfile
import os.path
import json
import pandas as pd

file_dir = os.path.dirname(__file__)
tar_file = tarfile.open(os.path.join(file_dir, "raw.tar.gz"), "r")
file_names = [x.name for x in tar_file.getmembers() if x.isfile()]
assert len(file_names) == 1
file_name = file_names[0]
fp = tar_file.extractfile(file_name)
df = pd.read_csv(fp, sep="\t", header=None)
df = df.rename(columns={0: "ja", 1: "en"})
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
df["index"] = "R" + df.index.astype(str)
df["input"] = df["ja"]
df["output"] = df["en"]

data_list = df[["index", "instruction", "input", "output"]].to_dict(orient="records")
reverse_n = len(data_list) // 1000 + 1
for i in range(reverse_n):
    file_name = os.path.join(file_dir, "data", f"{i + forward_n:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )


