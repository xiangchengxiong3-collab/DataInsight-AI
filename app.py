import streamlit as st

from src.data_loader import load_csv
from src.eda import get_basic_info
from src.visualization import plot_missing_values, plot_numeric_distribution
from src.report import generate_basic_report
from src.modeling import train_basic_model


st.set_page_config(
    page_title="DataInsight-AI",
    layout="wide"
)

st.title("📊 DataInsight-AI")
st.write("一个基于 Python 的智能数据分析助手。")

uploaded_file = st.file_uploader(
    "请上传一个 CSV 文件",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = load_csv(uploaded_file)

        st.success("CSV 文件上传成功！")

        st.subheader("1. 数据预览")
        st.dataframe(df.head())

        info = get_basic_info(df)

        st.subheader("2. 数据基本信息")

        col1, col2, col3 = st.columns(3)

        col1.metric("行数", info["rows"])
        col2.metric("列数", info["columns"])
        col3.metric("重复行数量", info["duplicated_rows"])

        st.subheader("3. 字段名称")
        st.write(info["column_names"])

        st.subheader("4. 缺失值统计")
        missing_df = info["missing_values"].reset_index()
        missing_df.columns = ["字段名", "缺失值数量"]
        st.dataframe(missing_df)

        st.subheader("5. 数据类型")
        types_df = info["data_types"].astype(str).reset_index()
        types_df.columns = ["字段名", "数据类型"]
        st.dataframe(types_df)

        st.subheader("6. 缺失值可视化")
        missing_fig = plot_missing_values(df)

        if missing_fig is not None:
            st.pyplot(missing_fig)
        else:
            st.info("当前数据没有缺失值。")

        st.subheader("7. 数值字段分布图")
        dist_fig = plot_numeric_distribution(df)

        if dist_fig is not None:
            st.pyplot(dist_fig)
        else:
            st.info("当前数据没有可绘制的数值字段。")

        st.subheader("8. 自动分析结论")

        report = generate_basic_report(df, info)

        for item in report:
            st.write("- " + item)

        st.subheader("9. 机器学习建模")

        target_column = st.selectbox(
            "请选择目标列",
            df.columns
        )

        if st.button("开始训练模型"):
            try:
                model_result = train_basic_model(df, target_column)

                st.success("模型训练完成！")

                st.write("任务类型：", model_result["task_type"])
                st.write("模型名称：", model_result["model_name"])

                if model_result["task_type"] == "分类任务":
                    st.metric(
                        "Accuracy",
                        round(model_result["accuracy"], 4)
                    )
                    st.metric(
                        "F1-score",
                        round(model_result["f1_score"], 4)
                    )
                else:
                    st.metric(
                        "R²",
                        round(model_result["r2_score"], 4)
                    )
                    st.metric(
                        "RMSE",
                        round(model_result["rmse"], 4)
                    )

            except Exception as e:
                st.error("模型训练失败，请检查数据是否适合建模。")
                st.exception(e)

    except Exception as e:
        st.error("文件读取失败，请检查 CSV 文件格式。")
        st.exception(e)

else:
    st.info("请先上传一个 CSV 文件。")
