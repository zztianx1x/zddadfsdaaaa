#!/bin/bash
# author: gfw-breaker

folder=$(dirname $0)
echo $folder
cd $folder

## pull
mkdir -p ../indexes
mkdir -p ../pages
rm *xml*
git pull

## sync
for sf in $(ls sync_*.sh); do
	bash $sf
done

## remove video news
tt=$(date "+%m%d%H%M")
for f in $(ls ../indexes/*); do
	sed -i "s/\.md/\.md?t=$tt/g" $f
	sed -i "/翻墙必看】/d" $f
	sed -i "/精彩推荐/d" $f
	sed -i "/全球新闻/d" $f
	sed -i "/环球直击/d" $f
	sed -i "/【中国禁闻/d" $f
	sed -i "/石涛聚焦/d" $f
done


## add qr code
base_url="https://github.com/gfw-breaker/banned-news/blob/master"
for d in $(ls ../pages/); do
    for f in $(ls -t ../pages/$d | grep 'md$'); do
		a_path="../pages/$d/$f"
		a_url="$base_url/pages/$d/$f"
		if [ ! -f $a_path.png ]; then
			qrencode -o $a_path.png -s 4 $a_url
		fi
		echo -e "\n<img src='http://gfw-breaker.win/statistics.png' width='1px' height='1px'/>\n" >> $a_path
    done
done


## add to git
git add ../indexes/*
git add ../pages/*


## purge old entries
for d in $(ls ../pages/); do
    for f in $(ls -t ../pages/$d | grep 'md$' | sed -n '300,$p'); do
        git rm "../pages/$d/$f"   
        git rm "../pages/$d/$f.png"   
    done
done


## write README.md
rm *.xml
sed -i "s/\.md?t=[0-9]*)/.md?t=$tt)/g" ../README.md
git add ../README.md

ts=$(date "+-%m月-%d日-%H时-%M分" | sed 's/-0//g' | sed 's/-//g')
git commit -a -m "同步于: $ts"
git push


