import os
import requests
from base64 import b64encode

# définition de l'adresse de l'API
api_address = 'localhost'
# port de l'API
api_port = 8000

username = 'alice1'
password = 'wonderlan1'
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

# requête 1
r1 = requests.get(
    url='http://{address}:{port}/performances'.format(address=api_address, port=api_port), verify=False,
    headers={'Authorization' : str(auth_header)})
    #auth=('alice', 'wonderland')


# requête 2
r2 = requests.get(
    url='http://{address}:{port}/performances'.format(address=api_address, port=api_port), verify=False,
    headers={'Authorization' : str(auth_header1)})

# requête 3
r3 = requests.get(
    url='http://{address}:{port}/performances'.format(address=api_address, port=api_port), verify=False,
    headers={'Authorization' :str(auth_header2)})


output = '''
============================
    Authentication test
============================

request done at "/performances"
| username="alice1"
| password="wonderland1"

expected result = 401
actual restult = {status_code_r1}

==>  {test_status_r1}

request done at "/performances"
| username="bob"
| password="builder"

expected result = 200
actual restult = {status_code_r2}

==>  {test_status_r2}

request done at "/performances"
| username="alice"
| password="clementine"

expected result = 200 
actual restult = {status_code_r3}

==>  {test_status_r3}

'''


# statut de la requête
status_code_r1 = r1.status_code
status_code_r2 = r2.status_code
status_code_r3 = r3.status_code


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

print(output.format(status_code_r1=status_code_r1, test_status_r1=test_status_r1,
status_code_r2=status_code_r2, test_status_r2=test_status_r2,
status_code_r3=status_code_r3, test_status_r3=test_status_r3))

# impression dans un fichier
if os.environ.get('LOG') == '1':
    with open('logs/api_test.log', 'a') as file:
        file.write(output)
