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

C2V = {
	'>': (0, 1),
	'v': (1, 0),
	'<': (0, -1),
	'^': (-1, 0),
}

def read_input1(lines):
	m = []
	l = iter(lines)
	while True:
		line = next(l)
		if not line:
			break
		m.append(list(line))
	a = []
	for i in l:
		for j in i:
			a.append(C2V[j])
	X = len(m)
	Y = len(m[0])
	rx = None
	ry = None
	for x in range(X):
		for y in range(Y):
			if m[x][y] == '@':
				assert rx is None and ry is None
				rx = x
				ry = y
	assert rx is not None and ry is not None
	return m, a, X, Y, rx, ry

def part_1(lines):
	s = 0
	m, a, X, Y, rx, ry = read_input1(lines)
	for dx, dy in a:
		ox, oy = rx + dx, ry + dy
		assert ox in range(X) and oy in range(Y)
		while m[ox][oy] == 'O':
			ox += dx
			oy += dy
			assert ox in range(X) and oy in range(Y)
		if m[ox][oy] == '.':
			# Move.
			m[ox][oy] = 'O'
			m[rx][ry] = '.'
			rx += dx
			ry += dy
			m[rx][ry] = '@'
		else:
			# No move.
			assert m[ox][oy] == '#'
	for x in range(X):
		for y in range(Y):
			if m[x][y] == 'O':
				s += 100 * x + y
	#for i in m:
	#	print(*i, sep='')
	return s

def read_input2(lines):
	m = []
	l = iter(lines)
	while True:
		line = next(l)
		if not line:
			break
		f = {'@': '@.', '#': '##', 'O': '[]', '.': '..'}.__getitem__
		m.append(list(itertools.chain.from_iterable(map(f, line))))
	a = []
	for i in l:
		for j in i:
			a.append(C2V[j])
	X = len(m)
	Y = len(m[0])
	rx = None
	ry = None
	for x in range(X):
		for y in range(Y):
			if m[x][y] == '@':
				assert rx is None and ry is None
				rx = x
				ry = y
	assert rx is not None and ry is not None
	return m, a, X, Y, rx, ry

def push2_buggy(m, X, Y, rx, ry, dx, dy):
	# Returns (if moving, list of boxes pushed using GPS coordinates).
	# List of boxes are sorted where furthest boxes first pushed appear first.
	if m[rx + dx][ry + dy] == '#':
		return False, []
	elif m[rx + dx][ry + dy] == '.':
		return True, []
	elif m[rx + dx][ry + dy] == '[':
		ox, oy = rx + dx, ry + dy
	elif m[rx + dx][ry + dy] == ']':
		ox, oy = rx + dx, ry + dy - 1
	else:
		raise ValueError
	# Continuation of previous elif's.
	assert m[rx + dx][ry + dy] in '[]'
	if dx:
		assert not dy
		m1, s1 = push2(m, X, Y, ox, oy, dx, dy)
		m2, s2 = push2(m, X, Y, ox, oy + 1, dx, dy)
		if not m1 or not m2:
			return False, []
		return True, s1 + s2 + [(ox, oy)]
	else:
		assert dy
		m, s = push2(m, X, Y, rx + dx, ry + dy * 2, dx, dy)
		if not m:
			return False, []
		return True, s + [(ox, oy)]

def push2(m, X, Y, rx, ry, dx, dy):
	'''
	Compared my solution with a random solution on Reddit to find my error.
		https://www.reddit.com/r/adventofcode/comments/1hele8m/comment/m24p2od/
		https://gitlab.com/davidsharick/advent-of-code-2024/
			-/blob/main/day15/day15.py
	Minimal input that triggers the error:
		######
		#....#
		#.OO.#
		#.OO@#
		#.OO.#
		#....#
		######

		<>vv<<<^
	The bug is that push2() does not return boxes layer by layer.
	Also it does not deduplicate the list.
	'''
	# Returns (if moving, list of boxes pushed using GPS coordinates).
	# List of boxes are not sorted. The caller should sort them.
	if m[rx + dx][ry + dy] == '#':
		return False, set()
	elif m[rx + dx][ry + dy] == '.':
		return True, set()
	elif m[rx + dx][ry + dy] == '[':
		ox, oy = rx + dx, ry + dy
	elif m[rx + dx][ry + dy] == ']':
		ox, oy = rx + dx, ry + dy - 1
	else:
		raise ValueError
	# Continuation of previous elif's.
	assert m[rx + dx][ry + dy] in '[]'
	if dx:
		assert not dy
		s = {(ox, oy)}
		m1, s1 = push2(m, X, Y, ox, oy, dx, dy)
		m2, s2 = push2(m, X, Y, ox, oy + 1, dx, dy)
		if not m1 or not m2:
			return False, []
		s.update(s1)
		s.update(s2)
		return True, s
	else:
		assert dy
		m, s = push2(m, X, Y, rx + dx, ry + dy * 2, dx, dy)
		if not m:
			return False, []
		s.add((ox, oy))
		return True, s

def part_2(lines):
	s = 0
	m, a, X, Y, rx, ry = read_input2(lines)
	for dx, dy in a:
		move, boxes = push2(m, X, Y, rx, ry, dx, dy)
		# Lines below are added after finding the bug.
		boxes = sorted(boxes, key=lambda x: (-1) * (x[0] * dx + x[1] * dy))
		# Lines above are added after finding the bug.
		if move:
			for ox, oy in boxes:
				m[ox][oy] = '.'
				m[ox][oy + 1] = '.'
				m[ox + dx][oy + dy] = '['
				m[ox + dx][oy + dy + 1] = ']'
			m[rx][ry] = '.'
			rx += dx
			ry += dy
			m[rx][ry] = '@'
		if 0:
			for i in m:
				print(*i, sep='')
			print('-')
			#input()
	for x in range(X):
		for y in range(Y):
			if m[x][y] == '[':
				s += 100 * x + y
	return s

if __name__ == '__main__':
	main()

