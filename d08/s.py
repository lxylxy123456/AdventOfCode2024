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

def part_1(lines):
	s = 0
	strategy = lines[0]
	assert not lines[1]
	mapping = {}
	for i in lines[2:]:
		k, l, r = re.fullmatch('([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)',
							   i).groups()
		assert k not in mapping
		mapping[k] = {'L': l, 'R': r}
	cur = 'AAA'
	while True:
		for i in strategy:
			cur = mapping[cur][i]
			s += 1
			if cur == 'ZZZ':
				return s
	return s

def find_cycle(strategy, mapping, src, dsts):
	# Return ([number of steps], period)
	reached_dst = {}	# dst name -> number of steps
	step = 0
	cur = src
	period = None
	while True:
		for i in strategy:
			cur = mapping[cur][i]
			step += 1
			if cur.endswith('Z'):
				assert cur in dsts
				if cur in reached_dst:
					period = step - reached_dst[cur]
					return (list(reached_dst.values()), period)
				else:
					reached_dst[cur] = step

def part_2(lines):
	s = 0
	strategy = lines[0]
	assert not lines[1]
	mapping = {}
	for i in lines[2:]:
		k, l, r = re.fullmatch('([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)',
							   i).groups()
		assert k not in mapping
		mapping[k] = {'L': l, 'R': r}
	srcs = []
	dsts = []
	for i in mapping:
		if i.endswith('A'):
			srcs.append(i)
		if i.endswith('Z'):
			dsts.append(i)
	ans = []
	for src in srcs:
		info = find_cycle(strategy, mapping, src, dsts)
		assert len(info[0]) == 1
		assert info[0][0] == info[1]
		ans.append(info[1])
	s = functools.reduce(math.lcm, ans)
	return s

if __name__ == '__main__':
	main()

