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

# TODO: cache
@functools.lru_cache(10485760)
def solve_2_recu(rec, cont, nh, nq, nc):
	if 1:
		assert (nh, nq, nc) == (rec.count('#'), rec.count('?'), sum(cont))
	# TODO: (nh, nq, nc)
	if not rec:
		if not cont:
			return 1
		else:
			return 0
	if rec[0] == '.':
		return solve_2_recu(rec[1:], cont, nh, nq, nc)
	elif rec[0] == '#':
		if not cont:
			return 0
		n = cont[0]
		if ((sum(map('?#'.__contains__, rec[:n])) == n) and
			(len(rec) == n or rec[n] in '.?')):
			# TODO
			return solve_2_recu(rec[n+1:], cont[1:], rec[n+1:].count('#'), rec[n+1:].count('?'), nc - n)
		else:
			return 0
	else:
		s = 0
		s += solve_2_recu('.' + rec[1:], cont, nh, nq - 1, nc)
		s += solve_2_recu('#' + rec[1:], cont, nh + 1, nq - 1, nc)
		return s

def solve_2(rec, cont):
	return solve_2_recu(rec, tuple(cont), rec.count('#'), rec.count('?'), sum(cont))

def part_2(lines):
	s = 0
	for index, i in enumerate(lines):
		print(index)
		rec, cont = i.split()
		cont = list(map(int, cont.split(',')))
		s += solve_2('?'.join([rec] * 5), cont * 5)
	return s

if __name__ == '__main__':
	main()

