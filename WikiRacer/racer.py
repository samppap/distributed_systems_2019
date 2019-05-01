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
import api

from collections import OrderedDict
from multiprocessing import cpu_count
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from concurrent.futures import ProcessPoolExecutor, as_completed

log = logging.getLogger(__name__)

class WikiRacer:

    def __init__(self):
        # Cache to hold links for node(page title)
        self.link_cache = {}
        # All paths found by Breadth-first search
        self.paths = []
        # API
        self.wiki_api_client = api.WikiApi()

    def _fetch_links_for_nodes(self, nodes):
        # Fetches all links


        # Create process pool(multiprocessing avoids python GIL)
        # with as many processes as cpu cores
        with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
            # Dictonary for storing future objects return by executor
            futures = {}

            # For each node(page title) if the node is not already cached
            # submit job to executor to fetch links
            for node in nodes:
                if not self.link_cache.get(node):
                    futures[executor.submit(
                        self.wiki_api_client.fetch_page_links, node)] = node

            # 'as_completed' returns the result of each future
            # as and when it is completed
            for future in as_completed(futures):
                try:
                    if future.done():
                        # Fetch the result of future and update cache
                        links = future.result()
                        self.link_cache[node] = links
                except Exception as e:
                    self.link_cache[node] = []
                    log.error(e.reason)

        executor.shutdown(wait=True)

    def _find_path_to_destination(self, page_title, end_title, path):
        # Determines if the page is the final destination


        if page_title == end_title:
            newpath = path + [page_title]
            if newpath not in self.paths:
                self.paths.append(newpath)
                return newpath

        return False

    def bfs(self, start_title, end_title):
        #Find all the paths between first and end page


        # Queue which holds tuple of the starting page title and path formed
        queue = [(start_title, [start_title])]

        # While queue is not empty perfrom Breadth-first search on popped node from queue
        while queue:
            vertex, path = queue.pop(0)

            # Fetch all links of nodes(page titles) parallely
            self._fetch_links_for_nodes(path)

            # For each node in path get all the links on page and
            # compare against destination page title
            for node in set(path) - set(vertex):
                # Fetch links for page title from cache
                links = self.link_cache[node]
                # Iterate over links and find destination
                for page_title in links:
                    wpath = self._find_path_to_destination(
                                page_title, end_title, path
                            )
                    # If path has been found yield to caller
                    # else append path found till now to queue
                    if wpath:
                        yield wpath
                    else:
                        queue.append((page_title, path + [page_title]))
