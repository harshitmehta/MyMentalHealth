# -*- coding: utf-8 -*-
"""
@author: HARSHIT
"""
import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier


def model_train():
    # to_predict = user_data
    df = pd.read_csv('survey.csv')
    df.drop(df.columns[[0, 4, 5, 26]], axis=1, inplace=True)
    # Deleting Timestamp, State, self-employed and comments

    df['Gender'] = df['Gender'].str.lower()

    df.Gender = df.Gender.replace('m', 'male')
    df.Gender = df.Gender.replace('male-ish', 'male')
    df.Gender = df.Gender.replace('maile', 'male')
    df.Gender = df.Gender.replace('mal', 'male')
    df.Gender = df.Gender.replace('male (cis)', 'male')
    df.Gender = df.Gender.replace('make', 'male')
    df.Gender = df.Gender.replace('man', 'male')
    df.Gender = df.Gender.replace('msle', 'male')
    df.Gender = df.Gender.replace('mail', 'male')
    df.Gender = df.Gender.replace('malr', 'male')
    df.Gender = df.Gender.replace('cis man', 'male')
    df.Gender = df.Gender.replace('cis male', 'male')
    df.Gender = df.Gender.replace('male', 'male')
    df.Gender = df.Gender.replace('male ', 'male')

    df.Gender = df.Gender.replace('f', 'female')
    df.Gender = df.Gender.replace('cis female', 'female')
    df.Gender = df.Gender.replace('woman', 'female')
    df.Gender = df.Gender.replace('femake', 'female')
    df.Gender = df.Gender.replace('female ', 'female')
    df.Gender = df.Gender.replace('cis-female/femme', 'female')
    df.Gender = df.Gender.replace('female (cis)', 'female')
    df.Gender = df.Gender.replace('femail', 'female')

    df.Gender = df.Gender.replace('trans-female', 'other')
    df.Gender = df.Gender.replace('something kinda male?', 'other')
    df.Gender = df.Gender.replace('queer/she/they', 'other')
    df.Gender = df.Gender.replace('non-binary', 'other')
    df.Gender = df.Gender.replace('nah', 'other')
    df.Gender = df.Gender.replace('all', 'other')
    df.Gender = df.Gender.replace('enby', 'other')
    df.Gender = df.Gender.replace('fluid', 'other')
    df.Gender = df.Gender.replace('genderqueer', 'other')
    df.Gender = df.Gender.replace('androgyne', 'other')
    df.Gender = df.Gender.replace('agender', 'other')
    df.Gender = df.Gender.replace('male leaning androgynous', 'other')
    df.Gender = df.Gender.replace('guy (-ish) ^_^', 'other')
    df.Gender = df.Gender.replace('trans woman', 'other')
    df.Gender = df.Gender.replace('neuter', 'other')
    df.Gender = df.Gender.replace('female (trans)', 'other')
    df.Gender = df.Gender.replace('queer', 'other')
    df.Gender = df.Gender.replace('ostensibly male, unsure what that really means', 'other')
    df.Gender = df.Gender.replace('p', 'other')
    df.Gender = df.Gender.replace('a little about you', 'other')

    df['Age'] = pd.to_numeric(df['Age'],errors='coerce')

    def age_process(age):
        if age>=0 and age<=100:
            return age
        else:
            return np.nan

    df['Age'] = df['Age'].apply(age_process)


    df = df.dropna(subset=['work_interfere'])
    df = df.dropna(subset=['Age'])
    df.copy = df

    # convert binary columns to 0 and 1
    for col in df.select_dtypes(include=['object']):
        u_count = len(df[col].unique()) 
        if u_count == 2:
            first = list(df[col].unique())[-1]
            df[col] = (df[col] == first).astype(int)
            # print('converted', col)

    df.work_interfere = df.work_interfere.map({'Never': 0, 'Rarely': 1,'Sometimes': 2, 'Often': 3})

    df.no_employees = df.no_employees.map({'6-25': 25, '26-100': 100, '100-500':500, '500-1000': 1000, 'More than 1000': 2000, '1-5': 5})

    mapping = {'Yes': 1, 'No': 0, "Don't know": 2,'Not sure': 2, 'Maybe': 2, 'Some of them': 2}
    #three_factor = {'Yes': 1, 'No': -1, 'Not sure': 0}
    for col in df.select_dtypes(include=['object']):
        uniques = set(df[col].unique())
        if (uniques == {'Yes', 'No', "Don't know"} or
            uniques == {'Yes', 'No', 'Not sure'} or
            uniques == {'Yes', 'No', 'Maybe'} or
            uniques == {'Yes', 'No', 'Some of them'}):
            # print('converted', col, 'To -1, 0, 1')
            df[col] = df[col].map(mapping)


    df.leave = df.leave.map({'Very easy': 0, 'Somewhat easy': 1, "Don't know": 2, 'Somewhat difficult': 3, 'Very difficult': 4})

    df.Gender = df.Gender.map({'male': 1, 'female': 2, 'other': 3})

    del df['Country']

    x, y = df.drop('treatment', axis=1), df.treatment

    model = RandomForestClassifier(n_jobs=-1, n_estimators=10, class_weight='balanced')

    model.fit(x,y)
    # preds = model.predict(x)
    # print(preds)
    
    # save model weights
    joblib.dump(model, "./rf_model.joblib")
    print("Model trained and exported to joblib")

    # print("Feature ranking:")   
    # for f in range(len(x.columns)):
    #     print("Feature %s : (%f)" %(x.columns[f], model.feature_importances_[f]))
        
        
def model_predict(user_data):
    # load, no need to initialize the loaded_rf
    print("Inside Model Predict")
    loaded_model = joblib.load("./rf_model.joblib")
    prediction = loaded_model.predict(user_data)
    return prediction        
        
        



