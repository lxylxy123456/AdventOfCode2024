import argparse, math, sys, re
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

def get_adjacent(lines, row, col):
	if 0 <= row < len(lines):
		if 0 <= col < len(lines[0]):
			return not re.match('[0-9\.]', lines[row][col])

def part_1(lines):
	s = 0
	for index, i in enumerate(lines):
		for j in re.finditer('[0-9]+', i):
			l, r = j.span()
			adj = False
			for x in range(l - 1, r + 1):
				for y in range(index - 1, index + 2):
					if get_adjacent(lines, y, x):
						adj = True
			if adj:
				s += int(j.group())
	return s

def part_2(lines):
	s = 0
	adj_list = defaultdict(list)
	for index, i in enumerate(lines):
		for j in re.finditer('[0-9]+', i):
			l, r = j.span()
			adj = False
			for x in range(l - 1, r + 1):
				for y in range(index - 1, index + 2):
					if get_adjacent(lines, y, x):
						adj_list[y, x].append(int(j.group()))
	for i in adj_list.values():
		if len(i) == 2:
			s += i[0] * i[1]
	return s

if __name__ == '__main__':
	main()

