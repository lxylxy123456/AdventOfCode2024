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

VE = (0, 1)
VW = (0, -1)
VN = (-1, 0)
VS = (1, 0)

VR = (0, 1)
VL = (0, -1)
VU = (-1, 0)
VD = (1, 0)
V = {'R': VR, 'L': VL, 'U': VU, 'D': VD}

def vec_neg(v):
	return tuple(map(operator.neg, v))

def vec_add(v1, v2):
	return tuple(map(operator.add, v1, v2))

def part_1(lines):
	# TODO: compute start
	loop = [(250, 60)]
	conn = defaultdict(set)

	for i in lines:
		matched = re.fullmatch('([LRUD]) (\d+) \(\#([0-9a-f]{6})\)', i)
		direction, length, color = matched.groups()
		length = int(length)
		color = int(color, 16)
		for i in range(length):
			cur = loop[-1]
			v = V[direction]
			nex = vec_add(cur, v)
			loop.append(nex)
			conn[cur].add(v)
			conn[nex].add(vec_neg(v))

	assert loop[0] == loop[-1]
	loop = set(loop)

	#print(max(map(operator.itemgetter(0), loop)))
	#print(max(map(operator.itemgetter(1), loop)))
	#print(loop)
	#print(conn)

	s = 0
	# TODO: constant
	for x in range(500):
		in_loop = False
		# 0: not on loop
		# -1: enter from top
		# 1: enter from bottom
		enter = 0
		#print(x)
		# TODO: constant
		for y in range(500):
			#print(in_loop, enter, end='\t')
			if (x, y) in loop:
				if enter == 0:
					if VE in conn[x, y]:
						if VN in conn[x, y]:
							enter = -1
						elif VS in conn[x, y]:
							enter = 1
						else:
							raise ValueError
					else:
						in_loop = not in_loop
				else:
					assert VW in conn[x, y]
					if VE in conn[x, y]:
						pass
					elif VS in conn[x, y]:
						# Exit from bottom
						if enter == -1:
							in_loop = not in_loop
						enter = 0
					elif VN in conn[x, y]:
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

	s += len(loop) - 1
	return s

def vec_mult(c, v):
	return tuple(map(lambda x: c * x, v))

def part_2(lines):
	s = 0
	cur = (0, 0)
	# [((curx, cury), dir, length), ...]
	segments = []
	for i in lines:
		matched = re.fullmatch('([LRUD]) (\d+) \(\#([0-9a-f]{6})\)', i)
		direction, length, color = matched.groups()

		#direction = V[direction]
		#length = int(length)

		direction = {'0': VR, '1': VD, '2': VL, '3': VU, }[color[-1]]
		length = int(color[:-1], 16)

		segments.append((cur, direction, length))
		cur = vec_add(cur, vec_mult(length, direction))

	assert cur == (0, 0)

	for index, (cur, direction, length) in enumerate(segments):
		prev_dir = segments[(index - 1 + len(segments)) % len(segments)][1]
		next_dir = segments[(index + 1 + len(segments)) % len(segments)][1]
		#print(direction, prev_dir, next_dir)
		if direction == VR:
			adj = {
				(VU, VU): 0,
				(VD, VU): -1,
				(VU, VD): 1,
				(VD, VD): 0,
			}[prev_dir, next_dir]
			s -= cur[0] * (length + adj)
			#print('-', cur[0], '*', (length + adj))
		elif direction == VL:
			adj = {
				(VU, VU): 0,
				(VD, VU): 1,
				(VU, VD): -1,
				(VD, VD): 0,
			}[prev_dir, next_dir]
			s += (cur[0] + 1) * (length + adj)
			#print('+', (cur[0] + 1), '*', (length + adj))
		else:
			pass

	nodes = list(map(operator.itemgetter(0), segments))
	#s += max(map(operator.itemgetter(0), nodes)) - min(map(operator.itemgetter(0), nodes))
	# TODO: ???
	#s -= 1

	#print(952408144115)
	#print(s - 952408144115)
	return s

if __name__ == '__main__':
	main()

