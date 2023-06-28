import tarfile
import os.path
import json
import pandas as pd

file_dir = os.path.dirname(__file__)
tar_file = tarfile.open(os.path.join(file_dir, "jqac20180625.tgz"), "r")
file_names = [x.name for x in tar_file.getmembers() if x.isfile() and x.name.endswith(".csv") and not x.name.startswith("jqac/.")]
dfs = []
for file_name in file_names:
    fp = tar_file.extractfile(file_name)
    df_ = pd.read_csv(fp, sep=",", header=0, encoding="utf-8").dropna(subset=["Question (What, Who, Where, Whose, How, Yes/No)", "Answer"])
    dfs.append(df_)
df = pd.concat(dfs, ignore_index=True, axis=0)
df["instruction"] = df["Question (What, Who, Where, Whose, How, Yes/No)"]
df["index"] = df.index.astype(str)
df["input"] = ""
df["output"] = df["Answer"]

data_list = df[["index", "instruction", "input", "output"]].to_dict(orient="records")
forward_n = len(data_list) // 1000 + 1
for i in range(forward_n):
    file_name = os.path.join(file_dir, "data", f"{i:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )
