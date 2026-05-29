"""DataInsight-AI global configuration."""

RANDOM_SEED = 42
TEST_SIZE = 0.2
N_ESTIMATORS = 100
IQR_FACTOR = 1.5
FIGURE_SIZE = (12, 8)
MAX_FEATURES_DISPLAY = 15

CLASSIFICATION_MODELS: dict = {
    "Random Forest": {
        "import_path": "sklearn.ensemble.RandomForestClassifier",
    },
    "XGBoost": {
        "import_path": "xgboost.XGBClassifier",
    },
    "Logistic Regression": {
        "import_path": "sklearn.linear_model.LogisticRegression",
    },
    "SVM": {
        "import_path": "sklearn.svm.SVC",
    },
    "KNN": {
        "import_path": "sklearn.neighbors.KNeighborsClassifier",
    },
    "Gradient Boosting": {
        "import_path": "sklearn.ensemble.GradientBoostingClassifier",
    },
}

REGRESSION_MODELS: dict = {
    "Random Forest": {
        "import_path": "sklearn.ensemble.RandomForestRegressor",
    },
    "XGBoost": {
        "import_path": "xgboost.XGBRegressor",
    },
    "Linear Regression": {
        "import_path": "sklearn.linear_model.LinearRegression",
    },
    "SVR": {
        "import_path": "sklearn.svm.SVR",
    },
    "KNN": {
        "import_path": "sklearn.neighbors.KNeighborsRegressor",
    },
    "Gradient Boosting": {
        "import_path": "sklearn.ensemble.GradientBoostingRegressor",
    },
}
