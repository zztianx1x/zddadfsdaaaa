#!/usr/bin/python
# coding: utf-8

import macros
import sys
import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

channel = sys.argv[1]
xml_file = channel + '.xml'

index_page = '' + macros.head
links = macros.tail

tree = ET.parse(xml_file)
root = tree.getroot()

def get_content(text):
	parser = BeautifulSoup(text, 'html.parser')
	for iframe in parser.find_all('iframe'):
		iframe.decompose()
	for script in parser.find_all('script'):
		script.decompose()
	content = parser.prettify().encode('utf-8')
	return content.replace('</figure>','</figure><br/>') \
		.replace('<figcaption','<br/><figcaption') \
		.replace('</figcaption>','</figcaption><br/>') \
		.replace('<h2>', '<h4>') \
		.replace('<h2 ', '<h4 ') \
		.replace('</h2>', '</h4>')


def write_page(name, title, link, content):
	body = '### ' + title
	body += "\n------------------------\n\n" + content
	body += "\n原文链接：" + link + "\n"
	body += "\n\n------------------------\n" + links
	f_name = '../pages/' + channel + '/' +  name + '.md'
	fh = open(f_name, 'w')
	fh.write(body)
	fh.close()


def get_name(link):
	fname = link.split('/')[-1]
	return fname.split('.')[0]


for child in root[0]:
	if child.tag != 'item':
		continue
	link = child.find('link').text
	title = child.find('title').text.encode('utf-8')
	content = child.find('content').text.encode('utf-8')
	content = get_content(content)
	name = get_name(link)
	file_path = '../pages/' + channel + '/' + name + '.md'
	
	if not os.path.exists(file_path):
		print file_path
		write_page(file_path, title, link, content)
	index_page += '#### [' + title + '](' + file_path + ') \n\n'


index_file = open('../indexes/' + channel + '.md', 'w')
index_file.write(index_page)
index_file.close()


