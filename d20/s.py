# https://youtu.be/p1D42_2ZNTU

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

def get_init_state(typ):
	if typ == '':
		return None
	elif typ == '%':
		return [False]
	elif typ == '&':
		return defaultdict(bool)
	else:
		raise ValueError

def read_nodes(lines):
	# name: (typ, [dst_names], [src_names], state)
	nodes = {}
	for i in lines:
		matched = re.fullmatch(r'([\%\&]?)(\w+) -> ((?:\w+, )*\w+)', i)
		typ, src, dsts = matched.groups()
		assert src not in nodes
		nodes[src] = (typ, dsts.split(', '), [], get_init_state(typ))
	for i, (_, d, _, _) in list(nodes.items()):
		for j in d:
			if j not in nodes:
				nodes[j] = ('', [], [], None)
			nodes[j][2].append(i)
	return nodes

def process_signal(nodes, signals, src, node, is_high):
	if nodes[node][0] == '':
		# Broadcaster
		for i in nodes[node][1]:
			signals.append((node, i, is_high))
	elif nodes[node][0] == '%':
		# Flip-flop
		if not is_high:
			if nodes[node][3][0]:
				nodes[node][3][0] = False
				for i in nodes[node][1]:
					signals.append((node, i, False))
			else:
				nodes[node][3][0] = True
				for i in nodes[node][1]:
					signals.append((node, i, True))
	elif nodes[node][0] == '&':
		# Conjunction
		nodes[node][3][src] = is_high
		send = not (sum(nodes[node][3].values()) == len(nodes[node][2]))
		for i in nodes[node][1]:
			signals.append((node, i, send))
	else:
		raise ValueError

def part_1(lines):
	nodes = read_nodes(lines)
	s_count = Counter()
	for _ in range(1000):
		# (src, node, is_high)
		signals = deque()
		signals.append((None, 'broadcaster', False))
		while signals:
			src, node, is_high = signals.popleft()
			s_count[is_high] += 1
			process_signal(nodes, signals, src, node, is_high)
	s = s_count[False] * s_count[True]
	return s

def graphviz(nodes):
	print('digraph G {')
	for k, (v0, v1, v2, v3) in nodes.items():
		print('\t%s [label=\"%s%s\"];' % (k, v0, k))
		for i in v1:
			print('\t%s -> %s;' % (k, i))
	print('}')

def part_2(lines):
	nodes = read_nodes(lines)

	graphviz(nodes)

	if 'rx' not in nodes:
		return NotImplemented

	stats = defaultdict(list)

	for s in range(100000000000000000000000000000000000000000000000000):
		#if s % 10000 == 0:
		#	print(s)
		# (src, node, is_high)
		signals = deque()
		signals.append((None, 'broadcaster', False))
		while signals:
			src, node, is_high = signals.popleft()
			if src in nodes['qt'][2] and is_high:
				stats[src].append(s)
			process_signal(nodes, signals, src, node, is_high)

		#print(sum(nodes['gl'][3].values()), end=' ', flush=True)
		if len(stats) == 4 and min(map(len, stats.values())) > 4:
			break

	# Check period
	diffs = []
	for i in stats.values():
		diff = i[0] + 1
		for jndex, j in enumerate(i):
			assert j == (1 + jndex) * diff - 1
		diffs.append(diff)

	s = functools.reduce(operator.mul, diffs)
	return s

if __name__ == '__main__':
	main()

