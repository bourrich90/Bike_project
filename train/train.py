# import des bibliothéques

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from scipy import stats
import joblib

# charger le jeu de données bike 

data = pd.read_csv('https://assets-datascientest.s3-eu-west-1.amazonaws.com/de/total/bike.csv')
data['dteday'] = pd.to_datetime(data.dteday, format='%Y-%m-%d')

# ajout de la colonne weekday pour le jour de semaine
data["weekday"]=data["dteday"].dt.day_name()

# créons un jeu de données qui contient  que le décompte de vélo du jour J et 7 derniers jours pendant 24 heures
functions_to_apply = {
    
    'cnt' : 'sum'
}
cnt_data = data.groupby('dteday').agg(functions_to_apply)
cnt_data['cnt_j_1']=cnt_data['cnt'].shift(periods=1)
cnt_data['cnt_j_2']=cnt_data['cnt'].shift(periods=2)
cnt_data['cnt_j_3']=cnt_data['cnt'].shift(periods=3)
cnt_data['cnt_j_4']=cnt_data['cnt'].shift(periods=4)
cnt_data['cnt_j_5']=cnt_data['cnt'].shift(periods=5)
cnt_data['cnt_j_6']=cnt_data['cnt'].shift(periods=6)
cnt_data['cnt_j_7']=cnt_data['cnt'].shift(periods=7)

# remplaçons les valeurs nan par la mediane 
cnt_data = cnt_data.fillna(cnt_data.median())

# Fonctions quantiles a appliquer dans functions_to_apply

# 25th Percentile
def q25(x):
    return x.quantile(0.25)

# 50th Percentile
def q50(x):
    return x.quantile(0.5)

# 75th Percentile
def q75(x):
    return x.quantile(0.75)

# créons un jeu de données qui affiche le pourcentage de chaque classe du weathersit pendant 24 heures
weathersit_class = data.groupby('dteday').weathersit.value_counts(normalize=True).unstack().fillna(0)

# fonction functions_to_apply pour passer en arguement dans agg 
functions_to_apply = {
    
    'hum' : ['min','max','mean',q25,q50,q75],
    'windspeed' :['min','max','mean',q25,q50,q75],
    'temp' : ['min','max','mean',q25,q50,q75],
    'atemp' : ['min','max','mean',q25,q50,q75]
  
}
#jeu de données data_jour_annee_avant_concat 
data_jour_annee_avant_concat = data.groupby('dteday').agg(functions_to_apply)

#le nouveau jeu de données par jour de l'année est nommé 'data_jour_annee'
data_jour_annee = pd.concat([data_jour_annee_avant_concat,weathersit_class,cnt_data],axis=1)

# ajout de la variable 'cnt_lendemain' qui est le décompte de vélo  au jour n+1 au jeu de données data_jour_annee
data_jour_annee['cnt_lendemain'] = cnt_data['cnt'].shift(periods=-1)

# remplaçons les valeurs nan par la mediane 
data_jour_annee = data_jour_annee.fillna(data_jour_annee.median())

# informations des données data_jour_annee
data_jour_annee.info()

# 1.Préparation des données

# A partir du module model_selection de la librairie scikit learn on importe la fonction train_test_split
from sklearn.model_selection import train_test_split

# Instanciation du dataframe contenant les variables explicatives

X = data_jour_annee.drop(columns=['cnt_lendemain'])

# Instanciation de la serie contenant la variable cible 

y = data_jour_annee.cnt_lendemain

# Création d'un ensemble d'entraînement et d'un ensemble test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#2.Entraînement et évaluation du modèle regression linéaire

# A partir du module linear_model de la librairie scikit learn on importe la fonction LinearRegression

from sklearn.linear_model import LinearRegression 

# A partir du module model_selection de la librairie scikit learn on importe la fonction cross_validate et KFold

from sklearn.model_selection import cross_val_score, KFold, GridSearchCV

lrg_model =LinearRegression() 

#on utilise shuffle afin de mélanger les observations du dataset

lrg_folds = KFold(n_splits = 7, shuffle = True, random_state=42)

#Creation des paramétres grid
lrg_param_grid = {
   
    'fit_intercept': [True, False],
    'normalize': [True, False]
}

# Instantiation  du modéle de  grid search
lrg_grid_search = GridSearchCV(estimator = lrg_model, param_grid = lrg_param_grid,
                           cv=lrg_folds, n_jobs=-1, verbose=2, scoring='r2')

# Entrainement du modéle rf_model avec X_train
lrg_grid_search.fit(X_train, y_train)

# Vérification des meilleurs parametres de de grid_search 
print(lrg_grid_search.best_params_)

# Paramétres optimisés du modéle LinearRegression pour le meilleur estimateur
lrg_best_grid = lrg_grid_search.best_estimator_

