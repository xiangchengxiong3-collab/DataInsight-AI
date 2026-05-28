import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, f1_score, r2_score, mean_squared_error


def detect_task_type(y):
    """
    自动判断机器学习任务类型：
    - 文本/类别型目标列：分类任务
    - 数值型但类别数量较少：分类任务
    - 连续数值型目标列：回归任务
    """
    if not pd.api.types.is_numeric_dtype(y):
        return "classification"

    unique_count = y.nunique()

    if unique_count <= 10:
        return "classification"

    return "regression"


def prepare_data(df, target_column):
    """
    数据预处理：
    - 删除目标列为空的行
    - 分离特征 X 和目标 y
    - 删除无效特征列
    - 数值型字段用中位数填充
    - 类别型字段用众数填充
    - 类别型特征进行 One-Hot 编码
    """
    if target_column not in df.columns:
        raise ValueError("目标列不存在")

    data = df.copy()

    # 删除目标列为空的行
    data = data.dropna(subset=[target_column])

    if data.shape[0] < 5:
        raise ValueError("有效数据量太少，无法进行模型训练")

    X = data.drop(columns=[target_column])
    y = data[target_column]

    if X.shape[1] == 0:
        raise ValueError("没有可用于训练的特征列")

    # 删除全部为空的特征列
    X = X.dropna(axis=1, how="all")

    if X.shape[1] == 0:
        raise ValueError("清洗后没有可用于训练的特征列")

    numeric_cols = X.select_dtypes(include=["number"]).columns
    categorical_cols = X.select_dtypes(exclude=["number"]).columns

    # 数值型缺失值填充
    for col in numeric_cols:
        X[col] = X[col].fillna(X[col].median())

    # 类别型缺失值填充
    for col in categorical_cols:
        if X[col].mode().empty:
            X[col] = X[col].fillna("Unknown")
        else:
            X[col] = X[col].fillna(X[col].mode()[0])

    # 类别型特征 One-Hot 编码
    X = pd.get_dummies(X, drop_first=True)

    if X.shape[1] == 0:
        raise ValueError("编码后没有可用于训练的特征列")

    return X, y


def train_basic_model(df, target_column):
    """
    训练基础机器学习模型：
    - 分类任务：RandomForestClassifier
    - 回归任务：RandomForestRegressor
    """
    X, y = prepare_data(df, target_column)

    task_type = detect_task_type(y)

    if task_type == "classification":
        if not pd.api.types.is_numeric_dtype(y):
            encoder = LabelEncoder()
            y = encoder.fit_transform(y)

        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        return {
            "task_type": "分类任务",
            "model_name": "RandomForestClassifier",
            "accuracy": accuracy_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred, average="weighted", zero_division=0)
        }

    else:
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        return {
            "task_type": "回归任务",
            "model_name": "RandomForestRegressor",
            "r2_score": r2_score(y_test, y_pred),
            "rmse": rmse
        }