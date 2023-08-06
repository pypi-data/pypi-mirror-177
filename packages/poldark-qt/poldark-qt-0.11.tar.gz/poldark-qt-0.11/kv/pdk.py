import pandas as pd


def pandas_kv(src: pd.DataFrame, index: str, key: str, value: str):
    return src.set_index(index).to_dict(orient="index")[key][value]
