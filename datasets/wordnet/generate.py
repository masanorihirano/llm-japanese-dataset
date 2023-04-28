import os.path
import pandas as pd
import json
import gzip
from io import BytesIO
from urllib.request import urlopen

URL_WORDS = "https://github.com/bond-lab/wnja/releases/download/v1.1/wnjpn-ok.tab.gz"
URL_DEFINITION = "https://github.com/bond-lab/wnja/releases/download/v1.1/wnjpn-def.tab.gz"
URL_EXAMPLE = "https://github.com/bond-lab/wnja/releases/download/v1.1/wnjpn-exe.tab.gz"

file_dir = os.path.dirname(__file__)
io_word = BytesIO(urlopen(URL_WORDS).read())
fp_word = gzip.GzipFile(fileobj=io_word, mode='rb')
io_definition = BytesIO(urlopen(URL_DEFINITION).read())
fp_definition = gzip.GzipFile(fileobj=io_definition, mode='rb')
io_example = BytesIO(urlopen(URL_EXAMPLE).read())
fp_example = gzip.GzipFile(fileobj=io_example, mode='rb')

df_word = pd.read_csv(fp_word, sep="\t", header=None).rename(columns={0: "index", 1: "word", 2: "pos"})
df_definition = pd.read_csv(fp_definition, sep="\t", header=None).rename(columns={0: "index", 1: "sub_index", 2: "definition_en", 3: "definition_ja"})
df_example = pd.read_csv(fp_example, sep="\t", header=None).rename(columns={0: "index", 1: "sub_index", 2: "example_en", 3: "example_ja"})
df_definition_merged = pd.merge(df_word, df_definition, on="index", how="outer").dropna()
df_example_merged = pd.merge(df_word, df_example, on="index", how="outer").dropna()

df_definition_merged["instruction"] = "「" + df_definition_merged["word"] + "」" + "の意味を教えてください。"
df_definition_merged["input"] = ""
df_definition_merged["output"] = df_definition_merged["definition_ja"]

n_total = 0
data_list = df_definition_merged[["instruction", "input", "output"]].to_dict(orient="records")
forward_n = len(data_list) // 1000 + 1
for i in range(forward_n):
    file_name = os.path.join(file_dir, "data", f"{i + n_total:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )
n_total += forward_n


df_definition_merged["instruction"] = "次の文を日本語に翻訳してください。"
df_definition_merged["input"] = df_definition_merged["definition_en"]
df_definition_merged["output"] = df_definition_merged["definition_ja"]

data_list = df_definition_merged[["instruction", "input", "output"]].to_dict(orient="records")
forward_n = len(data_list) // 1000 + 1
for i in range(forward_n):
    file_name = os.path.join(file_dir, "data", f"{i + n_total:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )
n_total += forward_n


df_definition_merged["instruction"] = "次の文を英語に翻訳してください。"
df_definition_merged["input"] = df_definition_merged["definition_ja"]
df_definition_merged["output"] = df_definition_merged["definition_en"]

data_list = df_definition_merged[["instruction", "input", "output"]].to_dict(orient="records")
forward_n = len(data_list) // 1000 + 1
for i in range(forward_n):
    file_name = os.path.join(file_dir, "data", f"{i + n_total:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )
n_total += forward_n


# df_example_merged["instruction"] = "次の単語を使用した例文を作ってください。"
# df_example_merged["input"] = df_example_merged["word"]
# df_example_merged["output"] = df_example_merged["example_ja"]

# data_list = df_example_merged[["instruction", "input", "output"]].to_dict(orient="records")
# forward_n = len(data_list) // 1000 + 1
# for i in range(forward_n):
#     file_name = os.path.join(file_dir, "data", f"{i + n_total:0>6}.json")
#     json.dump(
#         data_list[i * 1000: min((i+1)*1000, len(data_list))],
#         open(file_name, mode="w", encoding="utf-8"),
#         indent=2, ensure_ascii=False
#     )
# n_total += forward_n

df_example_merged["instruction"] = "次の文を日本語に翻訳してください。"
df_example_merged["input"] = df_example_merged["example_en"]
df_example_merged["output"] = df_example_merged["example_ja"]

data_list = df_example_merged[["instruction", "input", "output"]].to_dict(orient="records")
forward_n = len(data_list) // 1000 + 1
for i in range(forward_n):
    file_name = os.path.join(file_dir, "data", f"{i + n_total:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )
n_total += forward_n

df_example_merged["instruction"] = "次の文を英語に翻訳してください。"
df_example_merged["input"] = df_example_merged["example_ja"]
df_example_merged["output"] = df_example_merged["example_en"]

data_list = df_example_merged[["instruction", "input", "output"]].to_dict(orient="records")
forward_n = len(data_list) // 1000 + 1
for i in range(forward_n):
    file_name = os.path.join(file_dir, "data", f"{i + n_total:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )
n_total += forward_n
