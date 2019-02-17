#!/usr/bin/python
# coding: utf-8

import macros
import sys
import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

channel = sys.argv[1]
channel_url = sys.argv[2]

index_page = '' + macros.head
links = macros.tail


def get_content(url):
	response = requests.get(url)
	text = response.text.encode('utf-8')
	parser = BeautifulSoup(text, 'html.parser')
	post_content = parser.find('div', attrs = {'class': 'post_content'})
	if post_content is None:
		return '-'
	for related in post_content.find_all('div', attrs = {'class': 'post_related'}):
		related.decompose()
	for iframe in post_content.find_all('iframe'):
		iframe.decompose()
	return post_content.prettify().encode('utf-8') \
		.replace('</figure>','</figure><br/>') \
        .replace('<figcaption','<br/><figcaption') \
        .replace('</figcaption>','</figcaption><br/>') \
        .replace('<h2>', '<h4>') \
        .replace('<h2 ', '<h4 ') \
        .replace('</h2>', '</h4>')


def get_name(link):
	fname = link.split('/')[-1]
	aid  = fname.split('.')[0]
	return aid


def write_page(name, path, title, link, content):
	new_link = macros.git_base_url + '/' + channel + '/' + f_name 
	body = '### ' + title
	body += "\n------------------------\n\n" + content
	body += "\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++<br/><br/>" 
	body += "\n手机上长按并复制下列链接或二维码分享本文章：<br/>"
	body += "\n[" + new_link + "](" + new_link + ")<br/>"
	body += "\n[<img src='" + new_link + ".png'/>](" + new_link + ")<br/>"
	body += "\n原文地址（需翻墙访问）：" + link + "\n"
	body += "\n\n------------------------\n" + links
	fh = open(path, 'w')
	fh.write(body)
	fh.close()


index_text = requests.get(channel_url).text.encode('utf-8')
index_html = BeautifulSoup(index_text, 'html.parser')
articles = index_html.find_all('div', attrs = {'class': 'article'})
for article in articles:
	link = article.find_all('a')[1]
	a_url = link.get('href').encode('utf-8')
	a_title = link.find('h3').text.encode('utf-8').strip()
	name = get_name(a_url) + '.md'
	file_path = '../pages/' + channel + '/' + name 
	content = get_content(a_url)

	if not os.path.exists(file_path):
		print file_path
		write_page(name, file_path, a_title, a_url, content)
	index_page += '#### [' + a_title + '](' + file_path + ') \n\n'


index_file = open('../indexes/' + channel + '.md', 'w')
index_file.write(index_page)
index_file.close()



