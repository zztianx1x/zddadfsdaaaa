#!/bin/bash
# author: gfw-breaker

folder=$(dirname $0)
cd $folder

## pull
mkdir -p ../indexes
mkdir -p ../pages
rm *.xml
git pull

## sync
for sf in $(ls sync_*.sh); do
	bash $sf
done

## add to git
tt=$(date "+%m%d%H%M")
for f in $(ls ../indexes/*); do
	sed -i "s/\.md/\.md?t=$tt/g" $f
	sed -i "/翻墙必看/d" $f
	sed -i "/精彩推荐/d" $f
done
git add ../indexes/*
git add ../pages/*

sed -i "s/\.md?t=[0-9]*)/.md?t=$tt)/g" ../README.md
git add ../README.md

ts=$(date "+-%m月-%d日-%H时-%M分" | sed 's/-0//g' | sed 's/-//g')
git commit -a -m "同步于: $ts"
git push


