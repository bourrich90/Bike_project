# Bike_project
L’objectif de ce projet est de choisir, mettre en place, et peupler une base de données à partir d’un jeu de données de l’open data, et d’implémenter une API vous permettant de requêter cette base de données. 
This repository is dedicated for Bike project developed within Datascientist.com training . The purpose was to deploy a ML model in FastAPI and test it using docker and  deploy our app on 3 pods using kubernetes

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
