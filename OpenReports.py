#!/usr/bin/env python3

import requests
import json as js
from subprocess import call

remote = requests.get('http://samserver.bhargavrao.com:8000/napi/api/reports/all?filter=010000')
data = js.loads(remote.text)
links = [item['link'] for item in data['items']]

if len(links) == 1:
    call(['firefox', '-new-window'] + links)
elif len(links) > 1:
    call(['firefox'] + links)
else:
    print('All reports have been tended too.')


