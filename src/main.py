#!/usr/bin/env python3

import argparse
from simpycrawler import crawler

prs = argparse.ArgumentParser()
prs.add_argument('-u', '--url', action='store', default='', help='')
prs.add_argument('-i', '--urlcontains', action='store', default='', help='')
prs.add_argument('-e', '--urlnotcontains', action='store', default='', help='')
prs.add_argument('-g', '--geckodriver', action='store', default='', help='Path to geckodriver.')
prs.add_argument('-j', '--javascript', action='store_true', default=False, help='Enables javascript processing for AngularJS and similar technologies. It requires geckodriver setup.')
prs.add_argument('-f', '--filestorage', action='store_true', default=False, help='Enables to save the crawling progress. It is recommended for large projects.')
prs.add_argument('-r', '--resetstorage', action='store_true', default=False, help='Resets the saved crawling progress when the filestorage is active.')
prs.add_argument('-l', '--log', action='store_true', default=False, help='Enables logging.')
arg = prs.parse_args()

def pageanalyse(page, urls, html):
	pass

if __name__ == '__main__':
	crawler(pageanalyse, arg.url, arg.urlcontains, arg.urlnotcontains, arg.javascript, arg.geckodriver, arg.filestorage, arg.resetstorage, arg.log)
