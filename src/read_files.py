import pandas as pd


def read_excel(file_path: str) -> list[dict]:
    df = pd.read_excel(file_path, index_col=0)
    result = df.to_dict(orient="records")

    return result
