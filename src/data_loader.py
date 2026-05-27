import pandas as pd


def load_csv(file):
    """
    读取用户上传的 CSV 文件
    """
    df = pd.read_csv(file)
    return df
