import pandas as pd
import json
import os.path

URL = "https://jaqket.s3.ap-northeast-1.amazonaws.com/data/aio_02/aio_02_train.jsonl"
URL2 = "https://jaqket.s3.ap-northeast-1.amazonaws.com/data/aio_02/aio_02_dev_v1.0.jsonl"

file_dir = os.path.dirname(__file__)

df = pd.read_json(URL, lines=True)
df2 = pd.read_json(URL2, lines=True)

df = pd.concat([df, df2]).astype(str)
df = df.rename(columns={"original_question": "instruction", "original_answer": "output"})
df["input"] = ""
df = df[["instruction", "input", "output"]]
df["id"] = "F" + df.index.astype(str)

data_list = df.to_dict(orient="records")
forward_n = len(data_list) // 1000 + 1
for i in range(forward_n):
    file_name = os.path.join(file_dir, "data", f"{i:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )

df["instruction2"] = df["output"] + "について説明してください。"
df["output2"] = df["instruction"]
df = df[["instruction2", "input", "output2"]].rename(columns={"instruction2": "instruction", "output2": "output"})

def remove_fn(sentence: str) -> str:
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "０", "１", "２", "３", "４", "５", "６", "７", "８", "９"]
    if len(set(sentence) & set(nums)) > 0:
        return ""
    return sentence

def replace_fn(sentence: str) -> str:
    sentence = sentence.replace("?", "？")
    if not sentence.endswith("？"):
        sentence += "？"
    if "ですが" in sentence:
        return ""
    if "いくつでしょう" in sentence:
        return ""
    if "対して何" in sentence:
        return ""
    if "と誰" in sentence:
        return ""
    if "と何" in sentence:
        return ""
    if "の他に誰" in sentence:
        return ""
    if "の他に何" in sentence:
        return ""
    if "といえば、どんな" in sentence:
        return ""
    if "ますが、" in sentence:
        return ""
    if "とどこ" in sentence:
        return ""
    if "といえば" in sentence:
        return ""
    if sentence.endswith("を、ニューヨークにあるホテルの名前から何合意というでしょう？"):
        return sentence[:-30] + "です。" # R421
    if sentence.endswith("を、スイスの精神医学者の名前を取って何テストというでしょう？"):
        return sentence[:-30] + "です。" # R85
    if sentence.endswith("を、昔、おしゃべりをしていた場所から何会議というでしょう？"):
        return sentence[:-29] + "のことです。" # R199
    if sentence.endswith("を、船乗りがよく使ったことから何パイプというでしょう？"):
        return sentence[:-27] + "です。" # R78
    if sentence.endswith("を、ある天気のように見えることから何というでしょう？"):
        return sentence[:-26] + "です。" # R158
    if sentence.endswith("を、ギリシャの数学者の名前をとって何というでしょう？"):
        return sentence[:-26] + "です。" # R171
    if sentence.endswith("を、飲み物に喩えて「何も一時」というでしょう？"):
        return sentence[:-23] + "です。" # R440
    if sentence.endswith("を、飲み物に喩えて「何も一時」というでしょう？"):
        return sentence[:-23] + "です。" # R248
    if sentence.endswith("を、ある国の名を取って何ティーというでしょう？"):
        return sentence[:-23] + "です。" # R16
    if sentence.endswith("を、太鼓の音に例えて「何舞い」というでしょう？"):
        return sentence[:-23] + "です。" # R264
    if sentence.endswith("を、ドイツの山の名をとって何というでしょう？"):
        return sentence[:-22] + "です。" # R182
    if sentence.endswith("を、原因となった麻薬から何というでしょう？"):
        return sentence[:-21] + "です。" # R57
    if sentence.endswith("を、ある島の名を使って何というでしょう？"):
        return sentence[:-20] + "です。" # R141
    if sentence.endswith("を、ある野菜を使って何というでしょう？"):
        return sentence[:-19] + "です。" # R269
    if sentence.endswith("を、両生類に喩えて何というでしょう？"):
        return sentence[:-18] + "です。" # R113
    if sentence.endswith("を、一般に「何ボケ」というでしょう？"):
        return sentence[:-18] + "です。" # R166
    if sentence.endswith("を、「何ポーカー」というでしょう？"):
        return sentence[:-17] + "です。" # R441
    if sentence.endswith("を、花札の役から何というでしょう？"):
        return sentence[:-17] + "です。" # R401
    if sentence.endswith("を特に「何梅雨」というでしょう？"):
        return sentence[:-16] + "です。" # R231
    if sentence.endswith("を、「何を奪う」というでしょう？"):
        return sentence[:-16] + "です。" # R472
    if sentence.endswith("して「何の世代」というでしょう？"):
        return sentence[:-16] + "です。" # R480
    if sentence.endswith("を「何ごなし」というでしょう？"):
        return sentence[:-15] + "です。" # R215
    if sentence.endswith("を図柄からなんというでしょう？"):
        return sentence[:-15] + "です。" # R393
    if sentence.endswith("を何ボクシングというでしょう？"):
        return sentence[:-15] + "です。" # R202
    if sentence.endswith("を特に何宇宙というでしょう？"):
        return sentence[:-14] + "です。" # R308
    if sentence.endswith("にあたるのは何時代でしょう？"):
        return sentence[:-14] + "にあたる時代です。" # R250
    if sentence.endswith("を特に何狩りというでしょう？"):
        return sentence[:-14] + "です。" # R236
    if sentence.endswith("を何錠というでしょう？"):
        return sentence[:-11] + "です。" # R203
    if sentence.endswith("を、漢字四文字で何というでしょう？"):
        return sentence[:-17] + "です。"
    if sentence.endswith("を、和製英語で何というでしょう？"):
        return sentence[:-16] + "を示す和製英語です。"
    if sentence.endswith("を、英語で何というでしょう？"):
        return sentence[:-14] + "です。"
    if sentence.endswith("といえば「何と何」でしょう？"):
        return sentence[:-14] + "です。"
    if sentence.endswith("を総称して何というでしょう？"):
        return sentence[:-14] + "の総称です。"
    if sentence.endswith("のは、何という湖でしょう？"):
        return sentence[:-13] + "湖です。"
    if sentence.endswith("を略して何というでしょう？"):
        return sentence[:-13] + "の略です。"
    if sentence.endswith("を英語で何というでしょう？"):
        return sentence[:-13] + "です。"
    if sentence.endswith("のことを何というでしょう？"):
        return sentence[:-13] + "のことです。"
    if sentence.endswith("を一般に何というでしょう？"):
        return sentence[:-13] + "です。"
    if sentence.endswith("を特に何というでしょう？"):
        return sentence[:-12] + "です。"
    if sentence.endswith("を俗に何というでしょう？"):
        return sentence[:-12] + "です。"
    if sentence.endswith("をなんと言うでしょう？"):
        return sentence[:-11] + "です。"
    if sentence.endswith("といったら何でしょう？"):
        return sentence[:-11] + "です。"
    if sentence.endswith("を何といったでしょう？"):
        return sentence[:-11] + "です。"
    if sentence.endswith("といえばどこでしょう？"):
        return sentence[:-11] + "です。"
    if sentence.endswith("海峡は何海峡でしょう？"):
        return sentence[:-11] + "海峡です。"
    if sentence.endswith("で何というでしょう？"):
        return sentence[:-10] + "です。"
    if sentence.endswith("を何というでしょう？"):
        return sentence[:-10] + "です。"
    if sentence.endswith("といえば何でしょう？"):
        return sentence[:-10] + "です。"
    if sentence.endswith("といえば誰でしょう？"):
        return sentence[:-10] + "です。"
    if sentence.endswith("は何海峡でしょう？"):
        return sentence[:-9] + "です。"
    if sentence.endswith("のは何でしょう？"):
        return sentence[:-8] + "ものです。"
    if sentence.endswith("は何教でしょう？"):
        return sentence[:-8] + "です。"
    if sentence.endswith("はどこでしょう？"):
        return sentence[:-8] + "です。"
    if sentence.endswith("は何でしょう？"):
        return sentence[:-7] + "です。"
    if sentence.endswith("は誰でしょう？"):
        return sentence[:-7] + "です。"
    if sentence.endswith("ものでしょう？"):
        return sentence[:-7] + "ものです。"
    if sentence.endswith("は誰？"):
        return sentence[:-3] + "です。"
    if sentence.endswith("は何？"):
        return sentence[:-3] + "です。"
    return sentence

