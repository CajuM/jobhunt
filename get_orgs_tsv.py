#!/usr/bin/env python

import multiprocessing as mp
import os
import sys

import requests

from lxml import etree

def sorry():
    os.system('./sorry.sh')

def work(org):
    if org in ['updates', 'contexts']:
        return {'rc': 0, 'org': org, 'url': '', 'location': '', 'stars': []}

    try:
        resp = requests.get(f'https://github.com/{org}', timeout=25)

    except Exception as e:
        return {'rc': -1, 'org': org}

    if not resp.text.strip():
        return {'rc': -2, 'org': org}

    if 'Not Found' in resp.text:
        return {'rc': 0, 'org': org, 'url': '', 'location': '', 'stars': []}

    doc = etree.HTML(resp.text)

    meta = doc.xpath('//meta[@name="route-action" and (@content="sso" or @content="new")]')
    if len(meta) > 0:
        return {'rc': 0, 'org': org, 'url': '', 'location': '', 'stars': []}

    meta = doc.xpath('//meta[@name="analytics-location"]/@content')
    if len(meta) != 1:
        return {'rc': -3, 'org': org}

    if meta[0] != '/<org-login>':
        return {'rc': 0, 'org': org, 'url': '', 'location': '', 'stars': []}

    url = doc.xpath('//a[@itemprop="url"]/@href')
    if len(url) != 1:
        url = ''
    else:
        url = url[0]

    location = doc.xpath('//span[@itemprop="location"]/text()')
    if len(location) != 1:
        location = ''
    else:
        location = location[0]

    stars = doc.xpath('//a[@class="pinned-item-meta Link--muted"]/text()')
    stars = [star.strip() for star in stars if star.strip()]
    
    return {'rc': 0, 'org': org, 'url': url, 'location': location, 'stars': stars}

def main(workers):
    workers = int(workers)

    jobs = [org.strip() for org in sys.stdin]

    stack = jobs[:workers]
    del jobs[:workers]

    with mp.Pool(workers) as p:
        while len(stack) > 0:
            ret = p.map(work, stack)

            sorry()

            failed = []
            for r in ret:
                if r['rc'] != 0:
                    failed.append(r['org'])
                    print(r['org'], r['rc'], file=sys.stderr)
                    continue

                org = r['org']
                url = r['url']
                location = r['location']
                stars = ','.join(r['stars'])

                print(f'{org}\t{url}\t{location}\t{stars}')

            n_failed = len(failed)
            stack = failed + jobs[:workers - n_failed]

            del jobs[:workers - n_failed]

if __name__ == '__main__':
    main(sys.argv[1])
