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

def check_safe_1(r):
	# increasing
	for i, j in zip(r, r[1:]):
		if j - i not in range(1, 4):
			break
	else:
		return True
	# decreasing
	for i, j in zip(r, r[1:]):
		if i - j not in range(1, 4):
			break
	else:
		return True
	return False

def part_1(lines):
	s = 0
	rs = []
	for i in lines:
		rs.append(list(map(int, i.split())))
	for r in rs:
		s += check_safe_1(r)
	return s

def check_safe_2(r):
	if check_safe_1(r):
		return True
	for i in range(len(r)):
		rr = r.copy()
		rr.pop(i)
		if check_safe_1(rr):
			return True
	return False

def part_2(lines):
	s = 0
	rs = []
	for i in lines:
		rs.append(list(map(int, i.split())))
	for r in rs:
		s += check_safe_2(r)
	return s

if __name__ == '__main__':
	main()

