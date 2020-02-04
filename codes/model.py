from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from .preprocess import load_clean_data


class DelinquentClassifier:
    """
    Build and train a
    """

    def __init__(self, X_train, y_train):
        """

        Args:
            X_train: Features training data
            y_train: Target training data
            pipe: default is None, then will build a generic Pipeline
        """
        self.X_train, self.y_train = X_train, y_train  # initialize by passing in training data
        self.pipe = Pipeline()
    def build_pipeline(self, steps):
        """
        Build a pipeline.

        Args:
            steps (sklearn.pipeline.Pipeline): if None, build a default Pipeline [StandardScaler, OneHotEncoder,
            LogisticRegression]

        Returns:

        """
        if steps is None:
            steps = dict(
                std_sc=StandardScaler(),
                dummies=OneHotEncoder(),
                estm=LogisticRegression()
                )
        self.pipe = Pipeline(steps=list(steps.items()))
        return self

    def tune_hyperparam(self):
        # do RandomSearchCV just have wide range and a lot of iterations
        return self
