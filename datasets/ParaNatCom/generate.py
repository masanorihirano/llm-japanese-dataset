import os.path
import pandas as pd
from zipfile import ZipFile
import json
import xml.etree.ElementTree as ET
from tqdm import tqdm

file_dir = os.path.dirname(__file__)

zip_file = ZipFile(os.path.join(file_dir, "ParaNatCom-20201127.zip"), mode="r")
file_list = zip_file.namelist()
article_prefix_list = [x.replace("ParaNatCom-20201127/articles/", "") for x in file_list if x.startswith("ParaNatCom-20201127/articles/") and not x.endswith("/")]
article_prefix_list.sort()
data_list = []
for article_prefix in tqdm(article_prefix_list):
    root = ET.parse(zip_file.open(f"ParaNatCom-20201127/articles/{article_prefix}")).getroot()
    abstract_en = root.find("MedlineCitation").find("Article").find("Abstract").find("AbstractText").text
    title_en = root.find("MedlineCitation").find("Article").find("ArticleTitle").text
    if title_en.endswith("."):
        title_en = title_en[:-1]
    doi = root.find("MedlineCitation").find("Article").find("ELocationID").text
    
    ja1_data = zip_file.open(f"ParaNatCom-20201127/abstracts-ja-1/{article_prefix}").readlines()
    title_ja1 = ja1_data[0].decode("utf-8").replace("\r", "").replace("\n", "")
    if title_ja1.endswith("："):
        title_ja1 = title_ja1[:-1]
    abstract_ja1 = "".join([x.decode("utf-8").replace("\r", "").replace("\n", "") for x in ja1_data[1:]])
    
    data_list.append({"instruction": "論文のアブストラクトからタイトルを作ってください。", "input": abstract_ja1, "output": title_ja1, "doi": doi, "task": "title-gen-ja1"})
    data_list.append({"instruction": "論文のタイトルからアブストラクトを想像して書いてください。", "input": title_ja1, "output": abstract_ja1, "doi": doi, "task": "abstract-gen-ja1"})
    
    if f"ParaNatCom-20201127/abstracts-ja-2/{article_prefix}" in file_list:
        ja2_data = zip_file.open(f"ParaNatCom-20201127/abstracts-ja-2/{article_prefix}").readlines()
        title_ja2 = ja2_data[0].decode("utf-8").replace("\r", "").replace("\n", "")
        if title_ja2.endswith(":"):
            title_ja2 = title_ja2[:-1]
        abstract_ja2 = "".join([x.decode("utf-8").replace("\r", "").replace("\n", "") for x in ja2_data[1:]])
        data_list.append({"instruction": "論文のアブストラクトからタイトルを作ってください。", "input": abstract_ja2, "output": title_ja2, "doi": doi, "task": "title-gen-ja2"})
        data_list.append({"instruction": "論文のタイトルからアブストラクトを想像して書いてください。", "input": title_ja2, "output": abstract_ja2, "doi": doi, "task": "abstract-gen-ja2"})
    
    if f"ParaNatCom-20201127/abstracts-ja-3/{article_prefix}" in file_list:
        ja3_data = zip_file.open(f"ParaNatCom-20201127/abstracts-ja-3/{article_prefix}").readlines()
        title_ja3 = ja3_data[0].decode("utf-8").replace("\r", "").replace("\n", "")
        if title_ja3.endswith(":"):
            title_ja3 = title_ja3[:-1]
        abstract_ja3 = "".join([x.decode("utf-8").replace("\r", "").replace("\n", "") for x in ja3_data[1:]])
        data_list.append({"instruction": "論文のアブストラクトからタイトルを作ってください。", "input": abstract_ja3, "output": title_ja3, "doi": doi, "task": "title-gen-ja3"})
        data_list.append({"instruction": "論文のタイトルからアブストラクトを想像して書いてください。", "input": title_ja3, "output": abstract_ja3, "doi": doi, "task": "abstract-gen-ja3"})

forward_n = len(data_list) // 1000 + 1
for i in range(forward_n):
    file_name = os.path.join(file_dir, "data", f"{i:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )
