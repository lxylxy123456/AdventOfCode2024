# Youtube: https://youtu.be/g8bZojvOaUg

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
	line, = lines
	f = []
	s0 = 0
	s1 = False
	for i in line:
		if s1:
			s0 += 1
			s1 = False
			c = None
		else:
			s1 = True
			c = s0
		for _ in range(int(i)):
			f.append(c)

	p0 = 0
	p1 = len(f) - 1
	while p0 < p1:
		if f[p0] is not None:
			p0 += 1
			continue
		if f[p1] is None:
			p1 -= 1
			continue
		f[p0], f[p1] = f[p1], f[p0]

	for index, i in enumerate(f):
		if i is not None:
			s += index * i
	return s

def part_2(lines):
	s = 0
	line, = lines
	f = []	# (size, id)
	s0 = 0
	s1 = False
	for i in line:
		if s1:
			s0 += 1
			s1 = False
			c = None
		else:
			s1 = True
			c = s0
		f.append([int(i), c])
	f.append([0, None])

	for fid in range(s0, -1, -1):
		# Find block to be moved.
		for index, (size, i) in enumerate(f):
			if i == fid:
				break
		else:
			raise ValueError('Not found')
		old_index = index
		old_size = size
		# Find empty space to move to.
		for index, (size, i) in enumerate(f):
			if i is None and size >= old_size:
				break
		else:
			continue
		new_index = index
		new_size = size
		# Don't move to later.
		if new_index > old_index:
			continue
		# Remove old.
		assert f[old_index - 1][1] is None
		assert f[old_index + 1][1] is None
		f[old_index - 1][0] += f[old_index][0] + f[old_index + 1][0]
		f.pop(old_index)
		f.pop(old_index)
		# Add new.
		f[new_index][0] -= old_size
		f.insert(new_index, [old_size, fid])
		f.insert(new_index, [0, None])

	pos = 0
	for size, fid in f:
		for _ in range(size):
			if fid is not None:
				s += pos * fid
			pos += 1
#	print(f)
	return s

if __name__ == '__main__':
	main()

