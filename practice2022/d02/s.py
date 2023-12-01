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

D1 = {'A': 0, 'B': 1, 'C': 2}
D2 = {'X': 0, 'Y': 1, 'Z': 2}

total_s = 0
for i in lines:
	a, b = i.split()
	aa = D1[a]
	bb = D2[b]
	s1 = bb + 1
	s2 = None
	if aa == (bb + 1) % 3:
		s2 = 0
	elif aa == (bb + 0) % 3:
		s2 = 3
	else:
		assert aa == (bb + 2) % 3
		s2 = 6
	#print(s1, s2)
	total_s += s1 + s2

print(total_s)

D3 = {'X': 2, 'Y': 0, 'Z': 1}

total_s = 0
for i in lines:
	a, b = i.split()
	aa = D1[a]
	cc = D3[b]
	bb = (aa + cc) % 3
	s1 = bb + 1
	s2 = None
	if aa == (bb + 1) % 3:
		s2 = 0
	elif aa == (bb + 0) % 3:
		s2 = 3
	else:
		assert aa == (bb + 2) % 3
		s2 = 6
	#print(s1, s2)
	total_s += s1 + s2

print(total_s)

