#!/usr/bin/env python3

from bs4 import BeautifulSoup as soup
from time import localtime, strftime
from urllib.parse import urlparse
import requests, sys, os, re

def crawler(callback, starturl, urlcontains, urlnotcontains, javascript, geckodriver, usestorage, resetstorage, log):
	
	crawled = []
	pages   = []
	
	geckobrowser = ''
	workspacefld = './simpycrawler/'
	excludefiles = '\.jpg|\.jpeg|\.png|\.gif|\.pdf|\.doc|\.docx|\.xls|\.xlsq|\.ppt|\.pptx|\.pps|\.ppsx|\.zip|\.rar|\.exe|\.mkv|\.avi|\.mp4|\.mp3|\.mpg'
	
	headers = { 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36' }
	
	def setglobals(url):
		global domain
		global prefix
	
		urlpars = urlparse(url)
		domain  = urlpars.scheme + '://' + urlpars.netloc
		prefix  = (urlpars.netloc).replace('.', '_')
	
	def preparefolder(folder):
		if not os.path.exists(folder):
			os.makedirs(folder)
	
	def storagesave(listname, url):
		if usestorage == True:
			preparefolder(workspacefld)
			with open(workspacefld + prefix + '_' + listname + '.txt', 'a') as f:
				f.write(str(url) + "\n")
	
	def storagedelete():
		if resetstorage == True:
			os.remove(workspacefld + prefix + '_pages.txt')
			os.remove(workspacefld + prefix + '_crawled.txt')
	
	def storageloadpages():
		for l in open(workspacefld + prefix + '_pages.txt', 'r'):
			pages.append(l.strip())
	
	def storageloadcrawled():
		for l in open(workspacefld + prefix + '_crawled.txt', 'r'):
			crawled.append(l.strip())
	
	def logging(message):
		if log == True:
			preparefolder(workspacefld)
			with open(workspacefld + prefix + '_log.txt', 'a') as f:
				f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + ' ' + message + "\n")
		
		print(message)
	
	def stargecko():
		from selenium import webdriver
		from selenium.webdriver.firefox.options import Options
		
		options = Options()
		options.set_headless(headless=True)
		
		firefox_profile = webdriver.FirefoxProfile()
		firefox_profile.set_preference('permissions.default.image', 2)
		firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
		
		nonlocal geckobrowser
		
		if geckodriver:
			geckobrowser = webdriver.Firefox(executable_path=geckodriver, firefox_options=options, firefox_profile=firefox_profile)
		else:
			geckobrowser = webdriver.Firefox(firefox_options=options, firefox_profile=firefox_profile)
	
	def closegecko():
		if geckobrowser:
			geckobrowser.close()
	
	def gethtmlcontent(url):
		if javascript == False:
			request  = requests.get(url, headers=headers, timeout=5)
			response = request.text
			request.close()
		else:
			if not geckobrowser:
				stargecko()
			
			geckobrowser.get(url)
			response = geckobrowser.execute_script('return document.body.innerHTML')
		
		return response
	
	def nominneteforcrawling(url):
		url = url.split('#')[0]
		if re.match('^/.*', url):
			url = domain + url
		
		if re.match('^' + domain + '/.*', url) and not re.search(excludefiles, url) and re.search(urlcontains, url) and (not urlnotcontains or not re.search(urlnotcontains, url)):
			addtopageslis(url)
	
	def addtopageslis(url):
		if url not in pages and url not in crawled:
			pages.append(url)
			storagesave('pages', url)
	
	def addtocrawled(url):
		if url not in crawled:
			crawled.append(url)
			storagesave('crawled', url)
	
	def setcrawler(url):
		setglobals(url)
		storagedelete()
		
		if usestorage == True and os.path.exists(workspacefld + prefix + '_pages.txt') and os.path.exists(workspacefld + prefix + '_crawled.txt'):
			storageloadcrawled()
			storageloadpages()
		else:
			nominneteforcrawling(url)
		
		startcrawler(pages)
		closegecko()
	
	def startcrawler(urls):
		for url in urls:
			if url not in crawled:
				htmldata  = gethtmlcontent(url)
				soupdata  = soup(htmldata, 'html.parser')
				pagelinks = soupdata.find_all('a', attrs={'href': re.compile('^https?\:\/\/|^\/')})
			
				for link in pagelinks:
					nominneteforcrawling(link.get('href'))
					
				addtocrawled(url)
			
				progresslog = '[SimPyCrawler][F' + str(len(pages)) + '][W' + str(len(pages) - len(crawled)) + '][P' + str(len(crawled)) + '] ' + url
				callback(url, pagelinks, htmldata)
				logging(progresslog)
				
				soupdata.clear()
	
	print('[SimPyCrawler][Version: 1.1][Author: Martin Kaspar www.martinkaspar.net]')
	setcrawler(starturl)
