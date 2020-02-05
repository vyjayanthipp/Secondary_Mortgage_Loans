from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import *  #
from imblearn.pipeline import Pipeline
from yellowbrick.classifier import ConfusionMatrix


def CM(pipe, X, y):
    delinq_cm = ConfusionMatrix(pipe,
                                classes=['Current', 'Delinquent'],
                                label_encoder={0: 'Current', 1: 'Delinquent'},
                                is_fitted=True, percent=True
                                )
    delinq_cm.score(X, y)
    delinq_cm.show()
    print(delinq_cm.confusion_matrix_)
    print(classification_report(y, pipe.predict(X), target_names=['Current', 'Delinquent'], digits=4))


def build_transformers(X):
    """
    Build a columns transformer to be used at the first step in a Pipeline
    Args:
        X (pandas.DataFrame): Features

    Returns:
        ColumnTransformer: StandardScaler for numeric features and OneHotEncoder for categorical features to be used
        at the beginning of the pipeline
    """
    categ_cols = X.columns[X.dtypes == object].tolist()
    numeric_cols = X.columns[X.dtypes != object].tolist()
    categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])
    numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])
    preprocessor = ColumnTransformer(
        transformers=[
            ('numeric', numeric_transformer, numeric_cols),
            ('categor', categorical_transformer, categ_cols)
            ]
        )
    return preprocessor
