import gzip
import os.path
import json
import pandas as pd

file_dir = os.path.dirname(__file__)
fp = gzip.open(os.path.join(file_dir, "foodkb.dictionary.txt.gz"), "r")

data = "\n".join([line.decode("utf-8").strip() for line in fp.readlines()])
data = data.split("----------")
data = [[x for x in x.split("\n") if x != ""] for x in data if x.strip() != ""]
data_list = []
for i, x in enumerate(data):
    title = x[0].replace("【", "").replace("】", "")
    if x[1] == "[同義語]":
        if x[3] != "[材料]" or x[6] != "[調理法]" or x[8] != "[属性]":
            print(x)
            raise AssertionError
        other_titles = x[2].split(" ")
        ingreedients = [y.replace("<", "").replace(">", "").split(".")[0] for y in x[4].split(" ")]
        cooking_methods = [y.replace("<", "").replace(">", "").split(".")[0] for y in x[7].split(" ")]
        for _title in [title, *other_titles]:
            ingreedients_str = '\n'.join([' - ' + z for z in ingreedients])
            cooking_methods_str = '\n'.join([' - ' + z for z in cooking_methods])
            data_list.append({
                "instruction": f"{_title}の作り方を教えてください。",
                "input": "",
                "output": f"{_title}の作り方は以下の通りです。\n【材料】\n{ingreedients_str}\n【調理法】\n{cooking_methods_str}"})
    else:
        if x[1] != "[材料]" or x[4] != "[調理法]" or x[6] != "[属性]":
            print(x)
            raise AssertionError
        ingreedients = [y.replace("<", "").replace(">", "").split(".")[0] for y in x[2].split(" ")]
        cooking_methods = [y.replace("<", "").replace(">", "").split(".")[0] for y in x[5].split(" ")]
        ingreedients_str = '\n'.join([' - ' + z for z in ingreedients])
        cooking_methods_str = '\n'.join([' - ' + z for z in cooking_methods])
        data_list.append({
            "instruction": f"{title}の作り方を教えてください。",
            "input": "",
            "output": f"{title}の作り方は以下の通りです。\n【材料】\n{ingreedients_str}\n【調理法】\n{cooking_methods_str}"})
forward_n = len(data_list) // 1000 + 1
for i in range(forward_n):
    file_name = os.path.join(file_dir, "data", f"{i:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )
        