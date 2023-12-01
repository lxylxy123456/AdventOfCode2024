import argparse, math, sys
from collections import defaultdict
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

def score(s):
	if 'a' <= s <= 'z':
		return ord(s) - ord('a') + 1
	if 'A' <= s <= 'Z':
		return ord(s) - ord('A') + 27

def part_1(lines):
	s = 0
	for i in lines:
		assert len(i) % 2 == 0
		a = set(i[:len(i)//2]).intersection(set(i[len(i)//2:]))
		assert len(a) == 1
		s += score(next(iter(a)))
	return s

def part_2(lines):
	s = 0
	count = len(lines) // 3
	assert len(lines) % 3 == 0
	lines = iter(lines)
	for i in range(count):
		j0, j1, j2 = next(lines), next(lines), next(lines)
		a = set(j0).intersection(j1).intersection(j2)
		assert len(a) == 1
		s += score(next(iter(a)))
	return s

if __name__ == '__main__':
	main()

