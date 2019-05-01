#! /usr/bin/env python3

#Samuel Pitkanen 0455564
#Distributed Systems 2019

"""
Implement a distributed system that finds the shortest way between
two Wikipedia pages provided as an input.
The system should consist of several workers that parse Wikipedia pages.

"""

import argparse
import json
import logging
import re
import sys

from collections import OrderedDict
from multiprocessing import cpu_count
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from concurrent.futures import ProcessPoolExecutor, as_completed

log = logging.getLogger(__name__)

wikipedia_api = 'https://en.wikipedia.org/w/api.php?'


class WikiApi:

    def fetch_page_links(self, page_title,
                         format='json', limit=500,
                         title_filter='(Category:|Template:|Template_talk:)'):

        #Fetches all links in the wikipedia page


        page_links = []

        # API params for fetching wikipedia page links
        params = urlencode({'action': 'query',
                            'prop': 'links',
                            'titles': page_title,
                            'pllimit': limit,
                            'format': format})
        url = wikipedia_api + params

        # Run query by opening the api url to fetch links
        try:
            page = urlopen(url)
        except (URLError, HTTPError) as e:
            log.error(url + ": %s" % e.reason)
            return []

        # Read the results of query api and decode to utf-8
        try:
            json_data = page.read().decode('utf-8')
        except UnicodeError as e:
            log.error("UnicodeError: %s" % e)
            json_data = []

        if not json_data:
            return []

        # Convert str JSON data to python dict
        try:
            links = json.loads(json_data)
        except json.JSONDecodeError as e:
            log.error("Failure while trying to parse result from wiki api")
            log.error("JSONDecodeError: %s" % e)
            return []

        # From the result collect only the page title after applying
        # title_filter
        for pageid in links['query']['pages']:
            if links['query']['pages'][pageid].get('links'):
                for link in links['query']['pages'][pageid]['links']:
                    page_title = link['title'].replace(' ', '_')
                    if not re.search(title_filter, page_title):
                        page_links.append(page_title)

        return page_links
