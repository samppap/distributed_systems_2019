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
import racer


from collections import OrderedDict
from multiprocessing import cpu_count
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from concurrent.futures import ProcessPoolExecutor, as_completed

log = logging.getLogger(__name__)

wikipedia_url = 'https://en.wikipedia.org'

def main():

    wikipediaUrl = "https://en.wikipedia.org/wiki/"
    print("")
    print("             WIKIRACER \n")
    # Get page title from user input
    start_page_title = input("Start page name (article name): ")
    end_page_title = input("End page name (article name): ")

    # Capitalize first letter + replace whitespace with underscore
    start_page_title = start_page_title.capitalize().replace(" ", "_")
    end_page_title = end_page_title.capitalize().replace(" ", "_")


    print("\n")
    print("First article:", wikipediaUrl  + start_page_title)

    print("Last article:", wikipediaUrl  + end_page_title)
    print("")

    # Find the path
    wikiracer = racer.WikiRacer()

    # Breadth-first search (BFS)
    bfs_gen = wikiracer.bfs(start_page_title, end_page_title)

    # Get the first path
    path = [wikipedia_url + '/' + node for node in next(bfs_gen)]

    # JSON output
    json_output = OrderedDict()
    json_output["Path"] = path
    print("")
    print("Result: ")
    print(json.dumps(json_output, indent=4))


if __name__ == '__main__':
    main()
