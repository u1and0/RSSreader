# !/usr/bin/python3
# https://github.com/technoto/pyfeed/blob/master/feed.py

import re
import sys
from xml.etree import ElementTree as et
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.error import HTTPError

#with open('feeds.txt', 'r') as f:
#    feeds = f.read().splitlines()

un = lambda text: HTMLParser().unescape(text)


def menu(items):
	list_ = list(items)
	list_.insert(0, 'Go back')

	# print items with buttons
	for count in range(len(list_))[::-1]:
		button = '[%s]' % str(count)
		print(button, list_[count], '\n')

	# return the user's selection
	while True:
		try:
			selection = int(input())
			if selection == 0:
				return None
			else:
				return list_[selection]
		except (ValueError, IndexError):
			print('Type a number in the menu.')


def parse(url):
	'''parses xml url into title, description, and url'''

	# Get xml text
	try:
		r = urlopen(url)
	except HTTPError as e:
		print('Error:', e)
		input()
		return
	if r.status != 200:
		print('Error:', r.status)
		input()
		return
	else:
		text = r.read().decode()

	try:
		root = et.fromstring(text)
	except et.ParseError:
		print('Invalid feed data')
		return

	items = []
	for item in root.iter('item'):
		items.append(item)

	def getTitle(item):
		title = item.find('title').text
		return un(title)

	def getDescription(item):
		desc = item.find('description').text
		desc = re.sub('<.+?>', '', desc)
		return un(desc)

	def getURL(item):
		url = item.find('link').text
		return un(url)

	# compile a list of dictionaries each with feed info
	data = []
	for item in items:
		entry = {}
		entry['title'] = getTitle(item)
		entry['description'] = getDescription(item)
		entry['url'] = getURL(item)
		data.append(entry)
	return data


#def addFeed(url):
#    with open('feeds.txt', 'w') as f:
#        f.write(url)


def showDetails(item):
	print(item['title'], '\n')
	print(item['description'], '\n')
	print('URL:', item['url'], '\n')
	input()


def showArticles(site_title, data):
	print('Current articles from', site_title)
	titles = [article['title'] for article in data]
	selection = menu(titles)
	for item in data:
		if item['title'] == selection:
			return item


def showWebsites(rss_file):
	'''Parses subscription list into titles'''
	root = et.parse(rss_file).getroot()
	items = {}
	for outline in root.iter('outline'):
		if 'xmlUrl' in outline.attrib:
			items[outline.attrib['title']] = outline.attrib['xmlUrl']
	selection = menu(items.keys())
	if selection is None:
		sys.exit()
	entries = parse(items[selection])
	return (selection, entries)


while True:
	site_selection = showWebsites('feedly.opml')
	while True:
		if not site_selection[1]: #error when parsing selection
			break
		article_selection = showArticles(*site_selection)
		if not article_selection:
			break
showDetails(article_selection)
