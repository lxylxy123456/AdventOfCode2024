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

if 1:
	s = 0
	for i in lines:
		a = list(filter(lambda x: x in '0123456789', i))
		s0 = int(a[0] + a[-1])
		s += s0

	print(s)

W2I = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
	   'seven': 7, 'eight': 8, 'nine': 9}
EXP = 'one|two|three|four|five|six|seven|eight|nine|[0-9]'

if not 2:
	s = 0
	def lookup(x):
		return str(W2I.get(x, x))
	for i in lines:
		import re
		a = re.findall(EXP, i)
		s0 = int(lookup(a[0]) + lookup(a[-1]))
		s += s0

	print(s)

if 2:
	s = 0
	D = {}
	for k, v in W2I.items():
		D[k] = str(v)
		D[str(v)] = str(v)
	def lookup(x):
		return str(W2I.get(x, x))
	def test(s):
		import re
		matched = re.match(EXP, s)
		if matched:
			return lookup(matched.group())
		else:
			return None
	for i in lines:
		a = []
		for j in range(len(i)):
			t = test(i[j:])
			if t is not None:
				a.append(t)
		s0 = int(lookup(a[0]) + lookup(a[-1]))
		s += s0

	print(s)

