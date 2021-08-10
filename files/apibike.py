# 1. Library imports

import uvicorn
import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from Bikes import Bike
from base64 import b64encode
import pandas as pd
import joblib

# chargement des modéles
loaded_lineareModel = open("lineareModel.pkl", "rb")
lineareModel = joblib.load(loaded_lineareModel)

loaded_ridgeModel = open("ridgeModel.pkl", "rb")
ridgeModel = joblib.load(loaded_ridgeModel)

loaded_randomforestModel = open("randomforestModel.pkl", "rb")
randomforestModel = joblib.load(loaded_randomforestModel)

loaded_decisiontreemodel = open("decisiontreemodel.pkl", "rb")
decisiontreemodel = joblib.load(loaded_decisiontreemodel)

app = FastAPI()

security = HTTPBasic()

username = 'alice'
password = 'wonderland'
encoded_credentials = b64encode(bytes(f'{username}:{password}', encoding='ascii')).decode('ascii')
auth_header = f'Basic {encoded_credentials}'


username1 = 'bob'
password1 = 'builder'
encoded_credentials1 = b64encode(bytes(f'{username1}:{password1}', encoding='ascii')).decode('ascii')
auth_header1 = f'Basic {encoded_credentials1}'

username2 = 'clementine'
password2 = 'mandarine'
encoded_credentials2 = b64encode(bytes(f'{username1}:{password1}', encoding='ascii')).decode('ascii')
auth_header2 = f'Basic {encoded_credentials2}'


def get_current_username(encoded_credentials: HTTPBasicCredentials = Depends(security),
                         encoded_credentials1: HTTPBasicCredentials = Depends(security),
                         encoded_credentials2: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(encoded_credentials.username, "alice")
    correct_password = secrets.compare_digest(encoded_credentials.password, "wonderland")
    correct_username1 = secrets.compare_digest(encoded_credentials1.username, "bob")
    correct_password1 = secrets.compare_digest(encoded_credentials1.password, "builder")
    correct_username2 = secrets.compare_digest(encoded_credentials2.username, "clementine")
    correct_password2 = secrets.compare_digest(encoded_credentials2.password, "mandarine")

    if not (correct_username and correct_password):
        if not (correct_username1 and correct_password1):
            if not (correct_username2 and correct_password2):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                                    headers={"WWW-Authenticate": "Basic"})

            return encoded_credentials2.username

        return encoded_credentials1.username

    return encoded_credentials.username

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


@app.post('/ridgepredict')
async def ridgepredict(bk: Bike, username: str = Depends(get_current_username)):

    """Renvoie le décompte de vélo prédit dans les conditions ci-dessous
    """
    df = pd.DataFrame([bk.dict()])

    prediction = ridgeModel.predict(df)
    # score = ridgeModel.score(bk_array, prediction[0])
    return {'prediction': prediction[0]}


@app.post('/linearprediction')
async def linearprediction(bk: Bike, username: str = Depends(get_current_username)):
    """Renvoie le décompte de vélo prédit dans les conditions ci-dessous
    """
    df = pd.DataFrame([bk.dict()])
    prediction = lineareModel.predict(df)
    # score = lineareModel.score(bk_array, prediction[0])
    return {'prediction': prediction[0]}


@app.post('/randomforestprediction')
async def randomforestprediction(bk: Bike, username: str = Depends(get_current_username)):
    """Renvoie le décompte de vélo prédit dans les conditions ci-dessous
    """
    df = pd.DataFrame([bk.dict()])
    prediction = randomforestModel.predict(df)
    # score = decisiontreemodel.score(bk_array, prediction)
    return {'prediction': prediction[0]}


@app.post('/decisiontreeprediction')
async def decisiontreeprediction(bk: Bike, username: str = Depends(get_current_username)):
    """Renvoie le décompte de vélo prédit dans les conditions ci-dessous
    """
    df = pd.DataFrame([bk.dict()])
    prediction = decisiontreemodel.predict(df)
    return {'prediction': prediction[0]}

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
