# Imports
import os
import sys
import subprocess
import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import time
from datetime import datetime

# Model Imports
import category_encoders as ce
import xgboost as xgb
import sklearn as sk

# Base Preprocess
def encode_info(data):
    
    date = data["time_info"]
    PULocationID = data["PULocation"]
    DOLocationID = data["DOLocation"]
    trip_distance = data["trip_distance"]
    
    # Get day number, month number
    day = date.day
    month = date.month
    hour = date.hour
    
    # Get day of the week
    day_of_week = date.weekday()
    
    # Get weekend or weekday
    weekend = 0
    if day_of_week == 5 or day_of_week == 6:
        weekend = 1
        
    data_encode = {
        "day": day,
        "month": month,
        "hour": hour,
        "day_of_week": day_of_week,
        "weekend": weekend,
        "PULocationID": PULocationID,
        "DOLocationID": DOLocationID,
        "trip_distance": trip_distance
    }
    
    return data_encode
    
    
# Circular Encoding
def encode_circular(data):
    
    day_of_week = data["day_of_week"]
    hour = data["hour"]
    
    # Circular encoding for day of week
    dow_sin = np.sin((day_of_week / 7) * 2 * np.pi)
    dow_cos = np.cos((day_of_week / 7) * 2 * np.pi)
    
    # Circular encoding for hour of the day
    hour_sin = np.sin((hour / 24) * 2 * np.pi)
    hour_cos = np.cos((hour / 24) * 2 * np.pi)
    
    # Create a new dictionary with the circular encoded values
    data_encode = {
        "dow_sin": dow_sin,
        "dow_cos": dow_cos,
        "hour_sin": hour_sin,
        "hour_cos": hour_cos,
        "day_of_month": data["day"],
        "month": data["month"],
        "weekend": data["weekend"],
        "trip_distance": data["trip_distance"],
        "PULocationID": data["PULocationID"],
        "DOLocationID": data["DOLocationID"]
    }
    
    return data_encode

def run_model_xgb(data, path):
    model = xgb.XGBRegressor()
    model.load_model(path)
    
    # Encode the input data
    data_encoded = encode_info(data)
    data_encoded = encode_circular(data_encoded)
    feature_names = model.get_booster().feature_names
    data_df = pd.DataFrame([data_encoded], columns=feature_names)
    data_df = data_df.reindex(columns=feature_names, fill_value=0)
    
    # Make the prediction
    prediction = model.predict(data_df)
    
    return prediction[0]

def run_model_xgb_24(data, path):
    data_encoded = encode_info(data)
    
    model = xgb.XGBRegressor()
    model.load_model(path)
    feature_names = model.get_booster().feature_names
    
    predictions = []
    
    # Run the model for 24 hours of the day  
    for hour in range(24):
        data_temp = data_encoded.copy()
        data_temp["hour"] = hour
        data_temp = encode_circular(data_temp)
        data_df = pd.DataFrame([data_temp], columns=feature_names)
        data_df = data_df.reindex(columns=feature_names, fill_value=0)
        
        # Make the prediction
        prediction = model.predict(data_df)
        predictions.append(prediction[0])
        
    return predictions
    
# Main function

def run_login(input_data):
    """ Input json data
    {
        "date": "2024-08-15",
        "is_amount": true,
        "model_number": 1,
        "PULocationID": 13,
        "DOLocationID": 25
    }
    """  

    data = {}
    data["time_info"] = datetime.strptime(input_data["date"], "%Y-%m-%d")
    data["PULocation"] = input_data["PULocationID"]
    data["DOLocation"] = input_data["DOLocationID"]

    # Add dummy hour to the data to data["time_info"]
    data["time_info"] = data["time_info"].replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Get trip distance from trip_distance_matrix.csv row is PULocationID and column is DOLocationID
    trip_distance_matrix = pd.read_csv("trip_distance_matrix.csv")

    # Get trip distance
    trip_distance = trip_distance_matrix.iloc[data["DOLocation"] - 1, data["PULocation"] - 1]
        
    # If trip distance is NaN, return error
    if pd.isna(trip_distance):
        raise ValueError("Trip distance is NaN. Please check the trip distance matrix.")
    
    data["trip_distance"] = trip_distance
    
    if input_data["model_number"] == 1:
        print("")
        if input_data["is_amount"]:
            path = "models/total_amount_base_model.json"
        else:
            path = "models/travel_time_base_model.json"
        prediction = run_model_xgb_24(data, path)
            
    return prediction
    
    
if __name__ == "__main__":
    # Sample test input
    input_data = {
        "date": "2024-08-15",
        "is_amount": True,
        "model_number": 1,
        "PULocationID": 2,
        "DOLocationID": 2
    }

    result = run_login(input_data)
    print("Output:", result)