# DataInsight-AI

基于 Python 与 Streamlit 的智能数据分析助手。

## 项目简介

DataInsight-AI 是一个面向 CSV 数据文件的智能数据分析工具。用户可以通过网页上传 CSV 文件，系统自动完成数据预览、基础统计、缺失值分析、数据类型识别和可视化展示。

## 已实现功能

- CSV 文件上传
- 数据前 5 行预览
- 行数与列数统计
- 重复行数量统计
- 字段名称展示
- 缺失值统计
- 数据类型识别
- 缺失值可视化
- 数值字段分布图
- 错误 CSV 文件异常处理

## 技术栈

- Python
- Streamlit
- Pandas
- Matplotlib
- Scikit-learn

## 项目结构

```text
DataInsight-AI
├── app.py
├── requirements.txt
├── README.md
├── src
│   ├── data_loader.py
│   ├── eda.py
│   └── visualization.py
