import os
import requests
from base64 import b64encode
import json

# définition de l'adresse de l'API
api_address = 'fastapi_from_compose'
# port de l'API
api_port = 8000

data_pred= json.dumps({"hum_min": 0.44,"hum_max": 0.69,"hum_mean": 0.577500,"hum_q25": 0.5325,"hum_q50": 0.595,"hum_q75": 0.6400,
                       "windspeed_min": 6.0032,"windspeed_max": 15.0013,"windspeed_mean": 10.374671,"windspeed_q25": 8.998100,"windspeed_q50": 11.00140,"windspeed_q75": 12.998000,
                       "temp_min": -1.42,"temp_max": 5.16,"temp_mean": 2.144167,"temp_q25": -0.48,"temp_q50": 2.81,"temp_q75": 4.220,
                       "atemp_min": -6.0010,"atemp_max": 3.0014,"atemp_mean": -1.249825,"atemp_q25": -4.00120,"atemp_q50": -0.9982,"atemp_q75": 1.25075,
                       "clear": 0.500000,"cloudy": 0.500000,"rainy": 0,"snowy": 0,
                       "cnt": 2729,"cnt_j_1": 1796,"cnt_j_2": 1341,"cnt_j_3": 3095,"cnt_j_4": 2114,"cnt_j_5": 441,"cnt_j_6": 1013,"cnt_j_7": 920})

username = 'alice'
password = 'wonderland'
encoded_credentials = b64encode(bytes(f'{username}:{password}', encoding='ascii')).decode('ascii')
auth_header = f'Basic {encoded_credentials}'

# requête 1
r1 = requests.post(
    url='http://{address}:{port}/ridgepredict'.format(address=api_address, port=api_port),
    headers={'Content-Type': 'application/json', 'Authorization': str(auth_header)}
    , data=data_pred)

#requête 2
r2 = requests.post(
    url='http://{address}:{port}/linearprediction'.format(address=api_address, port=api_port),
    headers={'Content-Type': 'application/json', 'Authorization': str(auth_header)}
    , data=data_pred)

#requête 3
r3 = requests.post(
    url='http://{address}:{port}/randomforestprediction'.format(address=api_address, port=api_port),
    headers={'Content-Type': 'application/json', 'Authorization': str(auth_header)}
    , data=data_pred)

#requête 4
r4 = requests.post(
    url='http://{address}:{port}/decisiontreeprediction'.format(address=api_address, port=api_port),
    headers={'Content-Type': 'application/json', 'Authorization': str(auth_header)}
    , data=data_pred)


output = '''
============================
    prediction test
============================

request done at "/ridgepredict"
| username="alice"
| password="wonderland"

expected result = 200
actual result = {status_code_r1}

==> ridge prediction : {response_r1}

request done at "/linearprediction"
| username="alice"
| password="wonderland"

expected result = 200
actual result = {status_code_r2}

==> linear  prediction : {response_r2}

request done at "/randomforestprediction"
| username="alice"
| password="wonderland"

expected result = 200
actual result = {status_code_r3}

==> random forest  prediction : {response_r3}

request done at "/decisiontreeprediction"
| username="alice"
| password="wonderland"

expected result = 200
actual restult = {status_code_r4}

==> decision tree  prediction : {response_r4}

'''


# statut de la requête
status_code_r1 = r1.status_code
status_code_r2 = r2.status_code
status_code_r3 = r3.status_code
status_code_r4 = r4.status_code

# réponse de la requête
response_r1 = r1.json()['prediction']
response_r2 = r2.json()['prediction']
response_r3 = r3.json()['prediction']
response_r4 = r4.json()['prediction']

# affichage des résultats
if status_code_r1 == 200:
    test_status_r1 = 'SUCCESS'
else:
    test_status_r1 = 'FAILURE'

if status_code_r2 == 200:
    test_status_r2 = 'SUCCESS'
else:
    test_status_r2 = 'FAILURE'

if status_code_r3 == 200:
    test_status_r3 = 'SUCCESS'
else:
    test_status_r3 = 'FAILURE'

if status_code_r4 == 200:
    test_status_r4 = 'SUCCESS'
else:
    test_status_r4 = 'FAILURE'

print(output.format(status_code_r1=status_code_r1, test_status_r1=test_status_r1,
                    status_code_r2=status_code_r2, test_status_r2=test_status_r2,
                    status_code_r3=status_code_r3, test_status_r3=test_status_r3,
                    status_code_r4=status_code_r4, test_status_r4=test_status_r4,
                    response_r1=response_r1, response_r2=response_r2, response_r3=response_r3, response_r4=response_r4))

# impression dans un fichier
if os.environ.get('LOG') == '1':
    with open('logs/api_test.log', 'a') as file:
        file.write(output)
