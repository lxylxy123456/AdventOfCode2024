# Youtube: https://youtu.be/xnivJsoyMqs

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

def check_update1(rules, update):
	for index, i in enumerate(update):
		for j in update[:index]:
			if (i, j) in rules:
				return False
	return True

def part_1(lines):
	s = 0
	x = lines.index('')
	rules = set()
	for i in lines[:x]:
		rules.add(tuple(map(int, re.fullmatch(r'(\d+)\|(\d+)', i).groups())))
	updates = []
	for i in lines[x + 1:]:
		updates.append(list(map(int, i.split(','))))
	for update in updates:
		assert len(update) % 2 == 1
		if check_update1(rules, update):
			s += update[(len(update) - 1) // 2]
	return s

def fix_order(rules, update):
	fix = []
	while update:
		x = update[0]
		for i in update:
			if (i, x) in rules:
				x = i
		update.remove(x)
		fix.append(x)
	return fix

def part_2(lines):
	s = 0
	x = lines.index('')
	rules = set()
	for i in lines[:x]:
		rules.add(tuple(map(int, re.fullmatch(r'(\d+)\|(\d+)', i).groups())))
	updates = []
	for i in lines[x + 1:]:
		updates.append(list(map(int, i.split(','))))
	for update in updates:
		assert len(update) % 2 == 1
		if check_update1(rules, update):
			pass
		else:
			fix = fix_order(rules, update)
			s += fix[(len(fix) - 1) // 2]
	return s

if __name__ == '__main__':
	main()

