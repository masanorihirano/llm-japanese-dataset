import os.path
import pandas as pd
from zipfile import ZipFile
import json

file_dir = os.path.dirname(__file__)

zip_file = ZipFile(os.path.join(file_dir, "main.zip"), mode="r")
train_data = json.load(zip_file.open("JMRD-main/data/train.json"))
valid_data = json.load(zip_file.open("JMRD-main/data/valid.json"))
test_data = json.load(zip_file.open("JMRD-main/data/test.json"))
data = [*train_data, *valid_data, *test_data]
data_list = [{
    "instruction": f"{x['movie_title']}について教えてください。",
    "input": "",
    "output": (
        f'{x["movie_title"]}は，{x["knowledge"]["製作年度"]}に製作された映画で、監督は{x["knowledge"]["監督名"]}です。'
        f'{"、".join(x["knowledge"]["キャスト名"])}らが出演しています。あらすじは以下の通りです。\n'
        f'【あらすじ】\n{"".join(x["knowledge"]["あらすじ"])}'
    )
}for x in data]
data_list_dict = dict([(x["instruction"], x) for x in data_list])
data_list = list(data_list_dict.values())
forward_n = len(data_list) // 1000 + 1
for i in range(forward_n):
    file_name = os.path.join(file_dir, "data", f"{i:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )