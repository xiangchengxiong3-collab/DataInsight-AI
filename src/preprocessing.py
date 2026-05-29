"""Automated data preprocessing pipeline."""

import numpy as np
import pandas as pd
from typing import Any
from sklearn.preprocessing import StandardScaler
from config import IQR_FACTOR


def auto_clean(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Run a fully automated data cleaning pipeline.

    Steps: deduplicate -> handle outliers -> fill missing values
           -> standardize numeric features -> one-hot encode categorical features.

    Args:
        df: Raw input DataFrame.

    Returns:
        Tuple of (cleaned DataFrame, cleaning log dict).
    """
    log: dict[str, Any] = {}
    data = df.copy()

    # Step 1: Remove duplicates
    rows_before: int = data.shape[0]
    data = data.drop_duplicates()
    rows_after: int = data.shape[0]
    log["duplicates_removed"] = rows_before - rows_after

    # Identify column types
    numeric_cols = data.select_dtypes(include=["int64", "float64"]).columns
    categorical_cols = data.select_dtypes(exclude=["int64", "float64"]).columns

    # Step 2: Handle outliers (IQR method)
    outlier_count: int = 0
    for col in numeric_cols:
        Q1: float = float(data[col].quantile(0.25))
        Q3: float = float(data[col].quantile(0.75))
        IQR: float = Q3 - Q1
        lower: float = Q1 - IQR_FACTOR * IQR
        upper: float = Q3 + IQR_FACTOR * IQR
        mask = (data[col] < lower) | (data[col] > upper)
        outlier_count += mask.sum()
        median_val: float = float(data[col].median())
        data.loc[mask, col] = median_val
    log["outliers_replaced"] = int(outlier_count)

    # Step 3: Fill missing values
    missing_before: int = int(data.isnull().sum().sum())
    for col in numeric_cols:
        data[col] = data[col].fillna(data[col].median())
    for col in categorical_cols:
        if not data[col].mode().empty:
            data[col] = data[col].fillna(data[col].mode()[0])
        else:
            data[col] = data[col].fillna("Unknown")
    log["missing_values_filled"] = missing_before

    # Step 4: Standardize numeric features
    if len(numeric_cols) > 0:
        scaler = StandardScaler()
        data[numeric_cols] = scaler.fit_transform(data[numeric_cols])
    log["numeric_features_scaled"] = len(numeric_cols)

    # Step 5: One-hot encode categorical features
    if len(categorical_cols) > 0:
        data = pd.get_dummies(data, columns=list(categorical_cols), drop_first=True)
    log["categorical_features_encoded"] = len(categorical_cols)
    log["final_shape"] = data.shape

    return data, log
