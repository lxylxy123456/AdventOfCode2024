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

def _get_paths(begin, end, loc):
	bx, by = loc[begin]
	ex, ey = loc[end]
	ans = ''
	if bx < ex:
		ans += (ex - bx) * 'v'
	else:
		ans += (bx - ex) * '^'
	if by < ey:
		ans += (ey - by) * '>'
	else:
		ans += (by - ey) * '<'
	# TODO: maybe there is no need to interleave
	ret = []
	for i in set(itertools.permutations(ans)):
		ret.append(''.join(i))
	return ret

@functools.cache
def get_paths_num(begin, end):
	loc = {
		'7': (0, 0),
		'8': (0, 1),
		'9': (0, 2),
		'4': (1, 0),
		'5': (1, 1),
		'6': (1, 2),
		'1': (2, 0),
		'2': (2, 1),
		'3': (2, 2),
		'0': (3, 1),
		'A': (3, 2),
	}
	return _get_paths(begin, end, loc)

@functools.cache
def get_paths_dir(begin, end):
	loc = {
		'^': (0, 1),
		'A': (0, 2),
		'<': (1, 0),
		'v': (1, 1),
		'>': (1, 2),
	}
	return _get_paths(begin, end, loc)

def solve_level1(output, level):
	prev = 'A'
	assert output[-1] == 'A'
	seq_choices = ['']
	for i in output:
		new_seq_choices = []
		for j in itertools.product(seq_choices, level(prev, i)):
			new_seq_choices.append(''.join(j) + 'A')
		seq_choices = new_seq_choices
		prev = i
	return seq_choices

def solve_sequence1(output, levels):
	seqs = [output]
	for level in levels:
		new_seqs = []
		for i in seqs:
			new_seqs.extend(solve_level1(i, level))
		seqs = new_seqs
	return min(seqs, key=len)

def part_1(lines):
	s = 0
	levels = [get_paths_num, get_paths_dir, get_paths_dir]
	for i in lines:
		seq = solve_sequence1(i, levels)
		print(int(i.strip('A')), len(seq))
		s += len(seq) * int(i.strip('A'))
	return s

def part_2(lines):
	s = 0
	for i in lines:
		i
	return s

if __name__ == '__main__':
	main()

