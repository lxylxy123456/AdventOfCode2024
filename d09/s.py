# Youtube: https://youtu.be/olfhjIVWoHE

import argparse, math, sys, re, functools, operator, itertools
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

def solve1(nums):
	if not any(nums):
		return 0
	diffs = list(map(operator.sub, nums[1:], nums))
	return nums[-1] + solve1(diffs)

def part_1(lines):
	s = 0
	for i in lines:
		s += solve1(list(map(int, i.split())))
	return s

def solve2(nums):
	if not any(nums):
		return 0
	diffs = list(map(operator.sub, nums[1:], nums))
	return nums[0] - solve2(diffs)

def part_2(lines):
	s = 0
	for i in lines:
		s += solve2(list(map(int, i.split())))
	return s

if __name__ == '__main__':
	main()

