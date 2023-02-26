"""
This file contains training model
"""

import util as utils
from numpy import absolute
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error


def load_train_feng(params: dict):
    """
    Load train set
    """
    x_train = utils.pickle_load(params["train_feng_set_path"][0])
    y_train = utils.pickle_load(params["train_feng_set_path"][1])

    return x_train, y_train

def load_test_feng(params: dict):
    """
    Load test set
    """
    x_test = utils.pickle_load(params["test_feng_set_path"][0])
    y_test = utils.pickle_load(params["test_feng_set_path"][1])

    return x_test, y_test

def train_model(x_train, x_test, y_train, y_test):
    """
    Train Model
    """
    model = XGBRegressor()
    param_grid = {"max_depth": [4, 5],
                    "n_estimators": [500, 600, 700],
                    "learning_rate": [0.01, 0.015]}

    result = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_absolute_error',)
    result.fit(x_train, y_train)
    scores = absolute(result.best_score_)

    best_model = result.best_estimator_
    y_hat = best_model.predict(x_test)
    errors = mean_absolute_error(y_test, y_hat)

    print("The best hyperparameters are ",result.best_params_)
    print("MAE of gridsearch: %.3f" % (scores))
    print("MAE: %.3f" % (errors))
    
    return result.best_estimator_

if __name__ == "__main__" :
    # 1. Load config file
    config = utils.load_config()
    # 2. Load set data
    x_train, y_train = load_train_feng(config)
    x_test, y_test = load_test_feng(config)
    # 3. Train model
    model = train_model(x_train, x_test, y_train, y_test)
    # 4. Dump model
    utils.pickle_dump(model, config["production_model_path"])