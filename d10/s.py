# Youtube: https://youtu.be/Dy3bzhMWHzE

import argparse, math, sys, re, functools, operator, itertools
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

VE = (0, 1)
VW = (0, -1)
VN = (-1, 0)
VS = (1, 0)
str2vecs = {
	'|': (VN, VS),	# | is a vertical pipe connecting north and south.
	'-': (VE, VW),	# - is a horizontal pipe connecting east and west.
	'L': (VN, VE),	# L is a 90-degree bend connecting north and east.
	'J': (VN, VW),	# J is a 90-degree bend connecting north and west.
	'7': (VS, VW),	# 7 is a 90-degree bend connecting south and west.
	'F': (VS, VE),	# F is a 90-degree bend connecting south and east.
	'.': (),		# . is ground; there is no pipe in this tile.
	'S': (VN, VE, VW, VS),
}

def get_elem(lines, x, y):
	if x in range(len(lines)):
		if y in range(len(lines[0])):
			return lines[x][y]
	return '.'

def get_loop(lines):
	conn = []
	for i in lines:
		conn.append([])
		for j in i:
			conn[-1].append(set())
	for x in range(len(lines)):
		for y in range(len(lines[0])):
			for dx, dy in str2vecs[lines[x][y]]:
				if (-dx, -dy) in str2vecs[get_elem(lines, x + dx, y + dy)]:
					conn[x][y].add((dx, dy))
	start = None
	for x in range(len(lines)):
		for y in range(len(lines[0])):
			if lines[x][y] == 'S':
				assert start is None
				start = (x, y)
	assert start is not None
	loop = [start]
	prev = None
	while True:
		x, y = loop[-1]
		dx, dy = next(filter(lambda x: x != prev, conn[x][y]))
		prev = (-dx, -dy)
		cur = (x + dx, y + dy)
		loop.append(cur)
		if cur == start:
			break
	return conn, loop

def part_1(lines):
	s = 0
	conn, loop = get_loop(lines)
	if len(loop) % 2 == 1:
		s = (len(loop) - 1) // 2
	else:
		raise NotImplementedError
	return s

def part_2(lines):
	s = 0
	conn, loop = get_loop(lines)
	for x in range(len(lines)):
		in_loop = False
		# 0: not on loop
		# -1: enter from top
		# 1: enter from bottom
		enter = 0
		#print(x)
		for y in range(len(lines[0])):
			#print(in_loop, enter, end='\t')
			if (x, y) in loop:
				if enter == 0:
					if VE in conn[x][y]:
						if VN in conn[x][y]:
							enter = -1
						elif VS in conn[x][y]:
							enter = 1
						else:
							raise ValueError
					else:
						in_loop = not in_loop
				else:
					assert VW in conn[x][y]
					if VE in conn[x][y]:
						pass
					elif VS in conn[x][y]:
						# Exit from bottom
						if enter == -1:
							in_loop = not in_loop
						enter = 0
					elif VN in conn[x][y]:
						# Exit from top
						if enter == 1:
							in_loop = not in_loop
						enter = 0
					else:
						raise ValueError
			else:
				if in_loop:
					s += 1
		assert not in_loop
		assert enter == 0

	return s

if __name__ == '__main__':
	main()

