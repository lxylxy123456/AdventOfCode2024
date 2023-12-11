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

def solve(lines, x):
	s = 0
	galaxies = []
	occupied_row = set()
	occupied_col = set()
	for index, i in enumerate(lines):
		for jndex, j in enumerate(i):
			if j == '#':
				galaxies.append((index, jndex))
				occupied_row.add(index)
				occupied_col.add(jndex)
	# Distance from row 0 to row i
	dist_row = [0]
	# Distance from col 0 to col i
	dist_col = [0]
	for i in range(len(lines)):
		dist_row.append(dist_row[-1] + (1 if i in occupied_row else x))
	for i in range(len(lines[0])):
		dist_col.append(dist_col[-1] + (1 if i in occupied_col else x))
	for index, i in enumerate(galaxies):
		for jndex, j in enumerate(galaxies[:index]):
			s += abs(dist_row[i[0]] - dist_row[j[0]])
			s += abs(dist_col[i[1]] - dist_col[j[1]])
	return s

def part_1(lines):
	return solve(lines, 2)

def part_2(lines):
	return solve(lines, 1000000)

if __name__ == '__main__':
	main()

