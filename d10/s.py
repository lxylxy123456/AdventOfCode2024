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

V = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def part_1(lines):
	s = 0
	X = len(lines)
	Y = len(lines[0])
	reaches = []
	for x in range(X):
		reaches.append([])
		for y in range(Y):
			reaches[-1].append(None)
	for x in range(X):
		for y in range(Y):
			if lines[x][y] == '9':
				reaches[x][y] = {(x, y)}
	for n in range(8, -1, -1):
		for x in range(X):
			for y in range(Y):
				if lines[x][y] != str(n):
					continue
				se = set()
				reaches[x][y] = se
				for vx, vy in V:
					xx = x + vx
					yy = y + vy
					if not (xx in range(X) and yy in range(Y)):
						continue
					if lines[xx][yy] != str(n + 1):
						continue
					se.update(reaches[xx][yy])
	for x in range(X):
		for y in range(Y):
			if lines[x][y] == '0':
				s += len(reaches[x][y])
	return s

def part_2(lines):
	s = 0
	X = len(lines)
	Y = len(lines[0])
	reaches = []
	for x in range(X):
		reaches.append([])
		for y in range(Y):
			reaches[-1].append(None)
	for x in range(X):
		for y in range(Y):
			if lines[x][y] == '9':
				reaches[x][y] = 1
	for n in range(8, -1, -1):
		for x in range(X):
			for y in range(Y):
				if lines[x][y] != str(n):
					continue
				se = 0
				for vx, vy in V:
					xx = x + vx
					yy = y + vy
					if not (xx in range(X) and yy in range(Y)):
						continue
					if lines[xx][yy] != str(n + 1):
						continue
					se += reaches[xx][yy]
				reaches[x][y] = se
	for x in range(X):
		for y in range(Y):
			if lines[x][y] == '0':
				s += reaches[x][y]
	return s

if __name__ == '__main__':
	main()

