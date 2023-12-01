try:
	import os, sys
	stdin = sys.stdin
	if len(sys.argv) > 1:
		stdin = open(sys.argv[1])
	def input():
		line = stdin.readline()
		if line:
			assert line[-1] == '\n'
			return line[:-1]
		else:
			raise EOFError
except Exception:
	pass

# import math, sys
# sys.setrecursionlimit(100000000)
# from collections import defaultdict
# A = list(map(int, input().split()))
# T = int(input())

def read_lines():
	while True:
		try:
			yield input()
		except EOFError:
			break

lines = list(read_lines())


