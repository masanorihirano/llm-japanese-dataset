from zipfile import ZipFile
import os.path
import json
import pandas as pd

file_dir = os.path.dirname(__file__)
zip_file = ZipFile(os.path.join(file_dir, "AozoraTxt_UTF8.zip"), mode="r")
data = []
for file_name in sorted([x for x in zip_file.namelist() if x.endswith(".txt")]):
    with zip_file.open(file_name, mode="r") as f:
        header_count = 0
        info = {"file_name": file_name.replace("AozoraTxt/person_utf8/", "")}
        for i, line in enumerate(f):
            line = line.decode("utf-8").replace("\u3000", "").replace(" ", "")
            if i == 0:
                info["title"] = line.replace("\n", "")
                continue
            if i == 1:
                info["author"] = line.replace("\n", "")
                continue
            if line == "-------------------------------------------------------\n":
                header_count += 1
            else:
                if header_count == 2:
                    if line == "\n" or line.startswith("［＃"):
                        continue
                    else:
                        info["text"] = line.replace("\n", "")[:100]
                        break
                else:
                    continue
        data.append(info)
df = pd.DataFrame.from_dict(data)
df["instruction"] = df["author"] + "の作品『" + df["title"] + "』の冒頭を教えてください。"
df["input"] = ""
df["output"] = "「" + df["text"] + "」です。"

data_list = df[["instruction", "input", "output"]].to_dict(orient="records")
n_data = len(data_list)
for i in range(n_data // 1000 + 1):
    file_name = os.path.join(file_dir, "data", f"{i:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, n_data)],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )

df["instruction"] = "「" + df["text"] + "」で始まる文学作品の作者とタイトルを教えてください。"
df["input"] = ""
df["output"] = df["author"] + "の『" + df["title"] + "』です。"

data_list = df[["instruction", "input", "output"]].to_dict(orient="records")
n_accumurate = n_data // 1000 + 1
n_data = len(data_list)
for i in range(n_data // 1000 + 1):
    file_name = os.path.join(file_dir, "data", f"{i + n_accumurate:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, n_data)],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )

