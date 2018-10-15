#!/usr/bin/python
# coding: utf-8

import sys
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

channel = sys.argv[1]
xml_file = channel + '.xml'

tree = ET.parse(xml_file)
root = tree.getroot()
index_page = "#### 热门视频：[《文昭谈古论今》](https://github.com/gfw-breaker/wenzhao/blob/master/README.md)、[新唐人时事小品](https://github.com/gfw-breaker/ntdtv-comedy/blob/master/README.md)、[新唐人中国禁闻](https://github.com/gfw-breaker/ntdtv-news/blob/master/README.md)\n\n"


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
	body += "\n\n------------------------\n" + "#### [禁闻聚合首页](https://github.com/gfw-breaker/banned-news/blob/master/README.md) &nbsp;|&nbsp; [Web代理](https://github.com/gfw-breaker/open-proxy/blob/master/README.md) &nbsp;|&nbsp; [一键翻墙软件](https://github.com/gfw-breaker/nogfw/blob/master/README.md) &nbsp;|&nbsp; [《九评共产党》](https://github.com/gfw-breaker/9ping.md/blob/master/README.md#九评之一评共产党是什么) &nbsp;|&nbsp; [《解体党文化》](https://github.com/gfw-breaker/jtdwh.md/blob/master/README.md#绪论)"
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
	write_page(name, title, link, content)
	index_page += '#### [' + title + '](' + '../pages/' + channel + '/' + name + '.md) \n\n'


index_file = open('../indexes/' + channel + '.md', 'w')
index_file.write(index_page)
index_file.close()


