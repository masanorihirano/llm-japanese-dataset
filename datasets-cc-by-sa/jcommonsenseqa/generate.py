from typing import Dict, List, Union

import pandas as pd


def generate_instruction(row: pd.Series) -> Dict[str, str]:
    instruction: Dict[str, str] = {
        "index": str(row["q_id"]),
        "instruction": row["question"],
        "input": "、".join([row[f"choice{i}"] for i in range(5)]),
        "output": row["choice{}".format(row["label"])],
    }
    return instruction


def main() -> None:
    df: pd.DataFrame = pd.read_json("data.jsonl", orient="records", lines=True)
    df_generated: pd.DataFrame = pd.DataFrame(
        [generate_instruction(row) for _, row in df.iterrows()]
    )
    df_generated.to_json(
        "generated_data.jsonl", orient="records", force_ascii=False, lines=True
    )


if __name__ == "__main__":
    main()
