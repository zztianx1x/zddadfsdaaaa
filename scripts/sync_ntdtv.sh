#!/bin/bash
# author: gfw-breaker

channels="news204 news203 news202 news206 news207 news208"

## create dirs
for channel in $channels ; do
	mkdir -p ../pages/$channel
done
	
## get feeds files
for channel in $channels ; do
	url="http://www.ntdtv.com/xtr/gb/$channel.xml"
	wget -q $url -O $channel.xml
	echo "getting channel: $channel"
	python parse_ntdtv.py $channel
done


