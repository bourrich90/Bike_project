# 1. Library imports
import json
import uvicorn
import secrets
import base64
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from Bikes import Bike
from pydantic import BaseModel
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from base64 import b64encode
import numpy as np
import pickle
import pandas as pd
import joblib

2# chargement des modéles
loaded_lineareModel = open("lineareModel.pkl","rb")
lineareModel = joblib.load(loaded_lineareModel)

loaded_ridgeModel = open("ridgeModel.pkl","rb")
ridgeModel = joblib.load(loaded_ridgeModel)

loaded_randomforestModel = open("randomforestModel.pkl","rb")
randomforestModel = joblib.load(loaded_randomforestModel)

loaded_decisiontreemodel = open("decisiontreemodel.pkl","rb")
decisiontreemodel = joblib.load(loaded_decisiontreemodel)

app = FastAPI()

security = HTTPBasic()

username = 'alice'
password = 'wonderland'
encoded_credentials = b64encode(bytes(f'{username}:{password}',encoding='ascii')).decode('ascii')
auth_header = f'Basic {encoded_credentials}'
#headers = {"Authorization" : "Basic %s" % encoded_credentials}


def get_current_username(encoded_credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(encoded_credentials.username, "alice")
    correct_password = secrets.compare_digest(encoded_credentials.password, "wonderland")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return encoded_credentials.username
     
# 
@app.get('/status')
async def get_status():
    """Renvoie 1 si API UP
    """
    return {
        'status': 1
    }


@app.get('/performances')
async def models_perf(username: str = Depends(get_current_username)):
    """Renvoie les performances des différents modéles
    """

    return {
        'score du modéle  Ridge': 0.7995510925443807,
        'score du modéle  Random Forest': 0.776114526983984,
        'score du modéle  Decison Tree': 0.7684617271350079,
        'score du modéle  linearRegression': 0.8031284750503873,
    }

@app.get('/{username}')
async def get_name(username: str = Depends(get_current_username)):
    return {'Bienvenue au projet bike ': f'{username}'}


@app.post('/predict')
async def predict_bike(bk: Bike, username: str = Depends(get_current_username)):

    """Renvoie le décompte de vélo prédit dans les conditions ci-dessous
    """
    hum_min = bk.hum_min
    hum_max = bk.hum_max
    hum_mean = bk.hum_mean
    hum_q25 = bk.hum_q25
    hum_q50 = bk.hum_q50
    hum_q75 = bk.hum_q75

    windspeed_min = bk.windspeed_min
    windspeed_max = bk.windspeed_max
    windspeed_mean = bk.windspeed_mean
    windspeed_q25 = bk.windspeed_q25
    windspeed_q50 = bk.windspeed_q50
    windspeed_q75 = bk.windspeed_q75

    temp_min = bk.temp_min
    temp_max = bk.hum_max
    temp_mean = bk.hum_mean
    temp_q25 = bk.temp_q25
    temp_q50 = bk.temp_q50
    temp_q75 = bk.temp_q75

    atemp_min = bk.atemp_min
    atemp_max = bk.atemp_max
    atemp_mean = bk.hum_mean
    atemp_q25 = bk.atemp_q25
    atemp_q50 = bk.atemp_q50
    atemp_q75 = bk.atemp_q75

    clear = bk.clear
    cloudy = bk.cloudy
    rainy = bk.rainy
    snowy = bk.snowy

    cnt = bk.cnt
    cnt_j_1 = bk.cnt_j_1
    cnt_j_2 = bk.cnt_j_2
    cnt_j_3 = bk.cnt_j_3
    cnt_j_4 = bk.cnt_j_4
    cnt_j_5 = bk.cnt_j_5
    cnt_j_6 = bk.cnt_j_6
    cnt_j_7 = bk.cnt_j_7

    bk_array = np.array([[hum_min, hum_max, hum_mean, hum_q25, hum_q50, hum_q75, windspeed_min, windspeed_max,
                          windspeed_mean, windspeed_q25,
                          windspeed_q50, windspeed_q75, temp_min, temp_max, temp_mean, temp_q25, temp_q50, temp_q75,
                          atemp_min, atemp_max,
                          atemp_mean, atemp_q25, atemp_q50, atemp_q75, clear, cloudy, rainy, snowy, cnt, cnt_j_1,
                          cnt_j_2, cnt_j_3, cnt_j_4,
                          cnt_j_5, cnt_j_6, cnt_j_7]])

    prediction = ridgeModel.predict(bk_array)
    
    return {'prediction': prediction[0]}


# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)