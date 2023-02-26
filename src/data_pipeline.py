"""
This file contains data pipeline
"""

import pandas as pd
import util as utils
import copy
from sklearn.model_selection import train_test_split

def read_raw_data(config: dict) -> pd.DataFrame:
    """
    Load dataset
    """
    return pd.read_csv(config["dataset_path"])

def convert_datetime(input_data: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Convert object to datetime type
    """
    input_data = input_data.copy()

    input_data[config["datetime_columns"][0]] = pd.to_datetime(
            input_data[config["datetime_columns"][0]],
            unit = "s"
    )
    input_data[config["datetime_columns"][1]] = pd.to_datetime(
            input_data[config["datetime_columns"][1]]
    )

    return input_data

def check_data(input_data: pd.DataFrame, config: dict, api: bool = False):
        """
        Check types of data
        """
        input_data = copy.deepcopy(input_data)
        config = copy.deepcopy(config)
        len_input_data = len(input_data)

        if not api:
            assert input_data.select_dtypes("int").columns.to_list() == config["int_columns"], "an error occurs in int column(s)."
            assert input_data.select_dtypes("float").columns.to_list() == config["float_columns"], "an error occurs in float column(s)."
        else:
            int_columns = config["int_columns"]
            int_columns = int_columns[:2]

            float_columns = config["float_columns"]
            float_idx = [1,2,3,6]
            float_columns = [float_columns[idx] for idx in float_idx]
            print(float_columns)
            
            assert input_data.select_dtypes("int").columns.to_list() == int_columns, "an error occurs in int column(s)."
            assert input_data.select_dtypes("float").columns.to_list() == float_columns, "an error occurs in float column(s)."
                
        assert input_data[config["float_columns"][1]].between(
                            config["range_median_length"][0],
                            config["range_median_length"][1]
                            ).sum() == len_input_data, "an error occurs in range_median_length."
        assert input_data[config["float_columns"][2]].between(
                            config["range_median_delay_seconds"][0],
                            config["range_median_delay_seconds"][1]
                            ).sum() == len_input_data, "an error occurs in range_median_delay_seconds."
        assert input_data[config["float_columns"][3]].between(
                            config["range_median_regular_speed"][0],
                            config["range_median_regular_speed"][1]
                            ).sum() == len_input_data, "an error occurs in range_median_regular_speed."
        assert input_data[config["float_columns"][6]].between(
                            config["range_median_speed"][0],
                            config["range_median_speed"][1]
                            ).sum() == len_input_data, "an error occurs in range_median_speed."
        assert input_data[config["int_columns"][0]].between(
                            config["range_jam_level"][0],
                            config["range_jam_level"][1]
                            ).sum() == len_input_data, "an error occurs in range_jam_level."
        assert input_data[config["int_columns"][1]].between(
                            config["range_total_records"][0],
                            config["range_total_records"][1]
                            ).sum() == len_input_data, "an error occurs in range_total_records."
        
if __name__ == "__main__":
    # 1. Load configuration file
    config = utils.load_config()
    # 2. Read all raw dataset
    raw_dataset = read_raw_data(config)
    # 3. Data defense
    check_data(raw_dataset, config)
    # 4. Splitting pdata
    x = raw_dataset[config["predictors"]].copy()
    y = raw_dataset[config["label"]].copy()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 42)
    cleaned_dataset = pd.concat([x, y], axis = 1)
    # 6. Save train set
    utils.pickle_dump(x_train, config["train_set_path"][0])
    utils.pickle_dump(y_train, config["train_set_path"][1])
    utils.pickle_dump(x_test, config["test_set_path"][0])
    utils.pickle_dump(y_test, config["test_set_path"][1])
    utils.pickle_dump(cleaned_dataset, config["dataset_cleaned_path"])