# Youtube: https://youtu.be/tXR-1t0AkTg

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

L = (0, -1)
R = (0, 1)
U = (-1, 0)
D = (1, 0)

class Tile:
	def __init__(self, mirror, x, y, tiles):
		self.mirror = mirror
		self.x = x
		self.y = y
		self.tiles = tiles
		self.light = set()
	def reflect(self, light):
		if self.mirror == '.':
			return [light]
		elif self.mirror == '/':
			return [{L: D, D: L, U: R, R: U}[light]]
		elif self.mirror == '\\':
			return [{L: U, U: L, D: R, R: D}[light]]
		elif self.mirror == '-':
			if light in [L, R]:
				return [light]
			else:
				return [L, R]
		elif self.mirror == '|':
			if light in [U, D]:
				return [light]
			else:
				return [U, D]
		else:
			raise ValueError
	def next_tile(self, vec):
		x = self.x + vec[0]
		y = self.y + vec[1]
		if x in range(len(self.tiles)) and y in range(len(self.tiles[0])):
			return self.tiles[x][y]
		else:
			return None
	def __repr__(self):
		return repr(self.__dict__)

def let_there_be_light(lines, enter, vec):
	s = 0
	tiles = []
	for index, i in enumerate(lines):
		tiles.append([])
		for jndex, j in enumerate(i):
			tiles[-1].append(Tile(j, index, jndex, tiles))
	init_tile = tiles[enter[0]][enter[1]]
	init_tile.light.add(vec)
	frontier = [(init_tile, vec)]
	while frontier:
		tile, light = frontier.pop()
		for i in tile.reflect(light):
			n = tile.next_tile(i)
			if n is not None and i not in n.light:
				n.light.add(i)
				frontier.append((n, i))
	for i in tiles:
		for j in i:
			if j.light:
				s += 1
	return s

def part_1(lines):
	return let_there_be_light(lines, (0, 0), R)

def part_2(lines):
	s = 0
	I = len(lines)
	J = len(lines[0])
	for i in range(I):
		s = max(s, let_there_be_light(lines, (i, 0), R))
		s = max(s, let_there_be_light(lines, (i, J - 1), L))
	for j in range(J):
		s = max(s, let_there_be_light(lines, (0, j), D))
		s = max(s, let_there_be_light(lines, (I - 1, j), U))
	return s

if __name__ == '__main__':
	main()

