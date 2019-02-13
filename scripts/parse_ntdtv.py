#!/usr/bin/python
# coding: utf-8

import macros
import sys
import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

print 'test'

channel = sys.argv[1]
channel_url = sys.argv[2]

print channel_url

index_page = '' + macros.head
links = macros.tail


