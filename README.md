# DataInsight-AI

DataInsight-AI 是一个基于 Python 和 Streamlit 开发的智能数据分析助手，面向 CSV 数据文件，提供自动化的数据预览、基础统计分析、缺失值检测、数据可视化和基础分析结论生成。

本项目定位为数据科学与大数据技术专业学生的项目实践作品，可用于展示 Python 数据分析、Web 数据应用开发、可视化分析和机器学习建模能力。

## 当前版本

当前版本：v0.3 自动分析结论版

## 已实现功能

* CSV 文件上传
* 数据前 5 行预览
* 数据行数和列数统计
* 字段名称展示
* 重复行统计
* 缺失值统计
* 数据类型识别
* 缺失值柱状图可视化
* 数值字段分布图可视化
* 自动生成基础分析结论
* CSV 文件读取异常处理

## 技术栈

* Python
* Streamlit
* Pandas
* Matplotlib
* Scikit-learn
* GitHub

## 项目结构

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
    └── report.py
```

## 本地运行方法

1. 克隆项目到本地

```bash
git clone <your-repository-url>
```

2. 进入项目目录

```bash
cd DataInsight-AI
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 启动项目

```bash
streamlit run app.py
```

5. 在浏览器中打开

```text
http://localhost:8501
```

## 版本进度

### v0.1 基础数据分析版

已完成：

* CSV 文件上传
* 数据预览
* 行数统计
* 列数统计
* 字段名称展示
* 重复行统计
* 缺失值统计
* 数据类型识别
* 错误 CSV 文件异常处理

### v0.2 数据可视化版

已完成：

* 缺失值柱状图
* 数值字段分布图

### v0.3 自动分析结论版

已完成：

* 自动生成基础分析结论
* 分析数据集规模
* 判断重复行情况
* 统计缺失值总数
* 找出缺失值最多的字段
* 统计数值型字段数量
* 统计文本或类别型字段数量
* 给出后续数据分析建议

## 后续计划

### v0.4 机器学习建模模块

计划实现：

* 用户选择目标列
* 系统自动判断分类任务或回归任务
* 自动完成基础数据预处理
* 训练基础机器学习模型
* 输出模型评价指标

分类任务计划支持：

* Logistic Regression
* Random Forest Classifier
* Accuracy
* F1-score

回归任务计划支持：

* Linear Regression
* Random Forest Regressor
* R²
* RMSE

### v0.5 AI 报告生成模块

计划实现：

* 自动生成数据分析报告
* 自动总结数据质量问题
* 自动总结模型训练结果
* 支持生成更完整的数据分析说明

## 项目亮点

* 使用 Streamlit 构建交互式数据分析网页
* 使用 Pandas 完成自动化数据探索分析
* 使用 Matplotlib 完成基础可视化
* 模块化项目结构，便于后续扩展机器学习和 AI 报告生成功能
* 适合作为数据科学方向实习项目经历展示
