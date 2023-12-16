#!/bin/bash

set -xe

cd "$1"

TMPD="$(mktemp -d)"

grep '^Your puzzle answer was' q.txt | grep -oE '[0-9]+' > "$TMPD/expected"

for i in s*.py; do
	time python3 "$i" in.txt | tee -a "$TMPD/actual"
done

while read EXPECTED; do
	grep -w "$EXPECTED" "$TMPD/actual"
done < "$TMPD/expected"

if [ -f compute.sh ]; then
	. compute.sh
fi

rm -r "$TMPD"

