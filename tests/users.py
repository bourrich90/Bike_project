import os
import requests
from base64 import b64encode

# définition de l'adresse de l'API
api_address = 'fastapi_from_compose'
# port de l'API
api_port = 8000

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

users test
============================

request done at "/username"
| username="alice"
| password="wonderland"

expected result = 200
actual restult = {status_code_r1}


==>   username: {response_r1}

============================

request done at "/username"


expected result = 401
actual restult = {status_code_r2}

==>  username: {response_r1}

'''

# statut de la requête
status_code_r1 = r1.status_code
status_code_r2 = r2.status_code

# réponse de la requête
response_r1 = r1.text
response_r2 = r2.text

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
                    response_r1=response_r1, response_r2=response_r2))

# impression dans un fichier
if os.environ.get('LOG') == '1':
    with open('logs/api_test.log', 'a') as file:
        file.write(output)
