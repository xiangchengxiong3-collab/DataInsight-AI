"""Multi-model comparison and training module."""

import numpy as np
import pandas as pd
from typing import Any
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, r2_score, mean_squared_error
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from xgboost import XGBClassifier, XGBRegressor

from src.preprocessing import auto_clean
from config import RANDOM_SEED, TEST_SIZE, N_ESTIMATORS


def detect_task_type(y: pd.Series) -> str:
    """Auto-detect ML task type from target column.

    Args:
        y: Target column.

    Returns:
        "classification" or "regression".
    """
    if not pd.api.types.is_numeric_dtype(y):
        return "classification"
    unique_count: int = y.nunique()
    if unique_count <= 10:
        return "classification"
    return "regression"


def _get_classification_models() -> list[tuple[str, Any]]:
    """Return a list of (name, model_instance) for classification."""
    return [
        ("Random Forest", RandomForestClassifier(n_estimators=N_ESTIMATORS, random_state=RANDOM_SEED)),
        ("XGBoost", XGBClassifier(n_estimators=N_ESTIMATORS, random_state=RANDOM_SEED, eval_metric="logloss", verbosity=0)),
        ("Logistic Regression", LogisticRegression(max_iter=2000, random_state=RANDOM_SEED)),
        ("SVM", SVC(kernel="rbf", random_state=RANDOM_SEED)),
        ("KNN", KNeighborsClassifier()),
        ("Gradient Boosting", GradientBoostingClassifier(n_estimators=N_ESTIMATORS, random_state=RANDOM_SEED)),
    ]


def _get_regression_models() -> list[tuple[str, Any]]:
    """Return a list of (name, model_instance) for regression."""
    return [
        ("Random Forest", RandomForestRegressor(n_estimators=N_ESTIMATORS, random_state=RANDOM_SEED)),
        ("XGBoost", XGBRegressor(n_estimators=N_ESTIMATORS, random_state=RANDOM_SEED, verbosity=0)),
        ("Linear Regression", LinearRegression()),
        ("SVR", SVR(kernel="rbf")),
        ("KNN", KNeighborsRegressor()),
        ("Gradient Boosting", GradientBoostingRegressor(n_estimators=N_ESTIMATORS, random_state=RANDOM_SEED)),
    ]


def _get_feature_importance(model: Any, feature_names: list[str]) -> np.ndarray:
    """Extract feature importance from a fitted model.

    Args:
        model: Fitted sklearn-compatible model.
        feature_names: List of feature names.

    Returns:
        Array of feature importance scores. Falls back to uniform weights if unavailable.
    """
    if hasattr(model, "feature_importances_"):
        return model.feature_importances_
    if hasattr(model, "coef_"):
        coef = model.coef_
        if coef.ndim > 1:
            coef = coef[0]
        return np.abs(coef)
    return np.ones(len(feature_names))


def compare_models(df: pd.DataFrame, target_column: str) -> dict[str, Any]:
    """Train and compare multiple ML models on the given dataset.

    Args:
        df: Input DataFrame.
        target_column: Name of the target column.

    Returns:
        dict with keys: task_type, results_df (DataFrame of comparison metrics),
        best_model_name, best_model, feature_names, feature_importance.
    """
    cleaned_df, _ = auto_clean(df)

    if target_column not in cleaned_df.columns:
        for col in cleaned_df.columns:
            if col.startswith(target_column):
                target_column = col
                break

    X = cleaned_df.drop(columns=[target_column])
    y = cleaned_df[target_column]
    task_type = detect_task_type(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED
    )

    results: list[dict] = []
    best_model = None
    best_score: float = -float("inf")
    best_model_name: str = ""

    if task_type == "classification":
        models = _get_classification_models()
        if not pd.api.types.is_numeric_dtype(y):
            y_train = LabelEncoder().fit_transform(y_train)
            y_test = LabelEncoder().fit_transform(y_test)

        for name, model in models:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
            results.append({"模型": name, "Accuracy": round(acc, 4), "F1-Score": round(f1, 4)})
            if f1 > best_score:
                best_score = f1
                best_model = model
                best_model_name = name
    else:
        models = _get_regression_models()
        for name, model in models:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            r2 = r2_score(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            results.append({"模型": name, "R²": round(r2, 4), "RMSE": round(rmse, 4)})
            if r2 > best_score:
                best_score = r2
                best_model = model
                best_model_name = name

    results_df = pd.DataFrame(results)
    feature_names = list(X.columns)
    importance = _get_feature_importance(best_model, feature_names)

    return {
        "task_type": "分类任务" if task_type == "classification" else "回归任务",
        "results_df": results_df,
        "best_model_name": best_model_name,
        "best_model": best_model,
        "feature_names": feature_names,
        "feature_importance": importance,
    }
