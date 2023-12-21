time python3 optimize_fork.py in.txt | tee -a "$TMPD/actual2"
diff <(tail -n 1 "$TMPD/actual") <(tail -n 1 "$TMPD/actual2")
