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

class Brick:
	def __init__(self, ind, data):
		self.id = ind
		(self.x0, self.y0, self.z0), (self.x1, self.y1, self.z1) = data
		assert 0 <= self.x0 <= self.x1
		assert 0 <= self.y0 <= self.y1
		assert 0 < self.z0 <= self.z1
	def xy_intersect(self, rhs):
		return (max(self.x0, rhs.x0) <= min(self.x1, rhs.x1) and
				max(self.y0, rhs.y0) <= min(self.y1, rhs.y1))
	def z_intersect(self, rhs):
		return max(self.z0, rhs.z0) <= min(self.z1, rhs.z1)
	def fall(self, ground):
		assert self.z0 > ground
		dist = self.z0 - ground - 1
		self.z0 -= dist
		self.z1 -= dist
	def __repr__(self):
		return 'Brick%s' % repr(tuple(self.__dict__.values()))

def read_bricks(lines):
	bricks = []
	for index, i in enumerate(lines):
		data = list(map(lambda x: list(map(int, x.split(','))), i.split('~')))
		bricks.append(Brick(index, data))
	if not 'sanity check':
		for index, i in enumerate(bricks):
			for j in bricks[:index]:
				assert not (i.xy_intersect(j) and i.z_intersect(j))
	bricks.sort(key=lambda x: x.z0)
	return bricks

def get_supports(bricks):
	# supports[i] = support for blocks[i]
	supports = defaultdict(set)
	for index, i in enumerate(bricks):
		support = set()
		adj_ground = 0
		for j in bricks[:index]:
			if i.xy_intersect(j):
				if adj_ground < j.z1:
					adj_ground = j.z1
					support = set()
				if adj_ground == j.z1:
					support.add(j.id)
		i.fall(adj_ground)
		supports[i.id] = support
		#print(i.id, support)
	return supports

def part_1(lines):
	bricks = read_bricks(lines)
	supports = get_supports(bricks)
	unsafe_bricks = set()
	for support in supports.values():
		if len(support) == 1:
			unsafe_bricks.update(support)
	s = len(bricks) - len(unsafe_bricks)
	#print(unsafe_bricks)
	#print(*bricks, sep='\n')
	return s

def part_2(lines):
	bricks = read_bricks(lines)
	supports = get_supports(bricks)
	s = 0
	#print(supports)
	for index, i in enumerate(bricks):
		#print(i)
		collapsed = {i.id}
		for j in bricks[index:]:
			if supports[j.id] and supports[j.id].issubset(collapsed):
				#print('\t', j)
				collapsed.add(j.id)
		s += len(collapsed) - 1
	return s

if __name__ == '__main__':
	main()

