"""Automated analysis report generation module."""

import pandas as pd
from typing import Any


def generate_report(df: pd.DataFrame, info: dict[str, Any], cleaning_log: dict[str, Any]) -> list[str]:
    """Generate a textual analysis report from data statistics and cleaning log.

    Args:
        df: Input DataFrame.
        info: Basic info dict from get_basic_info.
        cleaning_log: Cleaning log dict from auto_clean.

    Returns:
        List of report sentences.
    """
    rows: int = info["rows"]
    columns: int = info["columns"]
    duplicated_rows: int = info["duplicated_rows"]

    missing_values = info["missing_values"]
    total_missing: int = int(missing_values.sum())
    missing_columns = missing_values[missing_values > 0]

    data_types = info["data_types"]
    numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns
    object_columns = df.select_dtypes(include=["object"]).columns

    report: list[str] = []

    report.append(f"该数据集共有 {rows} 行、{columns} 列。")

    if duplicated_rows > 0:
        report.append(f"原始数据中存在 {duplicated_rows} 行重复记录，已自动去重。")
    else:
        report.append("数据中未发现重复行。")

    if total_missing > 0:
        report.append(f"原始数据中共存在 {total_missing} 个缺失值，已自动填充处理。")
        max_missing_col = missing_columns.idxmax()
        max_missing_count: int = int(missing_columns.max())
        report.append(
            f"缺失值最多的字段是 {max_missing_col}（{max_missing_count} 个缺失值）。"
        )
    else:
        report.append("数据中未发现缺失值，数据完整性较好。")

    if cleaning_log["outliers_replaced"] > 0:
        report.append(f"检测到 {cleaning_log['outliers_replaced']} 个异常值，已使用中位数替换。")
    else:
        report.append("未检测到数值异常值。")

    report.append(f"数据中包含 {len(numeric_columns)} 个数值型字段。")
    report.append(f"数据中包含 {len(object_columns)} 个文本或类别型字段。")

    if len(numeric_columns) > 0:
        report.append("数值型字段可用于后续的分布分析、相关性分析以及机器学习建模。")
    if len(object_columns) > 0:
        report.append("类别型字段可进行分组统计、频数分析或特征编码。")

    report.append(f"数据清洗后最终形状为 {cleaning_log['final_shape'][0]} 行 × {cleaning_log['final_shape'][1]} 列。")
    report.append("总体来看，该数据集已适合进行深入的数据探索和模型训练。")

    return report
