#!/bin/bash
# author: gfw-breaker

channels="nsc412 nsc413 nsc418 nsc423 nsc422 nsc993 nsc424 nsc975"

## create dirs
for channel in $channels ; do
	mkdir -p ../pages/$channel
done
	
## get feeds files
for channel in $channels ; do
	url="http://www.epochtimes.com/gb/$channel.xml"
	wget -q $url
	sed -i 's/content:encoded/content/g' $channel.xml
	echo "getting channel: $url"
	python parse_epoch.py $channel
done


