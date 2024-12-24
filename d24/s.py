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

def read_input(lines):
	init_vals = {}
	l = iter(lines)
	for i in l:
		if not i:
			break
		k, v = re.fullmatch('(\w{3}): ([01])', i).groups()
		init_vals[k] = int(v)
	rules = []
	for i in l:
		matched = re.fullmatch('(\w{3}) (AND|OR|XOR) (\w{3}) -> (\w{3})', i)
		lhs, op, rhs, res = matched.groups()
		rules.append((lhs, op, rhs, res))
	return init_vals, rules

def dfs1(rules):
	# Topological sort.
	V = set()
	E = defaultdict(set)
	for lhs, op, rhs, res in rules:
		V.add(lhs)
		V.add(rhs)
		V.add(res)
		E[lhs].add(res)
		E[rhs].add(res)
	visited = set()
	ans = []
	def f(n):
		if n in visited:
			return
		visited.add(n)
		for i in E[n]:
			f(i)
		ans.append(n)
	for i in V:
		f(i)
	return list(reversed(ans))

def part_1(lines):
	s = ''
	init_vals, rules = read_input(lines)
	order = dfs1(rules)
	ans_lookup = {}
	for lhs, op, rhs, res in rules:
		ans_lookup[res] = (lhs, op, rhs)
	result = {}
	for i in order:
		if i in init_vals:
			result[i] = bool(init_vals[i])
		else:
			lhs, op, rhs = ans_lookup[i]
			lhs_v = result[lhs]
			rhs_v = result[rhs]
			if op == 'AND':
				res_v = lhs_v and rhs_v
			elif op == 'OR':
				res_v = lhs_v or rhs_v
			elif op == 'XOR':
				res_v = lhs_v and not rhs_v or not lhs_v and rhs_v
			else:
				raise ValueError
			result[i] = res_v
	for k, v in sorted(result.items(), reverse=True):
		if k.startswith('z'):
			s += str(int(v))
	return int(s, 2)

def graphviz(rules, f):
	print('digraph G {', file=f)
	for lhs, op, rhs, res in rules:
		print('\t{%s; %s} -> %s;' % (lhs, rhs, res), file=f)
		print('\t%s [label="%s\\n%s"];' % (res, op, res), file=f)
	print('}', file=f)

def part_2(lines):
	s = 0
	init_vals, rules = read_input(lines)
	graphviz(rules, sys.stderr)
	ans = [
		'z11', 'wpd',	# 11
		'skh', 'jqf',	# 15
		'mdd', 'z19',	# 19
		'z37', 'wts',	# 37
	]
	return ','.join(sorted(ans))

if __name__ == '__main__':
	main()

