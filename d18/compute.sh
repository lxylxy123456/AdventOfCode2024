time python3 optimize_sf.py in.txt | tee -a "$TMPD/actual2"
diff "$TMPD/actual" "$TMPD/actual2"
