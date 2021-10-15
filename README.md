# Projet Bike
L’objectif de ce projet est de déployer une API permettant de prédire décompte du nombre de vélos d'un jour au lendemain (bike).

Il se compose des éléments suivants :

* Un [script](https://github.com/bourrich90/Bike_project/blob/main/train/train.py) d'entrainement du modèle de machine learning.
* Une [api](https://github.com/bourrich90/Bike_project/blob/main/files/apibike.py), développée avec le framework FastAPI.

### Machine Learning
-----------------------------------------------------------------------
Pour lancer l'entrainement du modèle de machine learning placez vous dans le dossier train, installez les dépendances (dans un environnement virtuel dédié), puis exécutez le script train.py:

``` 
  cd train
  pip install -r requirments_train.txt
  python train.py
```

Le script train.py entraine 4 modéles : RandomForestRegressor , LinearRegression , Ridge et DecisionTreeRegressor,  enregistre (dans le dossier local) les modèles entrainés au format pickle (ecisiontreemodel.pkl , randomforestModel.pkl, ridgeModel.pkl, lineareModel.pkl ).

### API
============API==================

Pour lancer l'API , il faut se situer dans le chemin "https://github.com/bourrich90/Bike_project/tree/main/files" :

1. Installer les packages dans https://github.com/bourrich90/Bike_project/blob/main/files/requirements.txt et Lancer le script https://github.com/bourrich90/Bike_project/blob/main/files/apibike.py qui contient le serveur uvicorn.
2. Ouvrir l'interface : http://localhost:8000/docs pour voir les différents endpoints
3. Cliquer sur Authorize pour s’authentifier  , utiliser ces login/pwd : alice/wonderland, bob/builder , clementine/mandarine
4. Tester les endpoints : 
* /status ==> renvoie 1
* /performances ==> renvoie les performances des différents modéles
* /{username} ==> renvoie le login authentifié
* /ridgepredict ==> Renvoie le décompte de vélo prédit dans les conditions données (cf fichier https://github.com/bourrich90/Bike_project/blob/main/text.txt )

============Docker==================

Pour lancer les test conteneurisées de l'API , il faut se situer dans le chemin "https://github.com/bourrich90/Bike_project/tree/main/tests" :

1. Lancer docker-compose up
2. en cas d'erreur , lancer : lance docker-compose up -d , ensuite aprés qulques secondes  relancer une  deuxième tentative de docker-compose up

============Kubernetes==================

Pour lancer le deploiment de pods avec Kubernetes , il faut se situer dans le chemin "https://github.com/bourrich90/Bike_project/tree/main/Kubernetes" :

kubectl create -f my-deployment.yml
kubectl create -f my-ingress.yml
kubectl create -f my-servicel.yml
