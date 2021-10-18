# Projet Bike
L’objectif de ce projet est de déployer une API permettant de prédire décompte du nombre de vélos d'un jour au lendemain (bike).

Il se compose des éléments suivants :

* Un [script](https://github.com/bourrich90/Bike_project/blob/main/train/train.py) d'entrainement du modèle de machine learning.
* Une [api](https://github.com/bourrich90/Bike_project/blob/main/files/apibike.py), développée avec le framework FastAPI.

## Machine Learning

Pour lancer l'entrainement du modèle de machine learning placez vous dans le dossier train, installez les dépendances (dans un environnement virtuel dédié), puis exécutez le script train.py:

``` 
  cd train
  pip install -r requirments_train.txt
  python train.py
```

Le script train.py entraine 4 modéles : RandomForestRegressor , LinearRegression , Ridge et DecisionTreeRegressor,  enregistre (dans le dossier local) les modèles entrainés au format pickle (decisiontreemodel.pkl , randomforestModel.pkl, ridgeModel.pkl, lineareModel.pkl ).

## API

Après avoir entrainé les modèle de ML, nous souhaitons développer une API HTTP permettant d'interagir avec le modèle afin d'obtenir une prédiction à partir des features.

Cette API est développée avec le framework [FastAPI](https://fastapi.tiangolo.com/) dans le dossier [files](https://github.com/bourrich90/Bike_project/tree/main/files). Elle est composée des fichiers suivants :

 * [apibike.py](https://github.com/bourrich90/Bike_project/blob/main/files/apibike.py): fichier principal, qui définit les routes de prediction POST /ridgepredict ,/linearprediction, /randomforestprediction et /decisiontreeprediction .
 * [Bikes.py](https://github.com/bourrich90/Bike_project/blob/main/files/Bikes.py): définit les modèles de données attendus en entrée de l'API.
 * [decisiontreemodel.pkl](https://github.com/bourrich90/Bike_project/blob/main/files/decisiontreemodel.pkl) : le modèle decision tree de ML entrainé, au format pickle.
 * [lineareModel.pkl](https://github.com/bourrich90/Bike_project/blob/main/files/lineareModel.pkl) : le modèle linear de ML entrainé, au format pickle.
 * [randomforestModel.pkl](https://github.com/bourrich90/Bike_project/blob/main/files/randomforestModel.pkl) : le modèle random forest de ML entrainé, au format pickle.
 * [ridgepredict.pkl](https://github.com/bourrich90/Bike_project/blob/main/files/ridgeModel.pkl) : le modèle ridge de ML entrainé, au format pickle.
 * [requirements.txt](https://github.com/bourrich90/Bike_project/blob/main/files/requirements.txt) : dépendances Python.

Les modèles sont chargés au lancement de l'API :

```javascript
# chargement des modéles
loaded_lineareModel = open("lineareModel.pkl", "rb")
lineareModel = joblib.load(loaded_lineareModel)

loaded_ridgeModel = open("ridgeModel.pkl", "rb")
ridgeModel = joblib.load(loaded_ridgeModel)

loaded_randomforestModel = open("randomforestModel.pkl", "rb")
randomforestModel = joblib.load(loaded_randomforestModel)

loaded_decisiontreemodel = open("decisiontreemodel.pkl", "rb")
decisiontreemodel = joblib.load(loaded_decisiontreemodel)
```
Et sont utilisés au moment d'une requête POST /endpoint pour faire la prédiction à partir des features :
```javascript
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
```
Pour lancer l'API, exécutez les commandes suivantes :
``` 
  cd files
  pip install -r requirments.txt
  python apibike.py
```
L'API est désormais accessible à l'adresse localhost:8000.
En particulier, vous pouvez accéder à la documentation de l'API à l'adresse [localhost:8000/docs](http://localhost:8000/docs) 
![prjetc_bike1](https://user-images.githubusercontent.com/86717947/137695180-6244b7b4-419f-4f14-ace7-f8396faf3e85.PNG)
![projet_bike2](https://user-images.githubusercontent.com/86717947/137695731-f22ec2ee-57fe-4177-97c8-c1aabcb7cfe7.PNG)
![projet_bike3](https://user-images.githubusercontent.com/86717947/137695764-9b968906-ded8-4b9b-ac04-773447a53045.PNG)

#### Docker:

Vous pouvez également lancer l'API avec Docker, en buildant préalablement l'image Docker définie dans le [Dockerfile](https://github.com/bourrich90/Bike_project/blob/main/Dockerfile):

``` 
  docker build -t bike-api .
  docker run -p 8000:8000 --rm bike-api
```

## Tests

Afin de s'assurer facilement que l'API est fonctionnelle, nous avons développé une série de tests dans le dossier [tests](https://github.com/bourrich90/Bike_project/tree/main/tests).

Ces tests permettent notamment de s'assurer que :

* L'authentification est fonctionnelle. C'est à dire qu'une requête envoyée sans credentials ou avec des credentials erronés renverra une erreur 401.
* La validation du schéma est fonctionnelle. C'est à dire qu'une requête dont le corps n'est pas conforme au schéma attendu renverra une erreur 422.

#### Docker compose:

Vous pouvez  lancez l'API et les tests directement grâce à [docker-compose]() :
```
cd tests
docker-compose up --build
```


