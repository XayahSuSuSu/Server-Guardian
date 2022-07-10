import requests


def app():
    form = {
        'action': 'forward',
        'state': ''
    }
    r = requests.post("http://118.24.139.23:33307/api/v1/action", data=form)
    print(r.text)


app()
