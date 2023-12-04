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

def part_1(lines):
	s = 0
	for i in lines:
		a, b, c = re.fullmatch('Card +(\d+): (.+)\|(.+)', i).groups()
		int(a)
		win = list(map(int, b.split()))
		my = list(map(int, c.split()))
		score = 0
		for i in my:
			if i in win:
				if score == 0:
					score = 1
				else:
					score *= 2
		s += score
		#d = len(set(win).intersection(my))
		#assert len(my) == len(set(my))
		#assert len(win) == len(set(win))
		#if d:
		#	s += 2 ** (d - 1)
	return s

def part_2(lines):
	s = 0
	copies = Counter()
	for i in lines:
		a, b, c = re.fullmatch('Card +(\d+): (.+)\|(.+)', i).groups()
		a = int(a)
		win = list(map(int, b.split()))
		my = list(map(int, c.split()))
		score = 0
		for i in my:
			if i in win:
				score += 1
		# Original
		copies[a] += 1
		for j in range(score):
			copies[a + j + 1] += copies[a]
	s = sum(copies.values())
	return s

if __name__ == '__main__':
	main()

