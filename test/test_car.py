import requests


def car():
    r = requests.get("http://localhost:33307/api/v1/action")
    print(r.text)


car()
