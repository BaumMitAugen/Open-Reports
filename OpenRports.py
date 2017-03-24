#!/usr/bin/env python3

from urllib.request import urlretrieve
import json as js
from subprocess import call

remote = urlretrieve('http://samserver.bhargavrao.com:8000/napi/api/reports/all?filter=010000')
tempFile = open(remote[0])
data = js.load(tempFile)
links = [item['link'] for item in data['items']]

if len(links) == 1:
    call(['firefox', '-new-window'] + links)
elif len(links) > 1:
    call(['firefox'] + links)
else:
    print('All reports have been tended too.')


