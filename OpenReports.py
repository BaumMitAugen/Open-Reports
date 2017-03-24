#!/usr/bin/env python3

# This script will open all unhandled Natty reports in a new Firefox window

import requests
import json as js
import rfc3987
from subprocess import call

prefix = 'https://stackoverflow.com/a/'

remote = requests.get('http://samserver.bhargavrao.com:8000/napi/api/reports/all?filter=010000')
remote.raise_for_status()

data = js.loads(remote.text)
links = [item['link'] for item in data['items']]

if not all((rfc3987.match(link, rule='IRI') and link[:len(prefix)] == prefix) for link in links):
    raise RuntimeError('Invalid link received')

if len(links) == 1:
    call(['firefox', '-new-window'] + links)
elif len(links) > 1:
    call(['firefox'] + links)
else:
    print('All reports have been tended to.')


