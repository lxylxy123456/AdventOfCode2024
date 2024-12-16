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

def find_map(m, X, Y, c):
	for x in range(X):
		for y in range(Y):
			if m[x][y] == c:
				return (x, y)

def part_1(lines):
	s = 0
	X = len(lines)
	Y = len(lines[0])
	sx, sy = find_map(lines, X, Y, 'S')
	ex, ey = find_map(lines, X, Y, 'E')
	visited = set()
	q = [(0, (sx, sy), (0, 1))]
	while q:
		dist, (cx, cy), (dx, dy) = heapq.heappop(q)
		if ((cx, cy), (dx, dy)) in visited:
			continue
		visited.add(((cx, cy), (dx, dy)))
		if lines[cx][cy] == 'E':
			return dist
		elif lines[cx][cy] == '#':
			pass
		elif lines[cx][cy] in ['.', 'S']:
			heapq.heappush(q, (dist + 1, (cx + dx, cy + dy), (dx, dy)))
			heapq.heappush(q, (dist + 1001, (cx + dy, cy + dx), (dy, dx)))
			heapq.heappush(q, (dist + 1001, (cx - dy, cy - dx), (-dy, -dx)))
			if lines[cx][cy] == 'S':
				heapq.heappush(q, (dist + 2001, (cx - dx, cy - dy), (-dx, -dy)))
		else:
			raise ValueError
	for i in lines:
		print(i)
	return s

def dfs2(lines, X, Y, max_dist, dist, cx, cy, dx, dy, visited):
	if dist > max_dist:
		return False
	if lines[cx][cy] == 'E':
		assert dist == max_dist
		visited.add((cx, cy))
		return True
	elif lines[cx][cy] == '#':
		return False
	elif lines[cx][cy] in ['.', 'S']:
		c1 = dfs2(lines, X, Y, max_dist, dist + 1, cx + dx, cy + dy, dx, dy, visited)
		c2 = dfs2(lines, X, Y, max_dist, dist + 1001, cx + dy, cy + dx, dy, dx, visited)
		c3 = dfs2(lines, X, Y, max_dist, dist + 1001, cx - dy, cy - dx, -dy,
				  -dx, visited)
		if lines[cx][cy] == 'S':
			c4 = dfs2(lines, X, Y, max_dist, dist + 2001, cx - dx, cy - dy, -dx,
					  -dy, visited)
		else:
			c4 = False
		if any([c1, c2, c3, c4]):
			visited.add((cx, cy))
			return True
		else:
			return False
	else:
		raise ValueError

def part_2(lines):
	s = 0
	X = len(lines)
	Y = len(lines[0])
	max_dist = part_1(lines)
	sx, sy = find_map(lines, X, Y, 'S')
	ex, ey = find_map(lines, X, Y, 'E')
	visited = set()
	dfs2(lines, X, Y, max_dist, 0, sx, sy, 0, 1, visited)
	s = len(visited)
	return s

if __name__ == '__main__':
	main()

