# Youtube: https://youtu.be/f_0m98v2tQ8

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

def part_1(lines):
	s = 0
	conn = set()
	for i in lines:
		conn.add(tuple(i.split('-')))
	for i, j in conn:
		assert (j, i) not in conn
	nodes = set()
	for i, j in conn:
		nodes.add(i)
		nodes.add(j)
	for i, j in conn:
		for k in nodes:
			if i <= k or j <= k:
				continue
			if not ((i, k) in conn or (k, i) in conn):
				continue
			if not ((j, k) in conn or (k, j) in conn):
				continue
			if i.startswith('t') or j.startswith('t') or k.startswith('t'):
				s += 1
	return s

def part_2(lines):
	s = 0
	conn = set()
	for i in lines:
		conn.add(tuple(i.split('-')))
	for i, j in conn:
		assert (j, i) not in conn
	nodes = set()
	for i, j in conn:
		nodes.add(i)
		nodes.add(j)

	#print(len(conn), len(nodes))
	adj_list = defaultdict(set)
	for i, j in conn:
		adj_list[i].add(j)
		adj_list[j].add(i)

	parties = []
	# Initialize with size-2 parties
	for i in conn:
		parties.append(tuple(sorted(i)))
	# Increase gradually
	while True:
		new_parties = []
		for i in parties:
			n = functools.reduce(set.intersection, map(adj_list.__getitem__, i))
			for j in n:
				if j > i[-1]:
					new_parties.append(i + (j,))
		if new_parties:
			parties = new_parties
		else:
			assert len(parties) == 1
			s = ','.join(parties[0])
			break
	return s

if __name__ == '__main__':
	main()

