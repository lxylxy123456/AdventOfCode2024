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

def blink_single(stone):
	if stone == 0:
		return [1]
	s = str(stone)
	if len(s) % 2 == 0:
		return [int(s[:len(s) // 2]), int(s[len(s) // 2:])]
	else:
		return [stone * 2024]

def blink1(stones):
	ans = []
	for i in stones:
		ans.extend(blink_single(i))
	return ans

def part_1(lines):
	line, = lines
	stones = list(map(int, line.split()))
	for _ in range(25):
		stones = blink1(stones)
	return len(stones)

def blink2(stones):
	ans = Counter()
	for i, count in stones.items():
		for j in blink_single(i):
			ans[j] += count
	return ans

def part_2(lines):
	line, = lines
	stones = Counter(map(int, line.split()))
	for _ in range(75):
		stones = blink2(stones)
	return sum(stones.values())

if __name__ == '__main__':
	main()

