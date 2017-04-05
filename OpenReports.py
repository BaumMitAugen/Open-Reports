#!/usr/bin/env python3

# This script will open all unhandled Natty reports in a new Firefox window

import requests
import json as js
import webbrowser
from argparse import ArgumentParser

apiUrl = 'http://reports.socvr.org/api/create-report'
filename = '.report_data.txt'

def getData():
    prefix = 'https://stackoverflow.com/a/'

    remote = requests.get('http://samserver.bhargavrao.com:8000/napi/api/reports/all')
    remote.raise_for_status()

    data = js.loads(remote.text)
    return data['items']

def buildReport(reports):
    ret = {'botName' : 'OpenReportsScript'}
    posts = []
    for v in reports:
        posts.append([{'id':'title', 'name':v['name'], 'value':v['link'], 'specialType':'link'},
            {'id':'score', 'name':'NAA Score', 'value':v['naaValue']}])
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

reports = getData()
curr = [v['name'] for v in reports]

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
    good = [v for v in reports if not v['name'] in ignored]
    numIgnored = len(curr) - len(good)
    if numIgnored:
        print('Skipped %s ignored reports.'%numIgnored)
    openLinks(good)

