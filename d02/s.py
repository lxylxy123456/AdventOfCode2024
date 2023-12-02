import argparse, math, sys, re, functools, operator
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

def parse_set(s):
	ans = {'red': 0, 'green': 0, 'blue': 0}
	for i in s.split(','):
		matched = re.fullmatch('(\d+) (red|green|blue)', i.strip())
		a, b = matched.groups()
		assert ans[b] == 0
		ans[b] += int(a)
	return ans

def part_1(lines):
	s = 0
	for i in lines:
		a, b = i.split(':')
		game_id = int(re.fullmatch('Game (\d+)', a).groups()[0])
		for j in b.split(';'):
			se = parse_set(j)
			if se['red'] <= 12 and se['green'] <= 13 and se['blue'] <= 14:
				pass
			else:
				break
		else:
			s += game_id
	return s

def part_2(lines):
	s = 0
	for i in lines:
		a, b = i.split(':')
		game_id = int(re.fullmatch('Game (\d+)', a).groups()[0])
		m = {'red': 0, 'green': 0, 'blue': 0}
		for j in b.split(';'):
			se = parse_set(j)
			for k in m.keys():
				m[k] = max(m[k], se[k])
		s += functools.reduce(operator.mul, m.values())
	return s

if __name__ == '__main__':
	main()

