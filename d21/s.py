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

VECS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def vec_add(v1, v2):
	return tuple(map(operator.add, v1, v2))

def vec_mult(c, v):
	return tuple(map(lambda x: c * x, v))

def part_1(lines):
	s = 0
	dist = []
	start = None
	for index, i in enumerate(lines):
		dist.append([])
		for jndex, j in enumerate(i):
			dist[-1].append(None)
			if j == 'S':
				start = (index, jndex)
	assert start is not None

	in_map = lambda x, y: x in range(len(lines)) and y in range(len(lines[0]))
	cur_dist = 0
	frontier = {start}
	while frontier:
		new_frontier = set()
		for x, y in frontier:
			dist[x][y] = cur_dist
			for dx, dy in VECS:
				nx, ny = vec_add((x, y), (dx, dy))
				if (in_map(nx, ny) and lines[nx][ny] == '.' and
					dist[nx][ny] is None):
					new_frontier.add((nx, ny))
		frontier = new_frontier
		cur_dist += 1

	for i in dist:
		for j in i:
			if j is not None and j <= 64 and j % 2 == 0:
				s += 1
	return s

def part_2(lines):
	s = 0
	for i in lines:
		i
	return s

if __name__ == '__main__':
	main()

