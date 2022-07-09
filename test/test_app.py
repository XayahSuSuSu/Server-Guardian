import requests


def app():
    form = {
        'action': 'forward'
    }
    r = requests.post("http://localhost:33307/api/v1/action", data=form)
    print(r.text)


app()
