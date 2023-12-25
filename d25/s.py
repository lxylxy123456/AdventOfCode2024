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

class Graph:
	def __init__(self):
		self.E = defaultdict(set)
	def add_edge(self, v1, v2):
		assert v1 != v2
		assert v2 not in self.E[v1]
		assert v1 not in self.E[v2]
		self.E[v1].add(v2)
		self.E[v2].add(v1)
	def remove_edge(self, v1, v2):
		assert v2 in self.E[v1]
		assert v1 in self.E[v2]
		self.E[v1].remove(v2)
		self.E[v2].remove(v1)
	def all_edges(self):
		for k, v in self.E.items():
			for i in v:
				if k < i:
					yield k, i

def read_graph(lines):
	g = Graph()
	for i in lines:
		src, dsts = i.split(':')
		for dst in dsts.split():
			g.add_edge(src, dst)
	return g

def graphviz(g):
	print('graph {')
	for src, dst in g.all_edges():
		print('\t' + src, '--', dst)
	print('}')

def dfs_clusters(g):
	visited = defaultdict(set)
	clusters = []

	def visit(v):
		visited[v] = True
		clusters[-1].append(v)
		for i in g.E[v]:
			if not visited[i]:
				visit(i)

	for v in g.E:
		if not visited[v]:
			clusters.append([])
			visit(v)

	return clusters

def part_1(lines):
	s = 0
	g = read_graph(lines)
	graphviz(g)
	all_edges = list(g.all_edges())
	for index, i in enumerate(all_edges):
		print(index, '/', len(all_edges))
		g.remove_edge(*i)
		for jndex, j in enumerate(all_edges[:index]):
			g.remove_edge(*j)
			for kndex, k in enumerate(all_edges[:jndex]):
				g.remove_edge(*k)
				clusters = dfs_clusters(g)
				if len(clusters) == 2:
					print(list(map(len, clusters)))
					return functools.reduce(operator.mul, map(len, clusters))
				if len(clusters) != 1:
					print('Error:')
					print(len(clusters))
					print(list(map(len, clusters)))
				g.add_edge(*k)
			g.add_edge(*j)
		g.add_edge(*i)
	return s

def part_2(lines):
	s = 0
	for i in lines:
		i
	return s

if __name__ == '__main__':
	main()

