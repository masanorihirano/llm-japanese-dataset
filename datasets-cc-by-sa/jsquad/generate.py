import json
import itertools
from typing import Dict, List, Tuple, Union

import pandas as pd


def filter_answers(lst_examples: List[Dict[str, str]]) -> List[Dict[str, str]]:
    # 包含関係があれば一番長いもの
    # 包含関係がなければ必ず選択
    # 短い順に
    order_idx: List[int] = sorted(range(len(lst_examples)), key=lambda x: len(lst_examples[x]["output"]))
    lst_filtered: List[Dict[str, str]] = []
    for i in range(len(lst_examples)):
        idx: int = order_idx[i]
        left_output: List[str] = [lst_examples[j]["output"] for j in order_idx[i+1:]]
        example: Dict[str, str] = lst_examples[idx]
        if all([(example["output"] not in o) for o in left_output]):
            lst_filtered.append(example)
    return lst_filtered


def extract_instructs(
    example: Dict[str, Union[str, List[Dict[str, Union[int, str]]]]]
) -> List[Dict[str, str]]:
    # context: str = example["context"].split("[SEP]")[1].lstrip()
    context: str = "：".join(map(lambda x: x.strip(), example["context"].split("[SEP]")))
    available_instructs: List[List[Dict[str, str]]] = [
        [
            {
                "instruction": qa["question"],
                "input": context,
                "output": qa["answers"][i]["text"],
                "id": qa["id"],
            }
            for i in range(len(qa["answers"]))
        ]
        for qa in example["qas"]
    ]
    instructs: List[Dict[str, str]] = list(
        itertools.chain.from_iterable(map(filter_answers, available_instructs))
    )
    instructs = list(filter(lambda x: len(x["input"]) >= 30, instructs))
    return instructs


def read_json(filename: str) -> List[Dict[str, str]]:
    with open(filename, "r") as f:
        loaded_data: List[
            Dict[
                str,  # title, paragraphs
                Union[
                    str,
                    List[
                        Dict[
                            str,  # qas, context
                            Union[
                                str,
                                List[
                                    Dict[
                                        str,  # question, id, answers, is_impossible
                                        Union[int, str],  # answer_start  # text
                                    ]
                                ],
                            ],
                        ]
                    ],
                ],
            ]
        ] = json.load(f)["data"]
    # d: Dict[str, Union[str, List[Dict[str, Union[int, str]]]]]
    data: List[Dict[str, str]] = list(
        itertools.chain.from_iterable(
            [extract_instructs(d) for dct in loaded_data for d in dct["paragraphs"]]
        )
    )
    return data


def add_index(row: Tuple[int, Dict[str, str]]) -> Dict[str, str]:
    index: int = row[0]
    example: Dict[str, str] = row[1]
    example["index"] = str(index)
    return example

def fix_data(example: Dict[str, str]) -> Dict[str, str]:
    if example["id"] == "a1000888p0q2" and example["instruction"].startswith("たに語"):
        example["instruction"] = "新" + example["instruction"]
    return example


def main() -> None:
    train_data: List[Dict[str, str]] = read_json("train.json")
    valid_data: List[Dict[str, str]] = read_json("valid.json")
    concat_data: List[Dict[str, str]] = train_data + valid_data
    concat_data = list(map(add_index, enumerate(concat_data)))
    concat_data = list(map(fix_data, concat_data))
    pd.DataFrame(concat_data).to_json(
        "data.jsonl", orient="records", force_ascii=False, lines=True
    )


if __name__ == "__main__":
    main()
