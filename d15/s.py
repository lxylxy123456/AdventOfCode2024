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

def aoc_hash(x):
	h = 0
	for i in x:
		h = (h + ord(i)) * 17 % 256
	return h

def part_1(lines):
	s = 0
	for i in lines[0].split(','):
		s += aoc_hash(i)
	return s

def part_2(lines):
	s = 0
	boxes = []
	for i in range(256):
		boxes.append([])

	for i in lines[0].split(','):
		label, op, focal = re.fullmatch('(\w+)(\-|\=(\d+))', i).groups()
		box = boxes[aoc_hash(label)]
		if op == '-':
			for index, (l, f) in enumerate(box):
				if l == label:
					assert box.pop(index) == [l, f]
					break
		else:
			assert op.startswith('=')
			focal = int(focal)
			assert focal in range(1, 10)
			for lf in box:
				if lf[0] == label:
					lf[1] = focal
					break
			else:
				box.append([label, focal])
		if not 'print box':
			print('---')
			for index, box in enumerate(boxes):
				if box:
					print(index, box)

	for index, box in enumerate(boxes):
		for jndex, (l, f) in enumerate(box):
			s += (1 + index) * (1 + jndex) * f
			print((1 + index) * (1 + jndex) * f)

	return s

if __name__ == '__main__':
	main()

