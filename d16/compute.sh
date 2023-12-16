time python3 optimize_scc.py in.txt | tee -a "$TMPD/actual2"
diff "$TMPD/actual" "$TMPD/actual2"
