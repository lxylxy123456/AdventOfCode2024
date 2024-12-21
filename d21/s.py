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
	# Previous version did not handle the problem of moving to empty space.
	ret = []
	for i in set(itertools.permutations(ans)):
		valid = True
		cx, cy = bx, by
		for j in i:
			if j == '<':
				cy -= 1
			elif j == 'v':
				cx += 1
			elif j == '>':
				cy += 1
			elif j == '^':
				cx -= 1
			else:
				raise ValueError
			if (cx, cy) not in loc.values():
				valid = False
		if valid:
			ret.append(''.join(i) + 'A')
	return ret

LOC_NUM = {
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

LOC_DIR = {
	'^': (0, 1),
	'A': (0, 2),
	'<': (1, 0),
	'v': (1, 1),
	'>': (1, 2),
}

@functools.cache
def get_paths_num(begin, end):
	return _get_paths(begin, end, LOC_NUM)

@functools.cache
def get_paths_dir(begin, end):
	return _get_paths(begin, end, LOC_DIR)

LEVELS_MAP = {
	'n': get_paths_num,
	'd': get_paths_dir,
}

def solve1(begin, end, levels):
	if not levels:
		return end
	f = LEVELS_MAP[levels[0]]
	cand = None
	for i in f(begin, end):
		cur = solve_moves1(i, levels[1:])
		if cand is None or len(cur) < len(cand):
			cand = cur
	#print(repr(begin), repr(end), repr(levels), repr(cand))
	return cand

def solve_moves1(text, levels):
	assert text.endswith('A')
	ans = ''
	for b, e in zip(('A' + text)[:-1], text):
		ans += solve1(b, e, levels)
	#print(repr(text), repr(levels), repr(ans))
	return ans

def part_1(lines):
	s = 0
	levels = 'ndd'
	for i in lines:
		seq = solve_moves1(i, levels)
		#print(len(seq), int(i.strip('A')))
		s += len(seq) * int(i.strip('A'))
	return s

@functools.cache
def solve2(begin, end, levels):
	if not levels:
		return 1
	f = LEVELS_MAP[levels[0]]
	cand = None
	for i in f(begin, end):
		cur = solve_moves2(i, levels[1:])
		if cand is None or cur < cand:
			cand = cur
	#print(repr(begin), repr(end), repr(levels), repr(cand))
	return cand

@functools.cache
def solve_moves2(text, levels):
	assert text.endswith('A')
	ans = 0
	for b, e in zip(('A' + text)[:-1], text):
		ans += solve2(b, e, levels)
	#print(repr(text), repr(levels), repr(ans))
	return ans

def part_2(lines):
	s = 0
	levels = 'n' + 'd' * 25
	for i in lines:
		seq = solve_moves2(i, levels)
		#print(seq, int(i.strip('A')))
		s += seq * int(i.strip('A'))
	return s

if __name__ == '__main__':
	main()

