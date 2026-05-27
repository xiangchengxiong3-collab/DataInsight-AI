def generate_basic_report(df, info):
    """
    根据数据基本信息生成自动分析结论
    """
    rows = info["rows"]
    columns = info["columns"]
    duplicated_rows = info["duplicated_rows"]

    missing_values = info["missing_values"]
    total_missing = missing_values.sum()
    missing_columns = missing_values[missing_values > 0]

    data_types = info["data_types"]
    numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns
    object_columns = df.select_dtypes(include=["object"]).columns

    report = []

    report.append(f"该数据集共有 {rows} 行、{columns} 列。")

    if duplicated_rows > 0:
        report.append(f"数据中存在 {duplicated_rows} 行重复记录，建议后续进行去重处理。")
    else:
        report.append("数据中未发现重复行。")

    if total_missing > 0:
        report.append(f"数据中共存在 {total_missing} 个缺失值。")

        max_missing_col = missing_columns.idxmax()
        max_missing_count = missing_columns.max()

        report.append(
            f"缺失值最多的字段是 {max_missing_col}，缺失数量为 {max_missing_count}。"
        )
        report.append("建议优先检查缺失值较多的字段，并根据业务含义选择删除、填充或单独标记。")
    else:
        report.append("数据中未发现缺失值，数据完整性较好。")

    report.append(f"数据中包含 {len(numeric_columns)} 个数值型字段。")
    report.append(f"数据中包含 {len(object_columns)} 个文本或类别型字段。")

    if len(numeric_columns) > 0:
        report.append("数值型字段可用于后续分布分析、相关性分析或机器学习建模。")

    if len(object_columns) > 0:
        report.append("类别型字段可用于分组统计、频数分析或特征编码。")

    report.append("总体来看，该数据集已经可以进行进一步的数据清洗、可视化分析和建模探索。")

    return report