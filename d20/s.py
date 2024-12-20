# Youtube: https://youtu.be/IwlniP60orM

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

def find_symbol(lines, X, Y, c):
	for x in range(X):
		for y in range(Y):
			if lines[x][y] == c:
				return x, y
	raise ValueError

ADJ = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def calc_dist(lines, X, Y):
	sx, sy = find_symbol(lines, X, Y, 'S')
	ex, ey = find_symbol(lines, X, Y, 'E')
	# Record distance.
	dist = []
	for x in range(X):
		dist.append([])
		for y in range(Y):
			dist[-1].append(None)
	cx, cy = sx, sy
	d = 0
	while True:
		dist[cx][cy] = d
		if (cx, cy) == (ex, ey):
			break
		mx, my = None, None
		for dx, dy in ADJ:
			nx, ny = cx + dx, cy + dy
			if nx in range(X) and ny in range(Y):
				if dist[nx][ny] is None and lines[nx][ny] != '#':
					assert mx is None and my is None
					mx, my = nx, ny
		assert mx is not None and my is not None
		cx, cy = mx, my
		d += 1
	dot_count = ''.join(itertools.chain.from_iterable(lines)).count('.')
	assert dist[ex][ey] == dot_count + 1
	return dist

def part_1(lines):
	s = 0
	X = len(lines)
	Y = len(lines[0])
	dist = calc_dist(lines, X, Y)
	# Scan for '.#\n#.'
	for x in range(X - 1):
		for y in range(Y - 1):
			if (lines[x][y] == '#' and
				lines[x + 1][y] != '#' and
				lines[x][y + 1] != '#' and 
				lines[x + 1][y + 1] == '#'):
				raise ValueError
			if (lines[x][y] != '#' and
				lines[x + 1][y] == '#' and
				lines[x][y + 1] == '#' and 
				lines[x + 1][y + 1] != '#'):
				raise ValueError
	# Cound cheats
	for hx in range(X):
		for hy in range(Y):
			if lines[hx][hy] != '#':
				continue
			for dx, dy in ADJ:
				nx, ny = hx + dx, hy + dy
				mx, my = hx - dx, hy - dy
				if not (nx in range(X) and ny in range(Y)):
					continue
				if not (mx in range(X) and my in range(Y)):
					continue
				if lines[nx][ny] == '#':
					continue
				if lines[mx][my] == '#':
					continue
				saving = dist[nx][ny] - dist[mx][my] - 2
				if saving >= 100:
					s += 1
	return s

def part_2(lines):
	s = 0
	X = len(lines)
	Y = len(lines[0])
	dist = calc_dist(lines, X, Y)
	for mx in range(X):
		for my in range(Y):
			if lines[mx][my] == '#':
				continue
			for dx in range(-20, 21):
				nx = mx + dx
				if nx not in range(X):
					continue
				for dy in range(-20 + abs(dx), 21 - abs(dx)):
					assert abs(dx) + abs(dy) <= 20
					ny = my + dy
					if ny not in range(Y):
						continue
					if lines[nx][ny] == '#':
						continue
					saving = dist[nx][ny] - dist[mx][my] - (abs(dx) + abs(dy))
					if saving >= 100:
						s += 1
	return s

if __name__ == '__main__':
	main()

