#  Library imports
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
import pandas as pd
import joblib
from Bikes import Bike, Token, TokenData, User, UserInDB

# chargement des modéles
loaded_linearModel = open("lineareModel.pkl", "rb")
linearModel = joblib.load(loaded_linearModel)

loaded_ridgeModel = open("ridgeModel.pkl", "rb")
ridgeModel = joblib.load(loaded_ridgeModel)

loaded_randomforestModel = open("randomforestModel.pkl", "rb")
randomforestModel = joblib.load(loaded_randomforestModel)

loaded_decisiontreemodel = open("decisiontreemodel.pkl", "rb")
decisiontreemodel = joblib.load(loaded_decisiontreemodel)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "alice": {
        "username": "alice",
        "full_name": "alice wonderland",
        "email": "alicewonderland@example.com",
        "hashed_password": "$2b$12$.MCZra8u8Q0utw1S2o.1l.O5m/qp.GqputTJ/b5qPijQgjzSfdW1K",
        "disabled": False,
    },
    "bob": {
        "username": "bob",
        "full_name": "bob builder",
        "email": "bobbuilder@example.com",
        "hashed_password": "$2b$12$BnnrukCZrCdtwZjlhae7Tej1DS6eKfc8kRqMRn6Qrkhs78lcIDmHi",
        "disabled": False,
    },
    "clementine": {
        "username": "clementine",
        "full_name": "clementine mandarine",
        "email": "clementinemandarine@example.com",
        "hashed_password": "$2b$12$bHPKCJIZi/S8uUZ8MUr30.d02VvfB/97W808dUY7WZU7o7Ju7tss.",
        "disabled": False,
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
   user = authenticate_user(fake_users_db, form_data.username, form_data.password)
   if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
   access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
   access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
   return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


#@app.get("/users/me/items/")
#async def read_own_items(current_user: User = Depends(get_current_active_user)):
#    return [{"item_id": "Foo", "owner": current_user.username}]

@app.post('/ridgepredict')
async def ridgepredict(bk: Bike, current_user: User = Depends(get_current_active_user)):

    """Renvoie le décompte de vélo prédit dans les conditions ci-dessous
    """
    df = pd.DataFrame([bk.dict()])

    prediction = ridgeModel.predict(df)
    #score = ridgeModel.score(bk_array, prediction[0])
    return {'prediction': prediction[0]}
    # , 'score': score

@app.post('/linearprediction')
async def linearprediction(bk: Bike, current_user: User = Depends(get_current_active_user)):
    """Renvoie le décompte de vélo prédit dans les conditions ci-dessous
    """
    df = pd.DataFrame([bk.dict()])
    prediction = linearModel.predict(df)
    #score = lineareModel.score(bk_array, prediction[0])
    return {'prediction': prediction[0]}
    #, 'score': score
@app.post('/randomforestprediction')
async def randomforestprediction(bk: Bike, current_user: User = Depends(get_current_active_user)):
    """Renvoie le décompte de vélo prédit dans les conditions ci-dessous
    """
    df = pd.DataFrame([bk.dict()])
    prediction = randomforestModel.predict(df)
    #score = decisiontreemodel.score(bk_array, prediction)
    return {'prediction': prediction[0]}
        #, 'score': score}

@app.post('/decisiontreeprediction')
async def decisiontreeprediction(bk: Bike, current_user: User = Depends(get_current_active_user)):
    """Renvoie le décompte de vélo prédit dans les conditions ci-dessous
    """
    df = pd.DataFrame([bk.dict()])
    prediction = decisiontreemodel.predict(df)
    return {'prediction': prediction[0]}


#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)