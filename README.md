# Bike_project
This repository is dedicated for Bike project developed within Datascientist.com training . The purpose was to deploy a ML model in FastAPI and test it using docker and at last deploy our app on 3 pods using kubernetes

============API==================

Pour lancer l'API , il faut se situer dans le chemin "https://github.com/bourrich90/Bike_project/tree/main/files" :
1. Lancer le script apibike.py qui contienne le serveur uvicorn.
2. Ouvrir l'interface : http://localhost:8000/docs pour voir les différents endpoints
3. Cliquer sur Authorize pour s’authentifier  , utiliser ces login/pwd : alice/wonderland, bob/builder , clementine/mandarine
4. Tester les endpoints : 
* /status ==> renvoie 1
* /performances ==> renvoie les performances des différents modéles
* /{username} ==> renvoie le login authentifié
* /ridgepredict ==> Renvoie le décompte de vélo prédit dans les conditions données (cf fichier https://github.com/bourrich90/Bike_project/blob/main/text.txt )

