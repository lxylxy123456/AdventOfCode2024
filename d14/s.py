# Youtube: https://youtu.be/ZO83MHcgLMI

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
	X, Y = 101, 103
	#X, Y = 11, 7
	T = 100
	c = Counter()
	for i in lines:
		matched = re.fullmatch('p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', i)
		px, py, vx, vy = map(int, matched.groups())
		fx = (px + vx * T) % X
		fy = (py + vy * T) % Y
		# Check quadrant.
		mx = (X - 1) // 2
		my = (Y - 1) // 2
		if fx == mx or fy == my:
			continue
		c[((mx < fx), (my < fy))] += 1
	s = functools.reduce(operator.mul, c.values())
	return s

def part_2(lines):
	s = 0
	X, Y = 101, 103
	#X, Y = 11, 7
	T = 100
	c = Counter()
	robots = []
	for i in lines:
		matched = re.fullmatch('p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', i)
		px, py, vx, vy = map(int, matched.groups())
		robots.append((px, py, vx, vy))
	#for T in range(1000):
	for T in [7709]:
		canvas = []
		for y in range(Y):
			canvas.append([])
			for x in range(X):
				canvas[-1].append(' ')
		for px, py, vx, vy in robots:
			fx = (px + vx * T) % X
			fy = (py + vy * T) % Y
			canvas[fy][fx] = '█'
		for i in canvas:
			print(''.join(i))
		print('-' * X)
		input(str(T))
		# 33|, 87-, 134|, 190-, 235|, 293-, 336|
		# 33 + 101 * x = 87 + 103 * y
	return s

if __name__ == '__main__':
	main()

