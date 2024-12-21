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
	# Previous version did not handle the problem of moving to empty space
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

def simulate1(text, level):
	loc = {'n': LOC_NUM, 'd': LOC_DIR}[level]
	rev_loc = dict(map(lambda x: (x[1], x[0]), loc.items()))
	cx, cy = loc['A']
	ans = ''
	for i in text:
		if i == 'A':
			ans += rev_loc[(cx, cy)]
		elif i == '<':
			cy -= 1
		elif i == 'v':
			cx += 1
		elif i == '>':
			cy += 1
		elif i == '^':
			cx -= 1
		else:
			raise ValueError
		#print(i, cx, cy)
	assert rev_loc[(cx, cy)] == 'A'
	return ans

def simulate_levels1(text, levels):
	cur = text
	for level in levels:
		cur = simulate1(cur, level)
	return cur

#print(simulate1('<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A', 'd'))
#print(simulate1('v<<A>>^A<A>AvA<^AA>A<vAAA>^A', 'd'))
#print(simulate1('<A^A>^^AvvvA', 'n'))

_0 = '<vA<AA>^>AAvA<^A>AvA^Av<<A>^>AAvA^A<vA>^AA<A>Av<<A>A>^AAAvA<^A>A'
_1 = 'v<<AA>^A>A<AA>AvAA^A<vAAA>^A'
_2 = '<<^A^^A>>AvvvA'
_3 = '179A'
assert len(_0) == 64
assert simulate1(_0, 'd') == _1
assert simulate1(_1, 'd') == _2
assert simulate1(_2, 'n') == _3

r0 = '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'
r1 = '<Av<AA>>^A<AA>AvAA^A<vAAA>^A'
r2 = '^<<A^^A>>AvvvA'
r3 = '179A'
assert len(r0) == 68
assert simulate1(r0, 'd') == r1
assert simulate1(r1, 'd') == r2
assert simulate1(r2, 'n') == r3

for i in [
	'<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A',
	'<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A',
	'<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
	'<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A',
	'<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
]:
	print(simulate_levels1(i, 'ddn'))

def part_1(lines):
	s = 0
	levels = 'ndd'
	for i in lines:
		seq = solve_moves1(i, levels)
		print(len(seq), int(i.strip('A')))
		s += len(seq) * int(i.strip('A'))
	return s

def part_2(lines):
	s = 0
	for i in lines:
		i
	return s

if __name__ == '__main__':
	main()

