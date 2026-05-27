def get_basic_info(df):
    """
    获取数据集的基本信息
    """
    info = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum(),
        "data_types": df.dtypes,
        "duplicated_rows": df.duplicated().sum()
    }

    return info
