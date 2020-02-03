from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier


def split_train_test(df):
    X = df.drop(columns=['delinquency_status'])
    y = df.PRELEVER
    return train_test_split(X, y, test_size=0.2, stratify=y, random_state=2020)


class DelinquencyClassifier:
    def __init__(self, df, pipe=None):
        self.X_train, self.X_test, self.y_train, self.y_test = split_train_test(df)
        self.pipe = pipe

    def build_pipeline(self, steps=None):
        self.pipe = Pipeline(steps)

    def tune_hyperparam(self):
        # do RandomSearchCV
        # then GridSearchCV
        pass
