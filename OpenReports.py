#!/usr/bin/env python3

# Creates a socvr report with all unhandled Natty reports and maintains an ignore list

import requests
import json as js
import webbrowser
from argparse import ArgumentParser

apiUrl = 'http://reports.socvr.org/api/create-report'

def _getData():
    remote = requests.get('http://samserver.bhargavrao.com:8000/napi/api/reports/all')
    remote.raise_for_status()

    data = js.loads(remote.text)
    return data['items']

def _buildReport(reports):
    ret = {'botName' : 'OpenReportsScript'}
    posts = []
    for v in reports:
        reasons = ', '.join(r['reasonName'] for r in v['reasons'])
        posts.append([{'id':'title', 'name':v['name'], 'value':v['link'], 'specialType':'link'},
            {'id':'score', 'name':'NAA Score', 'value':v['naaValue']},
            {'id':'reasons', 'name':'Reasons', 'value':reasons}])
    ret['posts'] = posts
    return ret

def OpenLinks(reports, local = False):
    if len(reports) == 0:
        if local:
            print('All reports have been tended to.')
        return None
    report = _buildReport(reports)
    
    r = requests.post(apiUrl, data=js.dumps(report))
    r.raise_for_status()
    if local:
        webbrowser.open(r.text)
        return None
    else:
        return r.text

def OpenReports(mode='normal', local=False, userID=None):
    if userID:
        filename = str(userID) + '.ignorelist'
    else:
        filename = '.report_data.txt'
    reports = _getData()
    curr = [v['name'] for v in reports]

    try:
        dataFile = open(filename)
        ignored = [v for v in dataFile.readline().split()]
        last = [v for v in dataFile.readline().split()]
        dataFile.close()
    except:
        ignored = []
        last = []

    if mode == 'ignore_rest':
        newIgnored = [v for v in last if v in curr]
        f = open(filename, 'w')
        f.write(' '.join(newIgnored))
        f.write('\n')
        f.write(' '.join(last))
        msg = str(len(newIgnored)) + ' reports in ignore list.'
        if local:
            print(msg)
        else:
            return msg
    else:
        good = [v for v in reports if not v['name'] in ignored]
        numIgnored = len(curr) - len(good)
        if mode == 'fetch_amount':
            msg = 'There ' + ('is ' if len(curr) == 1 else 'are ') + str(len(curr)) \
                    + ' unhandled ' + ('report' if len(curr) == 1 else 'reports') \
                    + ', %s of which '%numIgnored \
                    + ('is' if numIgnored == 1 else 'are') + ' on your ignore list.'
            if local:
                print (msg)
            else:
                return msg
        else:
            f = open(filename, 'w')
            f.write(' '.join(ignored))
            f.write('\n')
            f.write(' '.join(curr))
            msg = ''
            if numIgnored:
                if local:
                    print('Skipped %s ignored reports.'%numIgnored)
                else:
                    msg = 'Skipped %s ignored reports. '%numIgnored
            report = OpenLinks(good, local)
            if not local:
                if not good:
                    msg += 'All reports have been tended to.'
                else:
                    msg += 'Opened %s [report%s](%s).'%(len(good),'' if len(good) == 1 else 's', report)
            return msg

if __name__ == '__main__':
    parser = ArgumentParser(description = 'Interface to Natty reports')
    parser.add_argument('-ir', '--ignore-rest', action='store_true',
                    help='Add all unhandled reports from the last batch to your ignore list')
    parser.add_argument('-fa', '--fetch-amount', action='store_true',
                    help='Only show the number of reports')
    args = parser.parse_args()

    mode = 'normal'
    if args.ignore_rest:
        mode = 'ignore_rest'
    if args.fetch_amount:
        mode = 'fetch_amount'

    OpenReports(mode, True)
