#!/usr/bin/python
# coding: utf-8

import sys
import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

channel = sys.argv[1]
channel_url = sys.argv[2]

index_page = "#### 精彩视频：[《文昭谈古论今》](https://github.com/gfw-breaker/wenzhao/blob/master/README.md) | [《大陆新闻解读》](https://github.com/gfw-breaker/ntdtv-comedy/blob/master/README.md) | [《中国禁闻》](https://github.com/gfw-breaker/ntdtv-news/blob/master/README.md) | [《历史上的今天》](https://github.com/gfw-breaker/today-in-history/blob/master/README.md) \n\n"


def get_content(url):
	response = requests.get(url)
	text = response.text.encode('utf-8')
	parser = BeautifulSoup(text, 'html.parser')
	post_content = parser.find('div', attrs = {'class': 'post_content'})
	if post_content is None:
		return '-'
	for related in post_content.find_all('div', attrs = {'class', 'post_related'}):
		related.decompose()
	return post_content.prettify().encode('utf-8') \
		.replace('<h2>','<h4>').replace('</h2>','</h4>')
	# return content.replace('href="/xtr','href="http://www.ntdtv.com/xtr') \
	#	.replace('<h2>','<h4>').replace('</h2>','</h4>')


def get_name(link):
	fname = link.split('/')[-1]
	aid  = fname.split('.')[0]
	return aid


def write_page(path, title, link, content):
	body = '### ' + title
	body += "\n------------------------\n\n" + content
	body += "\n<br/>原文链接：" + link + "\n"
	body += "\n\n------------------------\n" + "#### [禁闻聚合首页](https://github.com/gfw-breaker/banned-news/blob/master/README.md) &nbsp;|&nbsp; [Web代理](https://github.com/gfw-breaker/open-proxy/blob/master/README.md) &nbsp;|&nbsp; [一键翻墙软件](https://github.com/gfw-breaker/nogfw/blob/master/README.md) &nbsp;|&nbsp; [《九评共产党》](https://github.com/gfw-breaker/9ping.md/blob/master/README.md#九评之一评共产党是什么) &nbsp;|&nbsp; [《解体党文化》](https://github.com/gfw-breaker/jtdwh.md/blob/master/README.md#绪论)"
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
	name = get_name(a_url)
	file_path = '../pages/' + channel + '/' + name + '.md'
	content = get_content(a_url)

	if not os.path.exists(file_path):
		write_page(file_path, a_title, a_url, content)
	index_page += '#### [' + a_title + '](' + file_path + ') \n\n'


index_file = open('../indexes/' + channel + '.md', 'w')
index_file.write(index_page)
index_file.close()

