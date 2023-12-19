# Youtube: https://youtu.be/ZakocMnsFDk

import argparse, math, sys, re, functools, operator, itertools, heapq
from collections import defaultdict, Counter
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

def read_wf(lines):
	wf = {}
	for i in lines:
		if not i:
			break
		name, entries = re.fullmatch(r'(\w+)\{(.+)\}', i).groups()
		prog = []
		for j in entries.split(','):
			matched = re.fullmatch(r'(?:(\w+)([<>])(\d+):)?(\w+)', j)
			var, op, operand, jmp = matched.groups()
			if operand is not None:
				operand = int(operand)
			prog.append((var, op, operand, jmp))
			#print(var, op, operand, jmp)
		assert name not in wf
		wf[name] = prog
	return wf

def read_parts(lines):
	parts = []
	for i in lines:
		matched = re.fullmatch(r'\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}', i)
		parts.append(list(map(int, matched.groups())))
	return parts

def run_workflow(wf, xmas):
	x, m, a, s = xmas
	part = {'x': x, 'm': m, 'a': a, 's': s}

	cur = 'in'
	while True:
		if cur == 'A':
			return True
		if cur == 'R':
			return False
		for var, op, operand, jmp in wf[cur]:
			if var is not None:
				op = {
					'>': operator.gt,
					'<': operator.lt,
				}[op]
				if not op(part[var], operand):
					continue
			cur = jmp
			break

def run_workflow_recursive(wf, xmas, cur='in', ind=0):
	x, m, a, s = xmas
	part = {'x': x, 'm': m, 'a': a, 's': s}

	if cur == 'A':
		return True
	if cur == 'R':
		return False
	var, op, operand, jmp = wf[cur][ind]
	if var is not None:
		op = {
			'>': operator.gt,
			'<': operator.lt,
		}[op]
		if not op(part[var], operand):
			return run_workflow_recursive(wf, xmas, cur, ind + 1)
	return run_workflow_recursive(wf, xmas, jmp, 0)

def part_1(lines):
	total = 0
	lines = iter(lines)
	wf = read_wf(lines)
	parts = read_parts(lines)

	for x, m, a, s in parts:
		ans = run_workflow(wf, (x, m, a, s))
		ans2 = run_workflow_recursive(wf, (x, m, a, s))
		assert ans == ans2
		if ans:
			total += x + m + a + s

	return total

def range_op(rng, op, operand):
	if op == '>':
		return range(max(rng.start, operand + 1), rng.stop)
	elif op == '>=':
		return range(max(rng.start, operand), rng.stop)
	elif op == '<':
		return range(rng.start, min(operand, rng.stop))
	elif op == '<=':
		return range(rng.start, min(operand + 1, rng.stop))
	else:
		raise ValueError

def run_workflow_range(wf, part, cur='in', ind=0):
	if not all(part.values()):
		return 0
	if cur == 'A':
		return functools.reduce(operator.mul, map(len, part.values()))
	if cur == 'R':
		return 0
	var, op, operand, jmp = wf[cur][ind]

	s = 0
	if var is not None:
		part_false = part.copy()
		part_true = part.copy()
		if op == '<':
			part_true[var] = range_op(part_true[var], '<', operand)
			part_false[var] = range_op(part_false[var], '>=', operand)
		else:
			assert op == '>'
			part_true[var] = range_op(part_true[var], '>', operand)
			part_false[var] = range_op(part_false[var], '<=', operand)
	else:
		part_false = {'x': [], 'm': [], 'a': [], 's': []}
		part_true = part
	s += run_workflow_range(wf, part_false, cur, ind + 1)
	s += run_workflow_range(wf, part_true, jmp, 0)
	return s

def part_2(lines):
	s = 0
	lines = iter(lines)
	wf = read_wf(lines)
	rng = range(1, 4000 + 1)
	parts = {'x': rng, 'm': rng, 'a': rng, 's': rng}
	s = run_workflow_range(wf, parts)
	return s

if __name__ == '__main__':
	main()

