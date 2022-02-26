# -*- coding: utf-8 -*-
"""
@author: HARSHIT
"""
import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
        
        
def model_predict(user_data):
    # load, no need to initialize the loaded_rf
    print("Inside Model Predict")
    print(type(user_data))
    print("---The user data received from app---")
    print(user_data)
    loaded_model = joblib.load("./new_rf_model.joblib")
    print("Joblib successfully loaded")
    
    prediction = loaded_model.predict(user_data)
    return prediction
        
        






