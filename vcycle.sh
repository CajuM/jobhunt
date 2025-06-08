#!/bin/sh

set -e

TOP=$(dirname $(readlink -f $0))

gtek=$1
nurl=$2

tmp=$(cat "${gtek}" | awk '{print $2}')
tmp=$(comm -23 <(echo "${tmp}" | sort -u) <(cat "${TOP}/legit.txt" | sort -u))
tmp=$(comm -23 <(echo "${tmp}" | sort -u) <(cat "${TOP}/illegit.txt" | sort -u))
tmp=$(echo "${tmp}" | shuf | head -n${nurl})

urls=$(echo "${tmp}" | sed 's@^http@@g; s@^s@@g; s@^://@@g' | grep -Po '^[^/]+' | sed 's@^@https://www.google.com/search?q=careers%20@')

xdg-open $(echo "${urls}" | head -n1) & # Firefox insists on opening a blank tab when opening the first URL

for url in ${urls}; do
	xdg-open ${url} &
	sleep 0.2
done

wait

for url in ${urls}; do
	wait
done

echo "${tmp}"
