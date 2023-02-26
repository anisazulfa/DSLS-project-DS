"""
This file contains data preprocessing and feature engineering
"""

import util as utils
from sklearn.preprocessing import StandardScaler

def load_dataset(config_data: dict):
    """
    Load dataset
    """
    x_train = utils.pickle_load(config_data["train_set_path"][0])
    y_train = utils.pickle_load(config_data["train_set_path"][1])
    x_test = utils.pickle_load(config_data["test_set_path"][0])
    y_test = utils.pickle_load(config_data["test_set_path"][1])

    return x_train, x_test, y_train, y_test

def scaler_model(df, config):
    """
    save scaler model
    """
    scaler = StandardScaler()
    scaler.fit(df)
    utils.pickle_dump(scaler, config["standard_scaler"]) 

def scale_data(df, config):
    """
    scale the dataset
    """
    scaler = utils.pickle_load(config["standard_scaler"])
    x_scaled = scaler.transform(df)

    return x_scaled

if __name__ == "__main__":
    # 1. Load configuration file
    config = utils.load_config()
    # 2. Load dataset
    x_train, x_test, y_train, y_test = load_dataset(config)
    # 3. Scale data
    scaler_model(x_train, config)
    X_train_scaled = scale_data(x_train, config)
    X_test_scaled = scale_data(x_test, config)
    # 4. Dump set data
    utils.pickle_dump(X_train_scaled, config["train_feng_set_path"][0])
    utils.pickle_dump(y_train, config["train_feng_set_path"][1])

    utils.pickle_dump(X_test_scaled, config["test_feng_set_path"][0])
    utils.pickle_dump(y_test, config["test_feng_set_path"][1])
    