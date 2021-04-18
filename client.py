import requests

payload = {'key':5}

r = requests.post('http://127.0.0.1:5000/', json=payload)

print(r.json())
