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

def parse_input(lines):
	groups = [[]]
	for i in lines:
		if i:
			groups[-1].append(i)
		else:
			groups.append([])
	return groups

def get_refl_row(matrix):
	for i in range(1, len(matrix)):
		a = matrix[i:]
		b = matrix[i - 1:: -1]
		if all(map(operator.eq, a, b)):
			yield i

def get_refl_col(matrix):
	transpose = []
	for i in range(len(matrix[0])):
		s = ''
		for j in range(len(matrix)):
			s += matrix[j][i]
		transpose.append(''.join(s))
	yield from get_refl_row(transpose)

def part_1(lines):
	s = 0
	for i in parse_input(lines):
		#print('i')
		for j in get_refl_row(i):
			#print('row', j)
			s += j * 100
		for j in get_refl_col(i):
			#print('col', j)
			s += j
	return s

def get_refl_row_2(matrix):
	for i in range(1, len(matrix)):
		a = matrix[i:]
		b = matrix[i - 1:: -1]
		if sum(map(lambda x, y: sum(map(operator.ne, x, y)), a, b)) == 1:
			yield i

def get_refl_col_2(matrix):
	transpose = []
	for i in range(len(matrix[0])):
		s = ''
		for j in range(len(matrix)):
			s += matrix[j][i]
		transpose.append(''.join(s))
	yield from get_refl_row_2(transpose)

def part_2(lines):
	s = 0
	for i in parse_input(lines):
		#print('i')
		for j in get_refl_row_2(i):
			#print('row', j)
			s += j * 100
		for j in get_refl_col_2(i):
			#print('col', j)
			s += j
	return s

if __name__ == '__main__':
	main()

