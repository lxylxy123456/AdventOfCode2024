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

TURN = {
	(-1, 0): (0, 1),
	(0, 1): (1, 0),
	(1, 0): (0, -1),
	(0, -1): (-1, 0),
}

def part_1(lines):
	s = 0
	m = []
	for i in lines:
		m.append(list(i))
	gx, gy = None, None
	dx, dy = -1, 0
	for index, i in enumerate(m):
		for jndex, j in enumerate(i):
			if j == '^':
				assert gx is None and gy is None
				gx = index
				gy = jndex
	assert gx is not None and gy is not None

	X = len(m)
	Y = len(m[0])
	while True:
		m[gx][gy] = 'X'
		nx = gx + dx
		ny = gy + dy
		if nx in range(X) and ny in range(Y):
			if m[nx][ny] == '#':
				dx, dy = TURN[dx, dy]
			else:
				gx, gy = nx, ny
		else:
			break
	for i in m:
		for j in i:
			s += (j == 'X')
	return s

def visit_map(m, gx, gy):
	X = len(m)
	Y = len(m[0])
	dx, dy = -1, 0
	history = set()
	while True:
		nx = gx + dx
		ny = gy + dy
		if nx in range(X) and ny in range(Y):
			if m[nx][ny] == '#':
				dx, dy = TURN[dx, dy]
			else:
				gx, gy = nx, ny
		else:
			return False
		if (gx, gy, dx, dy) in history:
			return True
		else:
			history.add((gx, gy, dx, dy))

def part_2(lines):
	s = 0
	m = []
	for i in lines:
		m.append(list(i))
	gx, gy = None, None
	for index, i in enumerate(m):
		for jndex, j in enumerate(i):
			if j == '^':
				assert gx is None and gy is None
				gx = index
				gy = jndex
	assert gx is not None and gy is not None

	for index, i in enumerate(m):
		for jndex, j in enumerate(i):
			if j == '.':
				m[index][jndex] = '#'
				s += visit_map(m, gx, gy)
				m[index][jndex] = '.'
	return s

if __name__ == '__main__':
	main()

