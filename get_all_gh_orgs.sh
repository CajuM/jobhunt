#!/bin/sh

set -x

since=

while :; do
	data=$(curl -s "https://api.github.com/organizations?since=${since}")
	if [ -n "$(echo \"${data}\" | grep 'API rate limit exceeded')" ]; then
		./sorry.sh
		continue
	fi

	since=$(echo "${data}" | jq -r '.[].id' | tail -n1)
	echo "${data}" | jq -r '.[].login'
done
