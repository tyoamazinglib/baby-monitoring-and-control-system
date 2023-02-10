import requests
import time
from antares_http import antares
import json

url = "http://10.254.239.1/other/"

r = requests.get(url, stream=True)

counter = 0

for chunk in r.iter_content(1024):
    chunk_str = str(chunk)
    counter += chunk_str.count('"best_match":"tyo"')
    print(counter)
    

r.close()

