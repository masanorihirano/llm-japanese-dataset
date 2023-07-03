import pandas as pd
import json
import os.path

file_dir = os.path.dirname(__file__)

df2 = pd.read_excel("T23-2020.1.7.xlsx")
df = pd.read_excel("T15-2020.1.7.xlsx")
df = pd.concat([df, df2]).astype(str)
print(df.columns)
df["instruction"] = "以下の日本語をやさしい日本語に言い換えてください。"
df["input"] = df["#日本語(原文)"]
df["output"] = df["#やさしい日本語"]
df["index"] = "Y" + df["ID"] 

data_list = df[["instruction", "input", "output", "index"]].to_dict(orient="records")
n_all = 0
forward_n = len(data_list) // 1000 + 1
for i in range(forward_n):
    file_name = os.path.join(file_dir, "data", f"{i + n_all:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )
