import argparse, math, sys, re, functools, operator, itertools, heapq
from collections import defaultdict, Counter, deque
#sys.setrecursionlimit(100000000)
#A = list(map(int, input().split()))
#T = int(input())

def read_lines(f):
	while True:
		line = f.readline()
		if not line:
			break
		assert line[-1] == '\n'
		yield line[:-1]

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-1', '--one', action='store_true', help='Only part 1')
	parser.add_argument('-2', '--two', action='store_true', help='Only part 2')
	parser.add_argument('input_file', nargs='?')
	args = parser.parse_args()
	if args.input_file is not None:
		f = open(args.input_file)
	else:
		f = sys.stdin
	lines = list(read_lines(f))
	if not args.two:
		print(part_1(lines))
	if not args.one:
		print(part_2(lines))

def count(s):
	ss = ''.join(s)
	return ss.count('XMAS') + ss.count('SAMX')

def part_1(lines):
	s = 0
	# Horizontal
	for i in lines:
		s += count(i)
	# Vertical
	for j in range(len(lines[0])):
		a = []
		for i in range(len(lines)):
			a.append(lines[i][j])
		s += count(a)
	# /, i = x + y
	for i in range(0, len(lines) + len(lines[0])):
		a = []
		for j in range(len(lines)):
			k = i - j
			if k in range(len(lines[0])):
				a.append(lines[j][k])
		s += count(a)
	# \, i = x - y
	for i in range(-len(lines), len(lines[0]) + 1):
		a = []
		for j in range(len(lines)):
			k = j - i
			if k in range(len(lines[0])):
				a.append(lines[j][k])
		s += count(a)
	return s

def part_2(lines):
	s = 0
	for i in range(1, len(lines) - 1):
		for j in range(1, len(lines[0]) - 1):
			if lines[i][j] != 'A':
				continue
			ul = lines[i - 1][j - 1]
			ur = lines[i - 1][j + 1]
			ll = lines[i + 1][j - 1]
			lr = lines[i + 1][j + 1]
			if {ul, lr} == {'M', 'S'} and {ur, ll} == {'M', 'S'}:
				s += 1
	return s

if __name__ == '__main__':
	main()

