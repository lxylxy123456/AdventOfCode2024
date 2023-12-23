import argparse, math, sys, re, functools, operator, itertools, heapq
from collections import defaultdict, Counter, deque
sys.setrecursionlimit(100000000)
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

VECS = {(0, 1): '>', (1, 0): 'v', (-1, 0): '^', (0, -1): '<'}

def vec_add(v1, v2):
	return tuple(map(operator.add, v1, v2))

def part_1(lines):
	s = 0
	I = len(lines)
	assert len(lines[0]) == I
	entry = (0, 1)
	exit = (I - 1, I - 2)
	for e in [entry, exit]:
		for index, i in enumerate(lines[e[0]]):
			if index == e[1]:
				assert i == '.'
			else:
				assert i == '#'
	in_map = lambda x, y: x in range(I) and y in range(I)

	dist = []
	for i in range(I):
		dist.append([0] * I)

	def visit(p, dist, path):
		nonlocal exit, in_map
		if p in path:
			return -1
		if p == exit:
			return dist
		ans = -1
		path.add(p)
		for k, v in VECS.items():
			np = vec_add(p, k)
			if not in_map(*np):
				continue
			if lines[np[0]][np[1]] == '#':
				continue
			elif lines[np[0]][np[1]] in VECS.values():
				if lines[np[0]][np[1]] != v:
					continue
			else:
				assert lines[np[0]][np[1]] == '.'
			ans = max(ans, visit(np, dist + 1, path))
		path.remove(p)
		return ans

	s = visit(entry, 0, set())

	return s

def part_2(lines):
	s = 0
	for i in lines:
		i
	return s

if __name__ == '__main__':
	main()

