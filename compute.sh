#!/bin/bash

set -xe

cd "$1"

TMPD="$(mktemp -d)"

grep '^Your puzzle answer was' q.txt | cut -d ' ' -f 5- \
	| grep -oE '[0-9a-z,]+' > "$TMPD/expected"
if [ "$(basename "$PWD")" = "d25" ]; then
	diff <(wc -l < "$TMPD/expected") <(echo 1)
else
	diff <(wc -l < "$TMPD/expected") <(echo 2)
fi

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

