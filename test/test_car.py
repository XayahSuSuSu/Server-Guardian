import json

import requests


def car():
    r = requests.get("http://118.24.139.23:33307/api/v1/action")
    body = json.loads(r.text)
    action = body['data']
    print(action['action'])


while True:
    car()
