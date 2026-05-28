# DataInsight-AI

DataInsight-AI 是一个基于 Python 与 Streamlit 开发的智能数据分析助手。

## 在线演示

项目已部署至 Streamlit Cloud，可在线访问：

https://datainsight-ai.streamlit.app


用户上传 CSV 文件后，系统能够自动完成：

* 数据预览
* 数据基本信息统计
* 缺失值分析
* 数据类型识别
* 数据可视化
* 自动分析结论生成
* 基础机器学习建模

本项目主要用于展示 Python 数据分析、数据可视化、机器学习与 Web 数据应用开发能力，可作为数据科学与大数据技术方向的项目实践作品。

---

# 当前版本

当前版本：v0.4 机器学习建模版

---

# 已实现功能

## v0.1 基础数据分析

* CSV 文件上传
* 数据前 5 行预览
* 行数统计
* 列数统计
* 字段名称展示
* 重复值统计
* 缺失值统计
* 数据类型识别
* CSV 文件异常处理

---

## v0.2 数据可视化

* 缺失值柱状图
* 数值字段分布图

---

## v0.3 自动分析结论

自动生成：

* 数据规模分析
* 重复值分析
* 缺失值分析
* 缺失值最多字段识别
* 数值型字段统计
* 类别型字段统计
* 数据分析建议

---

## v0.4 机器学习建模

支持：

* 用户选择目标列
* 自动判断分类任务或回归任务
* 自动完成基础数据预处理
* RandomForestClassifier
* RandomForestRegressor
* Accuracy
* F1-score
* R²
* RMSE

---

# 技术栈

* Python
* Streamlit
* Pandas
* Matplotlib
* Scikit-learn
* GitHub

---

# 项目结构

```text
DataInsight-AI
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── src
    ├── data_loader.py
    ├── eda.py
    ├── visualization.py
    ├── report.py
    └── modeling.py
```

---

# 本地运行

## 1. 克隆项目

```bash
git clone <your-repository-url>
```

---

## 2. 进入项目目录

```bash
cd DataInsight-AI
```

---

## 3. 安装依赖

```bash
pip install -r requirements.txt
```

---

## 4. 启动项目

```bash
streamlit run app.py
```

---

## 5. 浏览器打开

```text
http://localhost:8501
```

---

# 项目演示

## 数据预览

支持 CSV 文件上传与数据表格展示。
<img width="1919" height="860" alt="homepage" src="https://github.com/user-attachments/assets/a4a08c8d-58f0-44a0-8dab-3b6bd3aa1120" />

---

## 缺失值分析

自动统计缺失值并生成缺失值柱状图。
<img width="1878" height="310" alt="missing_values" src="https://github.com/user-attachments/assets/5ae00670-11d7-4f36-b914-7731d901d718" />

---

## 数值字段分布分析

自动绘制数值型字段分布图。
<img width="1214" height="875" alt="distribution" src="https://github.com/user-attachments/assets/d902d82b-811f-4ef8-b53d-3f3f99a4a131" />

---

## 自动分析结论

自动生成基础数据分析报告。
<img width="828" height="403" alt="report" src="https://github.com/user-attachments/assets/c6e2dd40-bb47-4487-b8d1-eaabeccd8c8e" />

---

## 机器学习建模
<img width="1238" height="515" alt="modeling" src="https://github.com/user-attachments/assets/8815ddba-caf1-4e58-892b-2393b39030b0" />

支持：

* 分类任务
* 回归任务
* 自动模型训练
* 自动输出评价指标

---

# 后续计划

## v0.5 AI 数据分析报告

计划实现：

* AI 自动数据分析
* 自动生成数据质量报告
* 自动生成建模建议
* 自动生成业务分析结论

---

## v0.6 Web 部署版

计划实现：

* Streamlit Cloud 在线部署
* 支持公网访问
* 项目在线演示

---

# 项目亮点

* 使用 Streamlit 构建交互式数据分析网页
* 使用 Pandas 完成自动化数据探索分析
* 使用 Matplotlib 实现基础可视化
* 使用 Scikit-learn 完成基础机器学习建模
* 自动判断分类任务与回归任务
* 模块化项目结构，便于后续扩展
* 支持真实 CSV 数据集分析
* 适合作为数据分析 / AI / 大数据方向实习项目

---

# 项目定位

本项目定位为：

```text
数据分析 + 自动EDA + 机器学习 + Web应用
```

后续将继续扩展 AI 自动报告生成能力，逐步发展为轻量级 AutoML 数据分析平台。
