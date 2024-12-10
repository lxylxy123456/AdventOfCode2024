# Youtube: https://youtu.be/0urvitGbkn8

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

def part_1(lines):
	a = []
	b = []
	for i in lines:
		_0, _1 = map(int, i.split())
		a.append(_0)
		b.append(_1)
	a.sort()
	b.sort()
	return sum(map(lambda x, y: abs(x - y), a, b))

def part_2_slow(lines):
	s = 0
	a = []
	b = []
	for i in lines:
		_0, _1 = map(int, i.split())
		a.append(_0)
		b.append(_1)
	for i in a:
		s += i * b.count(i)
	return s

def part_2(lines):
	s = 0
	a = []
	b = []
	for i in lines:
		_0, _1 = map(int, i.split())
		a.append(_0)
		b.append(_1)
	bb = Counter(b)
	for i in a:
		s += i * bb[i]
	assert s == part_2_slow(lines)
	return s

if __name__ == '__main__':
	main()

