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

def gen_secret(old_secret):
	s = old_secret
	s = ((s * 64) ^ s) % 16777216
	s = ((s // 32) ^ s) % 16777216
	s = ((s * 2048) ^ s) % 16777216
	return s

def gen_secret_2000(old_secret, rounds=2000):
	s = old_secret
	for _ in range(rounds):
		s = gen_secret(s)
	return s

def part_1(lines):
	s = 0
	for i in lines:
		s += gen_secret_2000(int(i))
	return s

def gen_changes(init_secret, rounds=2000):
	prev = init_secret
	hist_change = deque([], 4)
	for i in range(rounds):
		s = gen_secret(prev)
		cur_change = s % 10 - prev % 10
		hist_change.append(cur_change)
		if len(hist_change) == 4:
			yield s % 10, tuple(hist_change)
		prev = s

def part_2(lines):
	s = 0
	profit = Counter()
	for i in lines:
		visited = set()
		for price, changes in gen_changes(int(i)):
			if changes in visited:
				continue
			visited.add(changes)
			profit[changes] += price
	s = max(profit.values())
	return s

if __name__ == '__main__':
	main()