# 3.Entraînement et évaluation du modèle RandomForest

# A partir du module ensemble de la librairie scikit learn on importe la fonction RandomForestRegressor

from sklearn.ensemble import RandomForestRegressor 

# A partir du module model_selection de la librairie scikit learn on importe la fonction cross_validate , KFold et GridSearchCV

from sklearn.model_selection import cross_val_score, KFold, GridSearchCV

#on utilise shuffle afin de mélanger les observations du dataset

rf_folds = KFold(n_splits = 7, shuffle = True, random_state=42)

# Creation du paramétres grid
rf_param_grid = {
    'max_features': ['auto','sqrt','log2'],
    'n_estimators': [100, 200, 300, 1000]
}

rf_model =RandomForestRegressor() 

# Instantiation  du modéle de  grid search
rf_grid_search = GridSearchCV(estimator = rf_model, param_grid = rf_param_grid,
                           cv=rf_folds, n_jobs=-1, verbose=2, scoring='r2')


# Entrainement du modéle rf_model avec X_train
rf_grid_search.fit(X_train, y_train)

# Vérification des meilleurs parametres de de grid_search 
print(rf_grid_search.best_params_)

# Paramétres optimisés du modéle randomforest pour le meilleur estimateur
rf_best_grid = rf_grid_search.best_estimator_

# 4.Entraînement et évaluation du modèle Ridge

# A partir du module linear_model de la librairie scikit learn on importe la fonction RandomForestRegressor

from sklearn.linear_model import Ridge

# A partir du module model_selection de la librairie scikit learn on importe la fonction cross_validate , KFold et GridSearchCV

from sklearn.model_selection import cross_val_score, KFold, GridSearchCV

#on utilise shuffle afin de mélanger les observations du dataset

ridge_folds = KFold(n_splits = 7, shuffle = True, random_state=42)

# Creation du paramétres grid
ridge_param_grid = {
    'solver': ['svd', 'cholesky', 'lsqr', 'sag'],
    'alpha': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100],
    'fit_intercept': [True, False],
    'normalize': [True, False]
}


ridge_model =Ridge() 

# Instantiation  du modéle de  grid search
ridge_grid_search = GridSearchCV(estimator = ridge_model, param_grid = ridge_param_grid,
                           cv=ridge_folds, n_jobs=-1, verbose=2, scoring='r2')


# Entrainement du modéle rf_model avec X_train
ridge_grid_search.fit(X_train, y_train)

# Paramétres optimisés du modéle Ridge pour le meilleur estimateur
ridge_best_grid = ridge_grid_search.best_estimator_

# 5.Entraînement et évaluation du modèle DecisionTreeRegressor

# A partir du module tree de la librairie scikit learn on importe la fonction DecisionTreeRegresso

from sklearn.tree import DecisionTreeRegressor

# A partir du module model_selection de la librairie scikit learn on importe la fonction cross_validate , KFold et GridSearchCV

from sklearn.model_selection import cross_val_score, KFold, GridSearchCV

#on utilise shuffle afin de mélanger les observations du dataset

dtr_folds = KFold(n_splits = 7, shuffle = True, random_state=42)

# Creation du paramétres grid
dtr_param_grid = {
    
    "min_samples_split": [10, 20, 40],
    "max_depth": [2, 6, 8],
    "min_samples_leaf": [20, 40, 100],
    "max_leaf_nodes": [5, 20, 100],
    
}

dtr_model =DecisionTreeRegressor() 

# Instantiation  du modéle de  grid search
dtr_grid_search = GridSearchCV(estimator = dtr_model, param_grid = dtr_param_grid,
                           cv=dtr_folds, n_jobs=-1, verbose=2, scoring='r2')


# Entrainement du modéle rf_model avec X_train
dtr_grid_search.fit(X_train, y_train)

# Paramétres optimisés du modéle DecisionTreeRegresso pour le meilleur estimateur
dtr_best_grid = dtr_grid_search.best_estimator_

# Sauvegarde des modéles

#sauvegarde du modéle decisiontree
decisiontreModel = open("decisiontreemodel.pkl","wb")
joblib.dump(dtr_best_grid,decisiontreModel)
decisiontreModel.close()

#sauvegarde du modéle randomforest
randomforestModel = open("randomforestModel.pkl","wb")
joblib.dump(rf_best_grid,randomforestModel)
randomforestModel.close()

#sauvegarde du modéle ridge
ridgeModel = open("ridgeModel.pkl","wb")
joblib.dump(ridge_best_grid,ridgeModel)
ridgeModel.close()

#sauvegarde du modéle linéaire
lineareModel = open("lineareModel.pkl","wb")
joblib.dump(lrg_best_grid,lineareModel)
lineareModel.close()

