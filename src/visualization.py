"""Visualization module for data analysis."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from typing import Optional
from config import FIGURE_SIZE, MAX_FEATURES_DISPLAY


def plot_missing_values(df: pd.DataFrame) -> Optional[plt.Figure]:
    """Plot a bar chart of missing value counts per column.

    Args:
        df: Input DataFrame.

    Returns:
        matplotlib Figure or None if no missing values.
    """
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if missing.empty:
        return None

    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    missing.plot(kind="bar", ax=ax, color="#E74C3C")
    ax.set_title("Missing Value Counts by Column", fontsize=14, fontweight="bold")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Count")
    plt.tight_layout()
    return fig


def plot_numeric_distributions(df: pd.DataFrame) -> Optional[plt.Figure]:
    """Plot histograms for all numeric columns in a subplot grid.

    Args:
        df: Input DataFrame.

    Returns:
        matplotlib Figure or None if no numeric columns.
    """
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    if len(numeric_cols) == 0:
        return None

    n_cols: int = min(3, len(numeric_cols))
    n_rows: int = int(np.ceil(len(numeric_cols) / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 4))
    axes = np.atleast_1d(axes).flatten()

    for i, col in enumerate(numeric_cols):
        df[col].dropna().hist(ax=axes[i], bins=30, color="#3498DB", edgecolor="white")
        axes[i].set_title(f"Distribution of {col}", fontsize=11)
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("Frequency")

    for j in range(len(numeric_cols), len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    return fig


def plot_correlation_heatmap(df: pd.DataFrame) -> Optional[plt.Figure]:
    """Plot a correlation heatmap for numeric columns.

    Args:
        df: Input DataFrame.

    Returns:
        matplotlib Figure or None if fewer than 2 numeric columns.
    """
    numeric_df = df.select_dtypes(include=["int64", "float64"])
    if numeric_df.shape[1] < 2:
        return None

    corr = numeric_df.corr()
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap="RdBu_r",
        center=0, square=True, linewidths=0.5, ax=ax,
        vmin=-1, vmax=1
    )
    ax.set_title("Correlation Heatmap", fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig


def plot_boxplots(df: pd.DataFrame) -> Optional[plt.Figure]:
    """Plot boxplots for all numeric columns.

    Args:
        df: Input DataFrame.

    Returns:
        matplotlib Figure or None if no numeric columns.
    """
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    if len(numeric_cols) == 0:
        return None

    n_cols: int = min(3, len(numeric_cols))
    n_rows: int = int(np.ceil(len(numeric_cols) / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 4))
    axes = np.atleast_1d(axes).flatten()

    for i, col in enumerate(numeric_cols):
        axes[i].boxplot(
            df[col].dropna().values, vert=True, patch_artist=True,
            boxprops=dict(facecolor="#3498DB"),
            medianprops=dict(color="red")
        )
        axes[i].set_title(f"Boxplot of {col}", fontsize=11)
        axes[i].set_ylabel(col)

    for j in range(len(numeric_cols), len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    return fig


def plot_feature_importance(
    feature_names: list[str],
    importance_scores: np.ndarray,
    model_name: str,
) -> plt.Figure:
    """Plot feature importance for a trained model.

    Args:
        feature_names: List of feature names.
        importance_scores: Array of importance values.
        model_name: Name of the model (for the title).

    Returns:
        matplotlib Figure.
    """
    sorted_idx = np.argsort(importance_scores)[-MAX_FEATURES_DISPLAY:]
    names = [feature_names[i] for i in sorted_idx]
    scores = importance_scores[sorted_idx]

    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    ax.barh(names, scores, color="#2ECC71")
    ax.set_title(f"Feature Importance — {model_name}", fontsize=14, fontweight="bold")
    ax.set_xlabel("Importance")
    plt.tight_layout()
    return fig
