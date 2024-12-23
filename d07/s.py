# Youtube: https://youtu.be/jdkzd5PXo4A

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

@functools.lru_cache
def check_equation1(lhs, rhs):
	if len(rhs) == 1:
		return lhs == rhs[0]
	# +
	if check_equation1(lhs, (rhs[0] + rhs[1], *rhs[2:])):
		return True
	# *
	if check_equation1(lhs, (rhs[0] * rhs[1], *rhs[2:])):
		return True
	return False

def part_1(lines):
	s = 0
	for i in lines:
		lhs, rhs = i.split(':')
		lhs = int(lhs)
		rhs = tuple(map(int, rhs.split()))
		if check_equation1(lhs, rhs):
			s += lhs
	return s

def check_equation2(lhs, rhs):
	if len(rhs) == 1:
		return lhs == rhs[0]
	# +
	if check_equation2(lhs, (rhs[0] + rhs[1], *rhs[2:])):
		return True
	# *
	if check_equation2(lhs, (rhs[0] * rhs[1], *rhs[2:])):
		return True
	# ||
	if check_equation2(lhs, (int(str(rhs[0]) + str(rhs[1])), *rhs[2:])):
		return True
	return False

def part_2(lines):
	s = 0
	for i in lines:
		lhs, rhs = i.split(':')
		lhs = int(lhs)
		rhs = tuple(map(int, rhs.split()))
		if check_equation2(lhs, rhs):
			s += lhs
	return s

if __name__ == '__main__':
	main()

