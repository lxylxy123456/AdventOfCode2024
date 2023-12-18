"""
Refactor using https://en.wikipedia.org/wiki/Shoelace_formula and handle
perimeter properly. Inspired by
https://github.com/bvandewalle/aoc2023/blob/main/18/main.go .
"""

import argparse, math, sys, re, functools, operator, itertools, heapq
from collections import defaultdict, Counter
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

VE = (0, 1)
VW = (0, -1)
VN = (-1, 0)
VS = (1, 0)

VR = (0, 1)
VL = (0, -1)
VU = (-1, 0)
VD = (1, 0)
V = {'R': VR, 'L': VL, 'U': VU, 'D': VD}

def vec_neg(v):
	return tuple(map(operator.neg, v))

def vec_add(v1, v2):
	return tuple(map(operator.add, v1, v2))

def vec_mult(c, v):
	return tuple(map(lambda x: c * x, v))

def solve(segments):
	a = 0
	p = 0
	for index, (cur, direction, length) in enumerate(segments):
		next_pos = segments[(index + 1 + len(segments)) % len(segments)][0]
		x1, y1 = cur
		x2, y2 = next_pos
		# Area
		a += (x1 - x2) * (y1 + y2)
		# Perimeter
		p += length
	s = abs(a) + p
	assert s % 2 == 0
	return s // 2 + 1

def part_1(lines):
	cur = (0, 0)
	# [((curx, cury), dir, length), ...]
	segments = []
	for i in lines:
		matched = re.fullmatch('([LRUD]) (\d+) \(\#([0-9a-f]{6})\)', i)
		direction, length, color = matched.groups()
		direction = V[direction]
		length = int(length)
		segments.append((cur, direction, length))
		cur = vec_add(cur, vec_mult(length, direction))
	assert cur == (0, 0)
	s = solve(segments)
	return s

def part_2(lines):
	cur = (0, 0)
	# [((curx, cury), dir, length), ...]
	segments = []
	for i in lines:
		matched = re.fullmatch('([LRUD]) (\d+) \(\#([0-9a-f]{6})\)', i)
		direction, length, color = matched.groups()
		direction = { '0': VR, '1': VD, '2': VL, '3': VU }[color[-1]]
		length = int(color[:-1], 16)
		segments.append((cur, direction, length))
		cur = vec_add(cur, vec_mult(length, direction))
	assert cur == (0, 0)
	s = solve(segments)
	return s

if __name__ == '__main__':
	main()