df["instruction"] = df["instruction"].apply(remove_fn)
df["output"] = df["output"].apply(replace_fn)
df["id"] = "R" + df.index.astype(str)

drop_list = [
    0, 1, 2, 4, 6, 7, 14, 15, 17, 18, 19, 20, 22, 24, 25, 27, 28, 31, 32, 39, 40, 42,
    43, 44, 47, 49, 50, 55, 56, 58, 59, 61, 62, 69, 72, 73, 76, 79, 80, 81, 82, 83,
    87, 100, 102, 106, 114, 118, 119, 123, 138, 139, 140, 145, 151, 159, 161, 165,
    168, 169, 172, 175, 178, 185, 189, 190, 194, 200, 201, 204,
    214, 216, 220, 223, 228, 233, 239, 241, 246, 252, 254, 255, 259, 263, 280, 301, 317, 318, 322, 329, 330,
    333, 337, 341, 344, 347, 349, 351, 352, 354, 356, 359, 361, 373, 383, 388, 395, 424, 425, 447, 459, 461, 475, 487,
    488, 490, 502, 507, 509, 512, 
]
index_list = [i for i in range(len(df)) if i not in drop_list]
df = df.iloc[index_list]
df = df.query("output != '' & instruction != ''")

data_list = df.to_dict(orient="records")
reverse_n = len(data_list) // 1000 + 1
for i in range(reverse_n):
    file_name = os.path.join(file_dir, "data", f"{i + forward_n:0>6}.json")
    json.dump(
        data_list[i * 1000: min((i+1)*1000, len(data_list))],
        open(file_name, mode="w", encoding="utf-8"),
        indent=2, ensure_ascii=False
    )