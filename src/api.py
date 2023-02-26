from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pandas as pd
import util as utils
import data_pipeline as data_pipeline
from preprocessing import scale_data

config = utils.load_config()
model_data = utils.pickle_load(config["production_model_path"])

class api_data(BaseModel):
    jam_level : int
    median_length :float
    median_delay_seconds : float
    median_regular_speed : float
    total_records : int
    median_speed : float

app = FastAPI()

@app.get("/")
def home():
    return "Cari apa?"

@app.post("/predict/")
def predict(data: api_data):    
    # Convert data api to dataframe
    print(data)
    data = pd.DataFrame(data).set_index(0).T.reset_index(drop = True)  # type: ignore
    data.columns = config["predictors"]

    # Convert dtype
    convert_type = {
        "jam_level" : int,
        "median_length" :float,
        "median_delay_seconds" : float,
        "median_regular_speed" : float,
        "total_records" : int,
        "median_speed" : float
    }
    data = data.astype(convert_type)

    # Check range data
    try:
        data_pipeline.check_data(data, config, True)  # type: ignore
    except AssertionError as ae:
        return {"res": [], "error_msg": str(ae)}
    
    # Preprocess data
    data_scaled = scale_data(data, config)

    # Predict data
    y_pred = model_data.predict(data_scaled)
    y_pred = round(y_pred[0])
    res_seconds = str(y_pred)
    res_minutes = str(round(y_pred/60, 2))

    return {"res" : "Waktu untuk menempuh kemacetan: %s detik atau %s menit." % (res_seconds, res_minutes), "error_msg": ""}

if __name__ == "__main__":
    uvicorn.run("api:app", host = "0.0.0.0", port = 8080, reload = True)