#!/bin/bash
# author: gfw-breaker

channels="news202 news203 news204 news205 news206 news207 news208 prog1138"

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


