# Youtube: https://youtu.be/pOO4UpTuY1Y

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

ADJ = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def dfs1(lines, visited, X, Y, x, y):
	assert not visited[x][y]
	visited[x][y] = True
	ans = {(x, y)}
	for dx, dy in ADJ:
		xx = x + dx
		yy = y + dy
		if xx in range(X) and yy in range(Y):
			if lines[x][y] == lines[xx][yy] and not visited[xx][yy]:
				ans.update(dfs1(lines, visited, X, Y, xx, yy))
	return ans

def get_peri(vertices):
	ans = 0
	for x, y in vertices:
		ans += 4
		for dx, dy in ADJ:
			xx = x + dx
			yy = y + dy
			if (xx, yy) in vertices:
				ans -= 1
	return ans

def part_1(lines):
	s = 0
	X = len(lines)
	Y = len(lines[0])
	visited = []
	# DFS
	for i in range(X):
		visited.append([])
		for j in range(Y):
			visited[-1].append(False)
	for x in range(X):
		for y in range(Y):
			if visited[x][y]:
				continue
			v = dfs1(lines, visited, X, Y, x, y)
			s += len(v) * get_peri(v)
	return s

def get_sides(vertices):
	vecs = defaultdict(list)
	for x, y in vertices:
		for dx, dy in ADJ:
			xx = x + dx
			yy = y + dy
			if (xx, yy) not in vertices:
				vecs[dx, dy].append((x, y))
	ans = 0
	for (dx, dy), points in vecs.items():
		#print(dx, dy, points)
		old_d = (dx, dy)
		points.sort()
		dx, dy = abs(dy), abs(dx)
		while points:
			x, y = points[0]
			#print(' ', x, y, '', old_d, end='  ')
			while (x, y) in points:
				points.remove((x, y))
				x = x + dx
				y = y + dy
			#print(x, y)
			ans += 1
	return ans

def part_2(lines):
	s = 0
	# DFS
	X = len(lines)
	Y = len(lines[0])
	visited = []
	for i in range(X):
		visited.append([])
		for j in range(Y):
			visited[-1].append(False)
	for x in range(X):
		for y in range(Y):
			if visited[x][y]:
				continue
			v = dfs1(lines, visited, X, Y, x, y)
			#print(lines[x][y], len(v), get_sides(v))
			s += len(v) * get_sides(v)
	return s

if __name__ == '__main__':
	main()

