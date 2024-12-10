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
	s = 0
	a = []
	X = len(lines)
	Y = len(lines[0])
	for i in range(X):
		a.append([])
		for j in range(Y):
			a[-1].append(False)
	freq = defaultdict(list)
	for i in range(X):
		for j in range(Y):
			if lines[i][j] != '.':
				freq[lines[i][j]].append((i, j))
	for coords in freq.values():
		for ix, iy in coords:
			for jx, jy in coords:
				if (ix, iy) == (jx, jy):
					continue
				ax, ay = ix * 2 - jx, iy * 2 - jy
				if ax in range(X) and ay in range(Y):
					a[ax][ay] = True
	for i in a:
		for j in i:
			s += j
	return s

def part_2(lines):
	s = 0
	a = []
	X = len(lines)
	Y = len(lines[0])
	for i in range(X):
		a.append([])
		for j in range(Y):
			a[-1].append(False)
	freq = defaultdict(list)
	for i in range(X):
		for j in range(Y):
			if lines[i][j] != '.':
				freq[lines[i][j]].append((i, j))
	for coords in freq.values():
		for ix, iy in coords:
			for jx, jy in coords:
				if (ix, iy) == (jx, jy):
					continue
				ax, ay = ix, iy
				while ax in range(X) and ay in range(Y):
					a[ax][ay] = True
					ax -= jx - ix
					ay -= jy - iy
	for i in a:
		for j in i:
			s += j
	return s

if __name__ == '__main__':
	main()

