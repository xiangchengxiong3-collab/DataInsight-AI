import matplotlib.pyplot as plt


def plot_missing_values(df):
    """
    绘制缺失值柱状图
    """
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if missing.empty:
        return None

    fig, ax = plt.subplots()
    missing.plot(kind="bar", ax=ax)
    ax.set_title("Missing Values")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Count")

    return fig


def plot_numeric_distribution(df):
    """
    绘制数值字段分布图
    """
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(numeric_cols) == 0:
        return None

    col = numeric_cols[0]

    fig, ax = plt.subplots()
    df[col].dropna().hist(ax=ax)
    ax.set_title(f"Distribution of {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("Frequency")

    return fig