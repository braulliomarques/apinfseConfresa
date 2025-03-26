import requests

headers = {
    'Content-Type': 'application/json',
}

json_data = {
    'cnpj': 'cnpj',
    'senha': 'senha',
    'data_inicio': '01/01/2024',
    'data_fim': '31/03/2025',
}

response = requests.post('http://localhost:5000/download_notas', headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{\n    "cnpj": "00149146000101",\n    "senha": "SuaSenha",\n    "data_inicio": "01/01/2024",\n    "data_fim": "31/01/2024"\n  }'
#response = requests.post('http://localhost:5000/download_notas', headers=headers, data=data)

with open('notas.zip', 'wb') as f:
    f.write(response.content)