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

def compute_cont(rec):
	assert '?' not in rec
	return list(map(len, re.findall('\#+', ''.join(rec))))

def try_combinations(rec, unknowns, cont):
	if unknowns:
		s = 0
		i = unknowns.pop()
		assert rec[i] == '?'
		rec[i] = '.'
		s += try_combinations(rec, unknowns, cont)
		rec[i] = '#'
		s += try_combinations(rec, unknowns, cont)
		rec[i] = '?'
		unknowns.append(i)
		return s
	else:
		if compute_cont(rec) == cont:
			return 1
		else:
			return 0

def solve_1(rec, cont):
	unknowns = []
	for index, i in enumerate(rec):
		if i == '?':
			unknowns.append(index)
	return try_combinations(list(rec), unknowns, cont)

def part_1(lines):
	s = 0
	for i in lines:
		rec, cont = i.split()
		cont = list(map(int, cont.split(',')))
		s += solve_1(rec, cont)
	return s

def part_2(lines):
	s = 0
	for i in lines:
		rec, cont = i.split()
		cont = list(map(int, cont.split(',')))
		s += solve_1('?'.join([rec] * 5), cont * 5)
	return s

if __name__ == '__main__':
	main()

