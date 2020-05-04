from pathlib import Path
import pickle
from datetime import datetime
import logging
import os

import numpy as np
from catboost import CatBoostRegressor, CatBoostClassifier, Pool
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.metrics import cohen_kappa_score
import shap


def mae_score(true, pred):
    true = np.array(true)
    pred = np.array(pred)
    metric = np.mean(np.abs(true - pred))
    return metric


def rmse_score(true, pred):
    true = np.array(true)
    pred = np.array(pred)
    metric = np.sqrt(np.mean((true - pred) ** 2))
    return metric


def qwk_score(true, pred):
    metric = cohen_kappa_score(true, pred, weights='quadratic')
    return metric


class BaseModel:

    def __init__(self, params):
        self.params = params
        self.model = None
        self.metrics = {}
        self.cv = None
        self.name = None
        self.scores = {}
        # self.module_logger = logging.getLogger('commercial_strategy.models')

    def fit(self, X, y):
        pass

    def predict(self, X):
        preds = self.model.predict(X)
        return preds
    
    def score(self, X, y_true):
        y_pred = self.predict(X)
        scores = {name: metric(y_true, y_pred) for name, metric in self.metrics.items()}
        return scores

    def cross_validate(self, X, y):
        scores = {name: [] for name in self.metrics.keys()}

        for train_index, test_index in self.cv.split(X, y):
            X_train, X_test = X.iloc[train_index, :], X.iloc[test_index, :]
            y_train, y_test = y[train_index], y[test_index]

            self.fit(X_train, y_train)
            X_test['is_mp'] = 0
            metrics = self.score(X_test, y_test)
            
            [scores[name].append(v) for name, v in metrics.items()]

        # refit the model
        self.fit(X, y)
        self.scores = {name: np.mean(values) for name, values in scores.items()}

        return self.scores

    def log_scores(self):
        for name, value in self.scores.items():
            print('{:>20s} {:>4s}: {:.4f}'.format(self.name, name, value))
            # self.module_logger.info('{:>20s} {:>4s}: {:.4f}'.format(self.name, name, value))

    def extract_shap_values(self, X):
        pass


class CatBoostRegressorModel(BaseModel):

    def __init__(self, categorical_features_indices, params):
        super().__init__(params)
        self.categorical_features_indices = categorical_features_indices
        self.name = 'CatBoostRegressor'
        self.cv = KFold(5, shuffle=True, random_state=1)
        self.metrics = {
            'MAE': mae_score,
            'RMSE': rmse_score
        }

    def fit(self, X, y):
        train_pool = Pool(X, y, cat_features=self.categorical_features_indices)

        self.model = CatBoostRegressor()
        self.model.set_params(**self.params)
        self.model.fit(train_pool)
        
        return self.model

    def extract_shap_values(self, X):
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(Pool(X, cat_features=self.categorical_features_indices))
        return shap_values
    
class CatBoostClassifierModel(BaseModel):

    def __init__(self, categorical_features_indices, params):
        super().__init__(params)
        self.categorical_features_indices = categorical_features_indices
        self.name = 'CatBoostClassifier'
        self.cv = StratifiedKFold(5, shuffle=True, random_state=1)
        self.metrics = {
            'QWK': qwk_score,
        }

    def fit(self, X, y):
        train_pool = Pool(X, y, cat_features=self.categorical_features_indices)

        self.model = CatBoostClassifier()
        self.model.set_params(**self.params)
        self.model.fit(train_pool)
        
        return self.model

    def extract_shap_values(self, X):
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(Pool(X, cat_features=self.categorical_features_indices))
        return shap_values

