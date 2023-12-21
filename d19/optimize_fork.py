"""Solve part 2 using os.fork(). Report result using os.pipe()."""

import argparse, math, os, sys, re, functools, operator, itertools, heapq, json
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

def part_1(lines):
	return NotImplemented

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

def q_init():
	return os.pipe()

def send(queue, data):
	r, w = queue
	data = json.dumps(data).encode() + b'\n'
	assert os.write(w, data) == len(data)

def recv(queue, buf=bytearray()):
	r, w = queue
	while b'\n' not in buf:
		data = os.read(r, 4096)
		if not data:
			raise EOFError
		buf.extend(data)
	i = buf.index(b'\n')
	ans = json.loads(buf[:i])
	right = buf[i + 1:]
	buf.clear()
	buf.extend(right)
	return ans

def send_and_exit(queue, data):
	send(queue, data)
	exit(0)

def fork_wrapper(queue, put=True):
	if put:
		send(queue, None)
	result = os.fork()
	if result == 0:
		return False
	if result > 0:
		return True
	raise Exception('Fork failed: %d' % result)

def run_workflow_range(wf, parts, queue):
	cur = 'in'
	while True:
		if cur == 'A':
			s = functools.reduce(operator.mul, map(len, parts.values()))
			send_and_exit(queue, s)
		if cur == 'R':
			send_and_exit(queue, 0)
		for var, op, operand, jmp in wf[cur]:
			if var is not None:
				if fork_wrapper(queue):
					if op == '<':
						parts[var] = range_op(parts[var], '<', operand)
					else:
						parts[var] = range_op(parts[var], '>', operand)
					if not all(map(len, parts)):
						send_and_exit(queue, 0)
				else:
					if op == '<':
						parts[var] = range_op(parts[var], '>=', operand)
					else:
						parts[var] = range_op(parts[var], '<=', operand)
					if not all(map(len, parts)):
						send_and_exit(queue, 0)
					continue
			cur = jmp
			break

def part_2(lines):
	s = 0
	lines = iter(lines)
	wf = read_wf(lines)
	rng = range(1, 4000 + 1)
	parts = {'x': rng, 'm': rng, 'a': rng, 's': rng}
	queue = q_init()
	if not fork_wrapper(queue, put=False):
		run_workflow_range(wf, parts, queue)
		assert False, 'should not return'

	pending = 1
	while pending:
		data = recv(queue)
		if data is None:
			pending += 1
		else:
			s += data
			pending -= 1

	return s

if __name__ == '__main__':
	main()

