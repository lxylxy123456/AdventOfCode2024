# Youtube: https://youtu.be/AA_HTUAiGN4

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

def read(lines):
	for i in lines:
		x, y = map(int, i.split(','))
		yield (x, y)

def part_1(lines):
	s = 0
	falls = list(read(lines))
	if len(falls) <= 25:
		X = Y = 6 + 1
		size = 12
	else:
		X = Y = 70 + 1
		size = 1024
	start = (0, 0)
	goal = (X - 1, Y - 1)
	m = []
	for y in range(Y):
		m.append([])
		for x in range(X):
			m[-1].append('.')
	for x, y in falls[:size]:
		m[y][x] = '#'
	# BFS
	visited = {}
	q = deque([(start, 0)])
	while q:
		(x, y), dist = q.popleft()
		if (x, y) in visited:
			continue
		if m[y][x] == '#':
			continue
		visited[(x, y)] = dist
		if (x, y) == goal:
			return dist
		for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
			nx = x + dx
			ny = y + dy
			if nx in range(X) and ny in range(Y):
				q.append(((nx, ny), dist + 1))
	raise ValueError

def part_2(lines):
	s = 0
	falls = list(read(lines))
	if len(falls) <= 25:
		X = Y = 6 + 1
	else:
		X = Y = 70 + 1
	start = (0, 0)
	goal = (X - 1, Y - 1)
	m = []
	for y in range(Y):
		m.append([])
		for x in range(X):
			m[-1].append('.')
	for x, y in falls:
		m[y][x] = '#'
	# Perform UFS on all current nodes
	ufs = {}
	for y in range(Y):
		for x in range(X):
			ufs[(x, y)] = (x, y)
	def find(x):
		if x != ufs[x]:
			ufs[x] = find(ufs[x])
		return ufs[x]
	def union(x, y):
		x = find(x)
		y = find(y)
		ufs[y] = x
	for y in range(Y):
		for x in range(X):
			if m[y][x] == '#':
				continue
			for dx, dy in [(1, 0), (0, 1)]:
				nx = x + dx
				ny = y + dy
				if nx in range(X) and ny in range(Y):
					if m[ny][nx] == '#':
						continue
					union((x, y), (nx, ny))
	# Reverse the falling of bytes.
	for x, y in reversed(falls):
		assert m[y][x] == '#'
		m[y][x] = '.'
		for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
			nx = x + dx
			ny = y + dy
			if nx in range(X) and ny in range(Y):
				union((x, y), (nx, ny))
		if find(start) == find(goal):
			return ','.join(map(str, (x, y)))
	raise ValueError

if __name__ == '__main__':
	main()

