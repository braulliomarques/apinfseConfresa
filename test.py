import requests

url = "http://172.28.229.102:5000/download_notas"

payload = {
    "cnpj": "00149146000101",
    "senha": "Mago@2025",
    "data_inicio": "01/03/2025",
    "data_fim": "25/03/2025"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

# Verifica se a resposta está ok
if response.status_code == 200:
    with open("notas.zip", "wb") as f:
        f.write(response.content)
    print("✅ Arquivo salvo como notas.zip")
else:
    print(f"❌ Erro {response.status_code}: {response.text}")
