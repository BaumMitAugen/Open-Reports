#!/usr/bin/env python3

# This script will open all unhandled Natty reports in a new Firefox window

import requests
import json as js
import rfc3987
import webbrowser
from argparse import ArgumentParser

apiUrl = 'http://reports.socvr.org/api/create-report'
filename = '.report_data.txt'

def getLinks():
    prefix = 'https://stackoverflow.com/a/'

    remote = requests.get('http://samserver.bhargavrao.com:8000/napi/api/reports/all?filter=010000')
    remote.raise_for_status()

    data = js.loads(remote.text)
    links = [item['link'] for item in data['items']]
    ids = [item['name'] for item in data['items']]

    if len(links) != len(ids):
        raise RuntimeError('Invalid data received')

    if not all((rfc3987.match(link, rule='IRI') and link[:len(prefix)] == prefix) for link in links):
        raise RuntimeError('Invalid link received')

    return ids, links

def buildReport(reports):
    ret = {'botName' : 'OpenReportsScript'}
    posts = []
    for i,l in reports:
        posts.append([{'id':'title', 'name':i, 'value':l, 'specialType':'link'}])
    ret['posts'] = posts
    return ret

def openLinks(reports):
    if len(reports) == 0:
        print('All reports have been tended to.')
        return
    report = buildReport(reports)
    r = requests.post(apiUrl, json=report)
    r.raise_for_status()
    webbrowser.open(r.text)

parser = ArgumentParser(description = 'Interface to Natty reports')
parser.add_argument('-ir', '--ignore-rest', action='store_true',
                help='Ignore all unhandled reports from the last run in the future')
args = parser.parse_args()

curr, links = getLinks()

try:
    dataFile = open(filename)
    ignored = [v for v in dataFile.readline().split()]
    last = [v for v in dataFile.readline().split()]
    dataFile.close()
except:
    ignored = []
    last = []

if args.ignore_rest:
    newIgnored = [v for v in last if v in curr]
    f = open(filename, 'w')
    f.write(' '.join(newIgnored))
    f.write('\n')
    f.write(' '.join(last))
    print(str(len(newIgnored)) + ' reports in ignore list.')
else:
    f = open(filename, 'w')
    f.write(' '.join(ignored))
    f.write('\n')
    f.write(' '.join(curr))
    good = [(i,l) for i, l in zip(curr, links) if not i in ignored]
    numIgnored = len(curr) - len(good)
    if numIgnored:
        print('Skipped %s ignored reports.'%numIgnored)
    openLinks(good)

