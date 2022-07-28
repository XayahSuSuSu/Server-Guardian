import requests

with open('test.npy', 'wb') as f:
    f.write(requests.get('http://118.24.139.23:33307/asserts/reid/reid.npy').content)
