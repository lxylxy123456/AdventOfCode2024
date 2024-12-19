# Youtube: https://youtu.be/IimV1qhxLVo

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

def solve1(goal, choices):
	dp = [True]
	for index, i in enumerate(goal):
		cur = False
		for j in range(index + 1):
			if goal[j:index + 1] in choices and dp[j]:
				cur = True
		dp.append(cur)
	return dp[-1]

def part_1(lines):
	s = 0
	choices = set(lines[0].split(', '))
	assert lines[1] == ''
	for i in lines[2:]:
		s += solve1(i, choices)
	return s

def solve2(goal, choices):
	dp = [1]
	for index, i in enumerate(goal):
		cur = 0
		for j in range(index + 1):
			if goal[j:index + 1] in choices and dp[j]:
				cur += dp[j]
		dp.append(cur)
	return dp[-1]

def part_2(lines):
	s = 0
	choices = set(lines[0].split(', '))
	assert lines[1] == ''
	for i in lines[2:]:
		s += solve2(i, choices)
	return s

if __name__ == '__main__':
	main()

