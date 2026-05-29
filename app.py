"""DataInsight-AI: AI-powered automated data analysis assistant."""

import streamlit as st
import pandas as pd

from src.data_loader import load_csv
from src.eda import get_basic_info
from src.preprocessing import auto_clean
from src.visualization import (
    plot_missing_values,
    plot_numeric_distributions,
    plot_correlation_heatmap,
    plot_boxplots,
    plot_feature_importance,
)
from src.report import generate_report
from src.modeling import compare_models

# ---------------------------------------------------------------------------
# Page config & custom CSS
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="DataInsight-AI",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* ── Global ── */
    .stApp { background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%); }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        padding-top: 2rem;
    }
    [data-testid="stSidebar"] * { color: #E2E8F0; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF;
    }
    [data-testid="stSidebar"] .stFileUploader label { color: #CBD5E1; }

    /* ── Metric cards ── */
    .metric-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
        border: 1px solid #E2E8F0;
        text-align: center;
        transition: transform 0.15s, box-shadow 0.15s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37,99,235,0.12);
    }
    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
        color: #2563EB;
        line-height: 1.2;
    }
    .metric-card .label {
        font-size: 0.8rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
    }

    /* ── Section container ── */
    .section-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.75rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        border: 1px solid #E2E8F0;
    }

    /* ── Headings ── */
    h1 { color: #0F172A; font-weight: 800; }
    h2 { color: #1E293B; font-weight: 700; margin-top: 0; }
    h3 { color: #334155; font-weight: 600; }

    /* ── Landing cards ── */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-top: 1.5rem;
    }
    .feature-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s;
    }
    .feature-card:hover {
        box-shadow: 0 4px 16px rgba(37,99,235,0.1);
        border-color: #93C5FD;
    }
    .feature-card .icon {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }
    .feature-card .title {
        font-weight: 700;
        font-size: 1rem;
        color: #1E293B;
        margin-bottom: 0.35rem;
    }
    .feature-card .desc {
        font-size: 0.85rem;
        color: #64748B;
        line-height: 1.5;
    }

    /* ── Status badges ── */
    .badge-success { color: #16A34A; }
    .badge-warn { color: #D97706; }
    .badge-info { color: #2563EB; }

    /* ── Cleaning log ── */
    .cleaning-tag {
        display: inline-block;
        background: #EFF6FF;
        color: #2563EB;
        border-radius: 20px;
        padding: 0.3rem 1rem;
        margin: 0.25rem;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* ── Buttons ── */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 2rem 0;">
        <div style="font-size: 1.6rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">
            DataInsight AI
        </div>
        <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 0.25rem;">
            Intelligent Data Analysis Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"],
        help="Upload a CSV file to begin analysis. Max 200MB.",
    )

    if uploaded_file is not None:
        st.markdown("---")
        st.markdown("### Navigation")
        st.markdown("1. Data Preview")
        st.markdown("2. Basic Information")
        st.markdown("3. Data Cleaning")
        st.markdown("4. Visualizations")
        st.markdown("5. Analysis Report")
        st.markdown("6. ML Modeling")

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem;color:#64748B;text-align:center;'>"
        "Built with Streamlit · Scikit-learn · XGBoost"
        "</div>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Main content
# ---------------------------------------------------------------------------

# ── Header ──
st.markdown("""
<div style="text-align:center; padding: 1rem 0 1rem 0;">
    <h1 style="font-size:2.4rem; margin-bottom:0.25rem;">DataInsight AI 2.0</h1>
    <p style="font-size:1.05rem; color:#64748B; margin:0;">
        Upload data &bull; Auto-clean &bull; Visualize &bull; Model
    </p>
</div>
""", unsafe_allow_html=True)

# ── Landing page ──
if uploaded_file is None:
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)

    features = [
        ("1", "Upload CSV", "Drag-and-drop any CSV file. We handle encoding, delimiters, and type inference automatically."),
        ("2", "Auto Clean", "Deduplication, outlier capping, missing value imputation, scaling, and encoding — all in one pass."),
        ("3", "Visualize", "Missing value charts, distribution histograms, boxplots, and correlation heatmaps in an interactive tab view."),
        ("4", "Analyze", "Get a human-readable analysis report summarizing your data's shape, quality, and readiness for modeling."),
        ("5", "Model", "One-click comparison of 6 ML models with automatic classification / regression detection and feature importance."),
    ]

    for icon, title, desc in features:
        st.markdown(f"""
        <div class="feature-card">
            <div class="icon">{ "📂" if icon == "1" else "🧹" if icon == "2" else "📊" if icon == "3" else "📝" if icon == "4" else "🤖" }</div>
            <div class="title">{icon}. {title}</div>
            <div class="desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ── File loaded ──
try:
    df = load_csv(uploaded_file)

    # ═══════════════════════════════════════════════════════════════════
    # 1. Data Preview
    # ═══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("## 1. Data Preview")
    st.caption(f"{df.shape[0]:,} rows &times; {df.shape[1]} columns loaded successfully")
    st.dataframe(df.head(10), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════
    # 2. Basic Information
    # ═══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("## 2. Basic Information")
    info = get_basic_info(df)

    total_missing = int(info["missing_values"].sum())

    st.markdown(f"""
    <div style="display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:1.5rem;">
        <div class="metric-card" style="flex:1; min-width:140px;">
            <div class="value">{info["rows"]:,}</div>
            <div class="label">Rows</div>
        </div>
        <div class="metric-card" style="flex:1; min-width:140px;">
            <div class="value">{info["columns"]}</div>
            <div class="label">Columns</div>
        </div>
        <div class="metric-card" style="flex:1; min-width:140px;">
            <div class="value">{info["duplicated_rows"]:,}</div>
            <div class="label">Duplicates</div>
        </div>
        <div class="metric-card" style="flex:1; min-width:140px;">
            <div class="value">{total_missing:,}</div>
            <div class="label">Missing</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_names, tab_types = st.tabs(["Column Names", "Data Types"])

    with tab_names:
        cols_per_row = 4
        names = info["column_names"]
        for i in range(0, len(names), cols_per_row):
            batch = names[i:i + cols_per_row]
            st.markdown(" ".join(
                f'<span class="cleaning-tag">{name}</span>'
                for name in batch
            ), unsafe_allow_html=True)

    with tab_types:
        types_df = info["data_types"].astype(str).reset_index()
        types_df.columns = ["Column", "Type"]
        # Make types look nicer
        types_df["Type"] = types_df["Type"].replace({
            "int64": "Integer", "float64": "Float",
            "object": "Text/Category", "bool": "Boolean"
        })
        st.dataframe(types_df, use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════
    # 3. Data Cleaning
    # ═══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("## 3. Automated Data Cleaning")

    with st.spinner("Cleaning data..."):
        cleaned_df, cleaning_log = auto_clean(df)

    dup = cleaning_log["duplicates_removed"]
    out = cleaning_log["outliers_replaced"]
    miss = cleaning_log["missing_values_filled"]

    st.markdown(f"""
    <div style="display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:1rem;">
        <div class="metric-card" style="flex:1; min-width:140px;">
            <div class="value">{dup:,}</div>
            <div class="label">Duplicates Removed</div>
        </div>
        <div class="metric-card" style="flex:1; min-width:140px;">
            <div class="value">{out:,}</div>
            <div class="label">Outliers Replaced</div>
        </div>
        <div class="metric-card" style="flex:1; min-width:140px;">
            <div class="value">{miss:,}</div>
            <div class="label">Missing Filled</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        f"Cleaned dimensions: "
        f"**{cleaning_log['final_shape'][0]:,} rows** &times; "
        f"**{cleaning_log['final_shape'][1]} columns** &nbsp;|&nbsp; "
        f"Scaled **{cleaning_log['numeric_features_scaled']}** numeric features &nbsp;|&nbsp; "
        f"Encoded **{cleaning_log['categorical_features_encoded']}** categorical features"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════
    # 4. Visualizations
    # ═══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("## 4. Data Visualizations")

    viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs([
        "Missing Values", "Distributions", "Boxplots", "Correlation Heatmap"
    ])

    with viz_tab1:
        missing_fig = plot_missing_values(df)
        if missing_fig:
            st.pyplot(missing_fig)
        else:
            st.info("No missing values detected — your data is complete.")

    with viz_tab2:
        dist_fig = plot_numeric_distributions(df)
        if dist_fig:
            st.pyplot(dist_fig)
        else:
            st.info("No numeric columns to plot distributions.")

    with viz_tab3:
        box_fig = plot_boxplots(df)
        if box_fig:
            st.pyplot(box_fig)
        else:
            st.info("No numeric columns to plot boxplots.")

    with viz_tab4:
        heatmap_fig = plot_correlation_heatmap(df)
        if heatmap_fig:
            st.pyplot(heatmap_fig)
        else:
            st.info("Need at least 2 numeric columns for a correlation heatmap.")

    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════
    # 5. Analysis Report
    # ═══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("## 5. Analysis Report")
    report = generate_report(df, info, cleaning_log)
    for item in report:
        icon = ""
        if "缺失" in item or "异常" in item or "重复" in item:
            icon = "⚠️ "
        elif "未发现" in item or "完整性" in item or "适合" in item:
            icon = "✅ "
        else:
            icon = "• "
        st.markdown(f"{icon}{item}")
    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════
    # 6. ML Modeling
    # ═══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("## 6. Machine Learning — Multi-Model Comparison")

    target_column = st.selectbox(
        "Select target column",
        df.columns,
        help="Choose the column you want to predict."
    )

    if st.button("Train & Compare 6 Models", type="primary", use_container_width=True):
        with st.spinner("Training 6 models... This may take a minute."):
            try:
                result = compare_models(df, target_column)

                st.success(f"Training complete — task type: **{result['task_type']}**")
                st.markdown("---")

                col_left, col_right = st.columns([3, 2])

                with col_left:
                    st.markdown("#### Model Performance Comparison")
                    sorted_df = result["results_df"].sort_values(
                        by=result["results_df"].columns[1], ascending=False
                    )
                    st.dataframe(
                        sorted_df,
                        use_container_width=True,
                        hide_index=True,
                    )

                with col_right:
                    st.markdown("#### Best Model")
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="value" style="font-size:1.4rem;">{result['best_model_name']}</div>
                        <div class="label">Top Performer</div>
                    </div>
                    """, unsafe_allow_html=True)

                    best_idx = sorted_df.iloc[0]
                    metric_col = sorted_df.columns[1]
                    st.metric(
                        label=metric_col,
                        value=best_idx[metric_col],
                    )

                st.markdown("---")
                st.markdown("#### Feature Importance")
                imp_fig = plot_feature_importance(
                    result["feature_names"],
                    result["feature_importance"],
                    result["best_model_name"],
                )
                st.pyplot(imp_fig)

            except Exception as e:
                st.error("Model training failed. Please check your data quality.")
                st.exception(e)

    st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error("Unable to read the file. Please verify it's a valid CSV.")
    st.exception(e)
