import os
import requests
from base64 import b64encode

# définition de l'adresse de l'API
api_address = 'localhost'
# port de l'API
api_port = 8000

data_pred={"hum_min": 0, "hum_max": 0, "hum_mean": 0, "hum_q25": 0, "hum_q50": 0, "hum_q75": 0,
            "windspeed_min": 0,"windspeed_max": 0,"windspeed_mean": 0,"windspeed_q25": 0,"windspeed_q50": 0,"windspeed_q75": 0,
            "temp_min": 0,"temp_max": 0,"temp_mean": 0,"temp_q25": 0,"temp_q50": 0,"temp_q75": 0,
            "atemp_min": 0,"atemp_max": 0,"atemp_mean": 0,"atemp_q25": 0,"atemp_q50": 0, "atemp_q75": 0,
            "clear": 0.5, "cloudy": 0.5, "rainy": 0, "snowy": 0,
            "cnt": 2729, "cnt_j_1": 1796, "cnt_j_2": 1341, "cnt_j_3": 3095, "cnt_j_4": 2114, "cnt_j_5": 441, "cnt_j_6": 1013, "cnt_j_7": 920}

username = 'alice'
password = 'wonderland'
encoded_credentials = b64encode(bytes(f'{username}:{password}', encoding='ascii')).decode('ascii')
auth_header = f'Basic {encoded_credentials}'

# requête 1
r1 = requests.post(
    url='http://{address}:{port}/ridgepredict'.format(address=api_address, port=api_port),
    headers={'Authorization': str(auth_header)}
    , data=data_pred
)




output = '''
============================
    prediction test
============================

request done at "/ridgepredict"
| username="alice"
| password="wonderland"

expected result = 200
actual restult = {status_code_r1}

==>  {test_status_r1}

'''

# statut de la requête
status_code_r1 = r1.status_code

# affichage des résultats
if status_code_r1 == 200:
    test_status_r1 = 'SUCCESS'
else:
    test_status_r1 = 'FAILURE'

print(output.format(status_code_r1=status_code_r1, test_status_r1=test_status_r1))

# impression dans un fichier
if os.environ.get('LOG') == '1':
    with open('logs/api_test.log', 'a') as file:
        file.write(output)
