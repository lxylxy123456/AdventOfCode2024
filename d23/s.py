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

def read_map(lines):
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
	return I, entry, exit, in_map

def part_1(lines):
	I, entry, exit, in_map = read_map(lines)

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

def count_intersections(lines, I, entry, exit, in_map):
	c = Counter()
	for index, i in enumerate(lines):
		for jndex, j in enumerate(i):
			if j != '#':
				count = 0
				for p in map(lambda x: vec_add((index, jndex), x), VECS.keys()):
					if in_map(*p):
						if lines[p[0]][p[1]] != '#':
							count += 1
				c[count] += 1
	return c

class Graph:
	def __init__(self):
		# key: coordinate in map, value: order
		# (can be calculated from self.E)
		self.V = Counter()
		# E[v1][v2] = E[v2][v1] = length
		self.E = defaultdict(dict)
	def convert_edge(self, e):
		return tuple(sorted(e))
	def add_edge(self, e, k):
		e = self.convert_edge(e)
		v1, v2 = e
		assert v1 not in self.E[v2]
		assert v2 not in self.E[v1]
		self.E[v1][v2] = k
		self.E[v2][v1] = k
		self.V[v1] += 1
		self.V[v2] += 1
	def remove_edge(self, e):
		e = self.convert_edge(e)
		v1, v2 = e
		k = self.E[v1].pop(v2)
		assert k == self.E[v2].pop(v1)
		self.V[v1] -= 1
		self.V[v2] -= 1
		return k
	def shrink_node(self, v):
		assert self.V[v] == 2
		assert len(self.E[v]) == 2
		v1, v2 = self.E[v].keys()
		k1 = self.remove_edge((v, v1))
		k2 = self.remove_edge((v, v2))
		self.add_edge((v1, v2), k1 + k2)
		assert self.V[v] == 0

def part_2(lines):
	I, entry, exit, in_map = read_map(lines)
	print(count_intersections(lines, I, entry, exit, in_map))

	# Construct graph
	g = Graph()
	for index, i in enumerate(lines):
		for jndex, j in enumerate(i):
			if j == '#':
				continue
			v1 = (index, jndex)
			for dv in [(1, 0), (0, 1)]:
				v2 = vec_add(v1, dv)
				if not in_map(*v2) or lines[v2[0]][v2[1]] == '#':
					continue
				g.add_edge((v1, v2), 1)

	# Shrink graph
	for count in range(2):
		found = False
		for v, order in list(g.V.items()):
			if order == 2:
				g.shrink_node(v)
				found = True
		assert found == (count == 0)

	#print(g.V)
	#print(g.E)

	def visit(p, dist, path):
		nonlocal exit, in_map, g
		if p in path:
			return -1
		if p == exit:
			return dist
		ans = -1
		path.add(p)
		for np, dd in g.E[p].items():
			assert in_map(*np)
			assert lines[np[0]][np[1]] != '#'
			ans = max(ans, visit(np, dist + dd, path))
		path.remove(p)
		return ans

	s = visit(entry, 0, set())
	return s

if __name__ == '__main__':
	main()

