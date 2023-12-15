#!/bin/bash

set -xe

cd "$1"

TMPD="$(mktemp -d)"

grep '^Your puzzle answer was' q.txt | grep -oE '[0-9]+' > "$TMPD/expected"

for i in s*.py; do
	python3 "$i" in.txt >> "$TMPD/actual"
done

while read EXPECTED; do
	grep "$EXPECTED" "$TMPD/actual"
done < "$TMPD/expected"

rm -r "$TMPD"

