import requests

file = {'file': ('reid.npy', open('../asserts/reid/reid.npy','rb'))}

print(requests.post('http://118.24.139.23:33307/api/v1/reid', files=file))
