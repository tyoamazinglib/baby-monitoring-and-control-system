import requests
import time
from antares_http import antares
import json

antares.setAccessKey('65f708123a858355:7084ef0d7c21f8cd')

url = "http://unitv2.py/func/result"

r = requests.post(url, stream=True)


for chunk in r.iter_content(1024):
    try:
        json.dumps(chunk)
    except TypeError as e:
        print(e)
    data = chunk.decode('utf-8')
    print(json.dumps(data))
    antares.send(json.dumps(data), 'ProchizImageCounting', 'Counter')

r.close()

# jstring = json.dumps(chunk)
