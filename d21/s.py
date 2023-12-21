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

VECS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def vec_add(v1, v2):
	return tuple(map(operator.add, v1, v2))

def vec_mult(c, v):
	return tuple(map(lambda x: c * x, v))

def get_start(lines):
	start = None
	for index, i in enumerate(lines):
		for jndex, j in enumerate(i):
			if j == 'S':
				start = (index, jndex)
	assert start is not None
	return start

def compute_dist(lines, start):
	dist = []
	for index, i in enumerate(lines):
		dist.append([])
		for jndex, j in enumerate(i):
			dist[-1].append(None)

	in_map = lambda x, y: x in range(len(lines)) and y in range(len(lines[0]))
	cur_dist = 0
	frontier = {start}
	while frontier:
		new_frontier = set()
		for x, y in frontier:
			dist[x][y] = cur_dist
			for dx, dy in VECS:
				nx, ny = vec_add((x, y), (dx, dy))
				if (in_map(nx, ny) and lines[nx][ny] in 'S.' and
					dist[nx][ny] is None):
					new_frontier.add((nx, ny))
		frontier = new_frontier
		cur_dist += 1

	return dist

def part_1(lines):
	s = 0
	STEPS = 64
	start = get_start(lines)
	dist = compute_dist(lines, start)
	for i in dist:
		for j in i:
			if j is not None and j <= STEPS and j % 2 == STEPS % 2:
				s += 1
	return s

def part_2(lines):
	start = get_start(lines)

	I = len(lines)
	assert I == len(lines[0])
	for i in range(I):
		assert lines[0][i] == '.'
		assert lines[-1][i] == '.'
		assert lines[i][0] == '.'
		assert lines[i][-1] == '.'
		assert lines[i][start[1]] in 'S.'
		assert lines[i][start[1]] in 'S.'
		assert lines[start[0]][i] in 'S.'
		assert lines[start[0]][i] in 'S.'

	S = start[0]
	assert S == start[1]
	assert S * 2 + 1 == I

	STARTS = [start, (0, 0), (I - 1, 0), (I - 1, I - 1), (0, I - 1),
			  (0, start[1]), (I - 1, start[1]), (start[0], 0),
			  (start[0], I - 1)]

	@functools.cache
	def _compute_dist(s):
		assert s in STARTS
		return compute_dist(lines, s)

	@functools.cache
	def _compute_count(start):
		dist = _compute_dist(start)
		c = Counter(itertools.chain.from_iterable(dist))
		del c[None]
		ans = []
		for i in range(max(c.keys()) + 1):
			if i < 2:
				ans.append(c[i])
			else:
				ans.append(ans[-2] + c[i])
		assert len(ans) < I * 2, 'Assumption failed: need to detour'
		return ans

	def cover_square(start, steps):
		if steps < 0:
			return 0
		c = _compute_count(start)
		try:
			return c[steps]
		except IndexError:
			if (steps - len(c)) % 2 == 0:
				return c[len(c) - 2]
			else:
				return c[len(c) - 1]

	STEPS = 26501365

	n = STEPS // I + 3
	s = 0

	# Current square
	s += cover_square(start, STEPS)

	# Go one way
	for i in range(n):
		steps = STEPS - (S + 1) - i * I
		s += cover_square((I - 1, S), steps)
		s += cover_square((S, I - 1), steps)
		s += cover_square((0, S), steps)
		s += cover_square((S, 0), steps)
	assert steps < 0

	# Go multiple ways
	for i in range(n):
		m = i + 1
		assert m >= 0
		steps = STEPS - (S + 1) * 2 - i * I
		s += m * cover_square((I - 1, 0), steps)
		s += m * cover_square((0, I - 1), steps)
		s += m * cover_square((0, 0), steps)
		s += m * cover_square((I - 1, I - 1), steps)
	assert steps < 0

	#print(STEPS, s, (STEPS + 1)**2)
	#assert s == (STEPS + 1)**2
	return s

if __name__ == '__main__':
	main()

