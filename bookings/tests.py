from django.test import TestCase

# Create your tests here.

import requests

URL = "http://127.0.0.1:8000/api/login/"
DATA = {
    "username": "Fabrizio",
    "password": "1234"
}

try:
    response = requests.post(URL, json=DATA)
    response.raise_for_status()
    print("✅ Login riuscito!")
    print("Risposta:", response.json())
except requests.exceptions.RequestException as e:
    print("❌ Errore di connessione:", e)
    if response is not None:
        print("Codice stato:", response.status_code)
        print("Risposta:", response.text)
