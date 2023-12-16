"""
Build a directed graph G = (V, E). For each tile, create 4 vertices: light to
the left, right, up, and down. Then two vertices are connected if a mirror
reflects a vertex to another. Then use DFS to find Strongly Connected
Components (SCC) of the graph. If any vertex in the SCC is lit, all vertices
are lit. Then topologically sort the SCCs, and traverse it to find the size of
downstream SCCs. Finally, for each possible entrance, look up SCC size. Take
the maximum.
"""

import argparse, math, sys, re, functools, operator, itertools
from collections import defaultdict, Counter
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

L = (0, -1)
R = (0, 1)
U = (-1, 0)
D = (1, 0)

class Tile:
	def __init__(self, mirror, x, y, tiles):
		self.mirror = mirror
		self.x = x
		self.y = y
		self.tiles = tiles
	def reflect(self, light):
		if self.mirror == '.':
			return [light]
		elif self.mirror == '/':
			return [{L: D, D: L, U: R, R: U}[light]]
		elif self.mirror == '\\':
			return [{L: U, U: L, D: R, R: D}[light]]
		elif self.mirror == '-':
			if light in [L, R]:
				return [light]
			else:
				return [L, R]
		elif self.mirror == '|':
			if light in [U, D]:
				return [light]
			else:
				return [U, D]
		else:
			raise ValueError
	def next_tile(self, vec):
		x = self.x + vec[0]
		y = self.y + vec[1]
		if x in range(len(self.tiles)) and y in range(len(self.tiles[0])):
			return self.tiles[x][y]
		else:
			return None
	def __repr__(self):
		return repr(self.__dict__)

def dfs(V, E, sort=lambda x: x):
	# Ref: Introduction to Algorithms, Third Edition, page 604
	time = 0
	color = defaultdict(lambda: 'WHITE')
	f = {}
	sccs = []

	def dfs_visit(u):
		nonlocal time
		time += 1
		sccs[-1].append(u)
		color[u] = 'GRAY'
		for v in E[u]:
			if color[v] == 'WHITE':
				dfs_visit(v)
		color[u] = 'BLACK'
		time += 1
		f[u] = time

	for u in sort(V):
		if color[u] == 'WHITE':
			sccs.append([])
			dfs_visit(u)

	return (sccs, f)

def strongly_connected_components(V, E, E_rev):
	# Ref: Introduction to Algorithms, Third Edition, page 617
	_, f = dfs(V, E)
	sccs, _ = dfs(V, E_rev,
				  lambda x: sorted(x, key=lambda y: f[y], reverse=True))
	return sccs

def solve(lines, entrance):
	I = len(lines)
	J = len(lines[0])

	# Build tiles, same as s.py.
	tiles = []
	for index, i in enumerate(lines):
		tiles.append([])
		for jndex, j in enumerate(i):
			tiles[-1].append(Tile(j, index, jndex, tiles))

	# Build G = (V, E).
	V = []
	E = defaultdict(list)
	E_rev = defaultdict(list)
	for i in range(I):
		for j in range(J):
			for k in [L, R, U, D]:
				V.append((i, j, *k))
	for i, j, *k in V:
		k = tuple(k)
		t = tiles[i][j]
		for k_new in t.reflect(k):
			n = t.next_tile(k_new)
			if n is not None:
				s = (i, j, *k)
				d = (n.x, n.y, *k_new)
				E[s].append(d)
				E_rev[d].append(s)

	# Build SCC
	sccs = strongly_connected_components(V, E, E_rev)
	v2scc = {}
	for index, i in enumerate(sccs):
		for j in i:
			v2scc[j] = index

	# Build G^SCC
	Vscc = range(len(sccs))
	Escc = defaultdict(set)
	Escc_rev = defaultdict(set)
	for u, vs in E.items():
		u_scc = v2scc[u]
		for v in vs:
			v_scc = v2scc[v]
			Escc[u_scc].add(v_scc)
			Escc_rev[v_scc].add(u_scc)
	entrance_scc = set()
	for i in entrance:
		entrance_scc.add(v2scc[i])

	# DFS algorithm for SCC
	def light(u, visited):
		visited.add(u)
		for v in Escc[u]:
			if v not in visited:
				light(v, visited)

	# Brute force
	s = 0
	for i in entrance_scc:
		visited = set()
		light(i, visited)
		lighted = set()
		for j in visited:
			for x, y, _, _ in sccs[j]:
				lighted.add((x, y))
		s = max(s, len(lighted))

	return s

def part_1(lines):
	entrance = [(0, 0, *R)]
	return solve(lines, entrance)

def part_2(lines):
	I = len(lines)
	J = len(lines[0])
	entrance = []
	for i in range(I):
		entrance.append((i, 0, *R))
		entrance.append((i, J - 1, *L))
	for j in range(J):
		entrance.append((0, j, *D))
		entrance.append((I - 1, j, *U))
	return solve(lines, entrance)

if __name__ == '__main__':
	main()

