import tarfile
import os.path
import json
import pandas as pd

file_dir = os.path.dirname(__file__)
tar_file = tarfile.open(os.path.join(file_dir, "nikkaji-20180507.tar.gz"), "r")
file_names = [x.name for x in tar_file.getmembers() if x.isfile() and (x.name.endswith(".en") or x.name.endswith(".ja"))]
prefix = set([x.split(".")[0] for x in file_names])
data_list = []
for pre in prefix:
    ja_file_fp = tar_file.extractfile(pre + ".ja")
    en_file_fp = tar_file.extractfile(pre + ".en")
    df_ja = pd.read_csv(ja_file_fp, sep="\t", header=None)
    df_en = pd.read_csv(en_file_fp, sep="\t", header=None)
    df = pd.concat([df_ja.rename(columns={0: "ja"}), df_en.rename(columns={0: "en"})], axis=1)
    df["instruction"] = "次の化合物の英語名を日本語に翻訳してください。"
    df["index"] = pre + "_F" + df.index.astype(str)
    df["input"] = df["en"]
    df["output"] = df["ja"]
    data_list.extend(df[["index", "instruction", "input", "output"]].to_dict(orient="records"))
    df["instruction"] = "次の化合物の日本語名を英語にしてください。"
    df["index"] = pre + "_R" + df.index.astype(str)
    df["input"] = df["ja"]
    df["output"] = df["en"]
    data_list.extend(df[["index", "instruction", "input", "output"]].to_dict(orient="records"))
forward_n = len(data_list) // 1000 + 1
for i in range(forward_n):
    file_name = os.path.join(file_dir, "data", f"{i:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )