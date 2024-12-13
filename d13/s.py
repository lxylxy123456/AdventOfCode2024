import argparse, math, sys, re, functools, operator, itertools, heapq
from collections import defaultdict, Counter, deque
from fractions import Fraction
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

def parse_input(lines):
	l = iter(lines)
	while True:
		m = []
		m += re.fullmatch(r'Button A: X\+(\d+), Y\+(\d+)', next(l)).groups()
		m += re.fullmatch(r'Button B: X\+(\d+), Y\+(\d+)', next(l)).groups()
		m += re.fullmatch(r'Prize: X=(\d+), Y=(\d+)', next(l)).groups()
		yield tuple(map(int, m))
		n = next(l, None)
		if n is None:
			break
		else:
			assert n == ''

def part_1(lines):
	s = 0
	qs = list(parse_input(lines))
	for ax, ay, bx, by, px, py in qs:
		# A * ax + B * bx = px
		# A * ay + B * by = py
		assert ax * by != ay * bx
		A = Fraction(-(by*px-bx*py), (ay*bx-ax*by))
		B = Fraction((ay*px-ax*py), (ay*bx-ax*by))
		if A.denominator != 1 or B.denominator != 1:
			continue
		assert A.numerator < 100 and B.numerator < 100
		s += 3 * A + B
	return s

def part_2(lines):
	s = 0
	qs = list(parse_input(lines))
	for ax, ay, bx, by, px, py in qs:
		px += 10000000000000
		py += 10000000000000
		# A * ax + B * bx = px
		# A * ay + B * by = py
		assert ax * by != ay * bx
		A = Fraction(-(by*px-bx*py), (ay*bx-ax*by))
		B = Fraction((ay*px-ax*py), (ay*bx-ax*by))
		if A.denominator != 1 or B.denominator != 1:
			continue
		s += 3 * A + B
	return s

if __name__ == '__main__':
	main()

