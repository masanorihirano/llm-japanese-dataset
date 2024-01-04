import glob
from typing import List, Dict, Optional
import joblib
import os.path
import json
import re

file_dir = os.path.dirname(__file__)

files = sorted(glob.glob(os.path.join(file_dir, "text", "*", "*")))

def process_file(file_name):
    data: List[Dict] = []
    current_state = 0
    current_id: Optional[str] = None
    current_url: Optional[str] = None
    current_word: Optional[str] = None
    current_description: str = ""
    with open(file_name, mode="r", encoding="utf-8") as f:
        for line in f:
            if line.startswith('<doc id="'):
                if current_state != 0:
                    raise AssertionError
                current_state = 1
                parser = line.split('"')
                current_id = parser[1]
            else:
                if current_state == 1:
                    if current_word is None:
                        current_word = line.replace("\n", "")
                    else:
                        if line == "\n":
                            continue
                        else:
                            if line.endswith(".\n") or line == "</doc>\n":
                                if current_description != "" and "(曖昧さ回避)" not in current_word and not re.fullmatch(r"\s*", current_description):
                                    if current_id is None or current_word is None or current_description == "":
                                        print(current_id)
                                        print(current_word)
                                        print(current_description)
                                        raise AssertionError
                                    if current_description.endswith("\n"):
                                        current_description = current_description[:-1]
                                    data.append({"curid": current_id, "instruction": "入力されたワードを説明してください。", "input": current_word, "output": current_description})
                                current_id = None
                                current_word = None
                                current_description = ""
                                current_state = 0
                            else:
                                current_description += line
                else:
                    continue
    return data

results = joblib.Parallel(n_jobs=-1)(joblib.delayed(process_file)(file_name) for file_name in files)
data_list = sum(results, [])
n_data = len(data_list)
for i in range(n_data // 1000 + 1):
    file_name = os.path.join(file_dir, "data", f"{i:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, n_data)],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )
