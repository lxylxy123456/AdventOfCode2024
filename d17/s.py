# Youtube: https://youtu.be/irtIc2NfqCM

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

def emulate1(operator, operand, reg, out, ip):
	# Returns new value of ip.
	def get_combo(operand):
		if operand in range(4):
			return operand
		elif operand == 4:
			return reg['A']
		elif operand == 5:
			return reg['B']
		elif operand == 6:
			return reg['C']
		else:
			raise ValueError
	if operator == 0:	# adv
		reg['A'] = reg['A'] // (2 ** get_combo(operand))
	elif operator == 1:	# bxl
		reg['B'] ^= operand
	elif operator == 2:	# bst
		reg['B'] = get_combo(operand) % 8
	elif operator == 3:	# jnz
		if reg['A'] != 0:
			return operand
	elif operator == 4:	# bxc
		reg['B'] ^= reg['C']
	elif operator == 5:	# out
		out.append(get_combo(operand) % 8)
	elif operator == 6:	# bdv
		reg['B'] = reg['A'] // (2 ** get_combo(operand))
	elif operator == 7:	# cdv
		reg['C'] = reg['A'] // (2 ** get_combo(operand))
	else:
		raise ValueError
	return ip + 2

def read(lines):
	l = iter(lines)
	reg = {
		'A': int(re.fullmatch('Register A: (\d+)', next(l)).groups()[0]),
		'B': int(re.fullmatch('Register B: (\d+)', next(l)).groups()[0]),
		'C': int(re.fullmatch('Register C: (\d+)', next(l)).groups()[0]),
	}
	assert next(l) == ''
	program_text = re.fullmatch('Program: (.+)', next(l)).groups()[0]
	program = list(map(int, program_text.split(',')))
	return reg, program

def run1(reg, program):
	out = []
	ip = 0
	while True:
		try:
			operator, operand = program[ip], program[ip + 1]
		except IndexError:
			break
		ip = emulate1(operator, operand, reg, out, ip)
	return out

def part_1(lines):
	s = 0
	reg, program = read(lines)
	out = run1(reg, program)
	return ','.join(map(str, out))

def part_2(lines):
	s = 0
	reg, program = read(lines)
	def recu(program, reg, level, base):
		for i in range(8):
			r = reg.copy()
			r['A'] = base + 8 ** (level) * i
			if r['A'] < 0:
				continue
			out = run1(r, program)
			#print(base, level, out, out == program)
			if out == program:
				return base + 8 ** (level) * i
			if len(out) == len(program) and out[level:] == program[level:]:
				ans = recu(program, reg, level - 1, base + 8 ** (level) * i)
				if ans is not None:
					return ans
		return None
	s = recu(program, reg, len(program) - 1, 0)
	assert s is not None
	return s

if __name__ == '__main__':
	main()

