import os
import requests
from base64 import b64encode

# définition de l'adresse de l'API
api_address = 'localhost'
# port de l'API
api_port = 8000

# data_pred = {"hum_min": 0.44,"hum_max": 0.69,"hum_mean": 0.577500,"hum_q25": 0.5325,"hum_q50": 0.595,"hum_q75": 0.6400,
#            "windspeed_min": 6.0032,"windspeed_max": 15.0013,"windspeed_mean": 10.374671,"windspeed_q25": 8.998100,"windspeed_q50": 11.00140,"windspeed_q75": 12.998000,
#            "temp_min": -1.42,"temp_max": 5.16,"temp_mean": 2.144167,"temp_q25": -0.48,"temp_q50": 2.81,"temp_q75": 4.220,
#            "atemp_min": -6.0010,"atemp_max": 3.0014,"atemp_mean": -1.249825,"atemp_q25": -4.00120,"atemp_q50": -0.9982,"atemp_q75": 1.25075,
#            "clear": 0.500000,"cloudy": 0.500000,"rainy": 0,"snowy": 0,
#            "cnt": 2729,"cnt_j_1": 1796,"cnt_j_2": 1341,"cnt_j_3": 3095,"cnt_j_4": 2114,"cnt_j_5": 441,"cnt_j_6": 1013,"cnt_j_7": 920}
#
# data_user = {'grant_type' : '','username' : 'alice','password' : 'wonderland','scope' : '','client_id' : '','client_secret' : ''}

username = 'alice'
password = 'wonderland'
encoded_credentials = b64encode(bytes(f'{username}:{password}', encoding='ascii')).decode('ascii')
auth_header = f'Basic {encoded_credentials}'


username1 = 'bob1'
password1 = 'builde1'
encoded_credentials1 = b64encode(bytes(f'{username1}:{password1}', encoding='ascii')).decode('ascii')
auth_header1 = f'Basic {encoded_credentials1}'


# requête 1
r1 = requests.get(
    url='http://{address}:{port}/username'.format(address=api_address, port=api_port), verify=False,
    headers={'Authorization' : str(auth_header)})
    #auth=('alice', 'wonderland')

# requête 2
r2 = requests.get(
    url='http://{address}:{port}/username'.format(address=api_address, port=api_port), verify=False,
    headers={'Authorization' : str(auth_header1)})

output = '''
============================

Authentication test
============================

request done at "/token"
| username="alice"
| password="wonderland"

expected result = 200
actual restult = {status_code_r1}


==>  {test_status_r1}


    prediction test
============================

request done at "/linearprediction"


expected result = 200
actual restult = {status_code_r2}

==>  {status_code_r2}

'''

# statut de la requête
status_code_r1 = r1.status_code
status_code_r2 = r2.status_code


# affichage des résultats
if status_code_r1 == 200:
    test_status_r1 = 'SUCCESS'
else:
    test_status_r1 = 'FAILURE'

if status_code_r2 == 200:
    test_status_r2 = 'SUCCESS'
else:
    test_status_r2 = 'FAILURE'

print(output.format(status_code_r1=status_code_r1, test_status_r1=test_status_r1,
                    status_code_r2=status_code_r2, test_status_r2=test_status_r2,
                    ))

# impression dans un fichier
if os.environ.get('LOG') == '1':
    with open('logs/api_test.log', 'a') as file:
        file.write(output)
