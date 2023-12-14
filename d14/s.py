# Youtube: https://youtu.be/wND4vNoAlw4

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

def roll_n(rocks):
	for i in range(len(rocks[0])):
		o_count = 0
		for j in range(len(rocks) - 1, -1, -1):
			if rocks[j][i] == '#':
				for k in range(o_count):
					assert rocks[j + k + 1][i] == '.'
					rocks[j + k + 1][i] = 'O'
				o_count = 0
			elif rocks[j][i] == 'O':
				rocks[j][i] = '.'
				o_count += 1
			else:
				assert rocks[j][i] == '.'
		for k in range(o_count):
			assert rocks[k][i] == '.'
			rocks[k][i] = 'O'

def compute_load(rocks):
	s = 0
	for index, i in enumerate(rocks):
		load_factor = len(rocks) - index
		for j in i:
			if j == 'O':
				s += load_factor
	return s

def part_1(lines):
	s = 0
	rocks = []
	for i in lines:
		rocks.append(list(i))
	roll_n(rocks)
	s = compute_load(rocks)
	return s

def roll_s(rocks):
	for i in range(len(rocks[0])):
		o_count = 0
		for j in range(len(rocks)):
			if rocks[j][i] == '#':
				for k in range(o_count):
					assert rocks[j - k - 1][i] == '.'
					rocks[j - k - 1][i] = 'O'
				o_count = 0
			elif rocks[j][i] == 'O':
				rocks[j][i] = '.'
				o_count += 1
			else:
				assert rocks[j][i] == '.'
		for k in range(o_count):
			assert rocks[len(rocks) - k - 1][i] == '.'
			rocks[len(rocks) - k - 1][i] = 'O'

def roll_e(rocks):
	for i in range(len(rocks)):
		o_count = 0
		for j in range(len(rocks[0])):
			if rocks[i][j] == '#':
				for k in range(o_count):
					assert rocks[i][j - k - 1] == '.'
					rocks[i][j - k - 1] = 'O'
				o_count = 0
			elif rocks[i][j] == 'O':
				rocks[i][j] = '.'
				o_count += 1
			else:
				assert rocks[i][j] == '.'
		for k in range(o_count):
			assert rocks[i][len(rocks[0]) - k - 1] == '.'
			rocks[i][len(rocks[0]) - k - 1] = 'O'

def roll_w(rocks):
	for i in range(len(rocks)):
		o_count = 0
		for j in range(len(rocks) - 1, -1, -1):
			if rocks[i][j] == '#':
				for k in range(o_count):
					assert rocks[i][j + k + 1] == '.'
					rocks[i][j + k + 1] = 'O'
				o_count = 0
			elif rocks[i][j] == 'O':
				rocks[i][j] = '.'
				o_count += 1
			else:
				assert rocks[i][j] == '.'
		for k in range(o_count):
			assert rocks[i][k] == '.'
			rocks[i][k] = 'O'

def roll_nwse(rocks):
	roll_n(rocks)
	roll_w(rocks)
	roll_s(rocks)
	roll_e(rocks)

def hash_rocks(rocks):
	return hash(tuple(map(tuple, rocks)))

def part_2(lines):
	s = 0
	rocks = []
	for i in lines:
		rocks.append(list(i))
	N = 1000000000

	#history = []
	hash_history = defaultdict(list)
	for i in range(N):
		#history.append(rocks)
		h = hash_rocks(rocks)
		hash_history[h].append(i)
		hh = hash_history[h]
		#print(hh)
		if len(hh) >= 2 and (N - hh[-1]) % (hh[-1] - hh[-2]) == 0:
			#print(N, hh[-1], hh[-2])
			break
		roll_nwse(rocks)

	s = compute_load(rocks)
	return s

if __name__ == '__main__':
	main()

