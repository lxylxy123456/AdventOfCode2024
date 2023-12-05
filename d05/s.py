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
	parser.add_argument('-b', '--b2', action='store_true', help='Only part 2')
	parser.add_argument('input_file', nargs='?')
	args = parser.parse_args()
	if args.input_file is not None:
		f = open(args.input_file)
	else:
		f = sys.stdin
	lines = list(read_lines(f))
	if not args.two:
		print(part_1(lines))
	if args.b2:
		print(part_2_bruteforce(lines))
	if not args.one:
		print(part_2(lines))

def read_input(ilines):
	seeds = list(map(int, re.fullmatch('seeds: (.+)',
									   next(ilines)).groups()[0].split()))
	assert not next(ilines)
	maps = []
	for i in range(7):
		cur_map = (next(ilines), [])
		maps.append(cur_map)
		while True:
			line = next(ilines, '')
			if line:
				cur_map[1].append(list(map(int, line.split())))
			else:
				break
	return (seeds, maps)

def lookup_map(m, x):
	for y0, x0, l in m[1]:
		if x in range(x0, x0 + l):
			return x - x0 + y0
	return x

def part_1(lines):
	s = 0
	seeds, maps = read_input(iter(lines))
	locs = []
	for i in seeds:
		for j in maps:
			i = lookup_map(j, i)
		locs.append(i)
	s = min(locs)
	return s

def part_2_bruteforce(lines):
	s = 0
	seeds, maps = read_input(iter(lines))
	locs = []
	for i0, i1 in zip(*([iter(seeds)] * 2)):
		for i in range(i0, i0 + i1):
			for j in maps:
				i = lookup_map(j, i)
			locs.append(i)
	#print(locs)
	s = min(locs)
	return s

def lookup_map_seg(m, segments):
	cur_map = []
	for y0, x0, l in m[1]:
		cur_map.append((range(x0, x0 + l), y0 - x0))
	cur_map.sort(key=lambda x: x[0].start)
	segments = sorted(segments, key=lambda x: x.start)
	while segments:
		if len(segments[0]) == 0:
			segments.pop(0)
		elif not cur_map:
			# No intersection, segments first
			yield segments.pop(0)
		elif segments[0].stop <= cur_map[0][0].start:
			# No intersection, segments first
			yield segments.pop(0)
		elif cur_map[0][0].stop <= segments[0].start:
			# No intersection, map first
			cur_map.pop(0)
		elif segments[0].start < cur_map[0][0].start:
			# Intersection, segments first
			yield range(segments[0].start, cur_map[0][0].start)
			segments[0] = range(cur_map[0][0].start, segments[0].stop)
		else:
			# Intersection, map first
			stop = min(segments[0].stop, cur_map[0][0].stop)
			delta = cur_map[0][1]
			yield range(segments[0].start + delta, stop + delta)
			segments[0] = range(stop, segments[0].stop)

def merge_segs(segs):
	cur = None
	for i in sorted(segs, key=lambda x: x.start):
		if cur is None:
			cur = i
		else:
			if cur.start >= i.stop:
				cur = range(cur.start, max(cur.stop, i.stop))
			else:
				yield cur
				cur = i
	if cur is not None:
		yield cur

def part_2(lines):
	#return part_2_bruteforce(lines)
	s = 0
	seeds, maps = read_input(iter(lines))
	segs = []
	for i0, i1 in zip(*([iter(seeds)] * 2)):
		segs.append(range(i0, i0 + i1))
	for j in maps:
		segs = list(lookup_map_seg(j, segs))
		#print(segs)
		segs = list(merge_segs(segs))
		#print(segs)
	s = min(segs, key=lambda x: x.start).start
	return s

if __name__ == '__main__':
	main()

