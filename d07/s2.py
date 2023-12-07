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

CARDS = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']

def rank_card(x):
	return CARDS.index(x)

def get_type(x):
	assert 'J' not in x
	c = Counter(x)
	if c.most_common(1)[0][1] == 5:
    	# Five of a kind, where all five cards have the same label: AAAAA
		return 6
	elif c.most_common(1)[0][1] == 4:
		# Four of a kind, where four cards have the same label and one card has
		# a different label: AA8AA
		return 5
	elif c.most_common(1)[0][1] == 3 and c.most_common(2)[1][1] == 2:
		# Full house, where three cards have the same label, and the remaining
		# two cards share a different label: 23332
		return 4
	elif c.most_common(1)[0][1] == 3:
		# Three of a kind, where three cards have the same label, and the
		# remaining two cards are each different from any other card in the
		# hand: TTT98
		return 3
	elif c.most_common(1)[0][1] == 2 and c.most_common(2)[1][1] == 2:
		# Two pair, where two cards share one label, two other cards share a
		# second label, and the remaining card has a third label: 23432
		return 2
	elif c.most_common(1)[0][1] == 2:
		# One pair, where two cards share one label, and the other three cards
		# have a different label from the pair and each other: A23A4
		return 1
	else:
		# High card, where all cards' labels are distinct: 23456
		assert c.most_common(1)[0][1] == 1
		return 0

def get_types(x):
	# Greedy algorithm: all J's should all match a same existing card.
	# The only exception is 'JJJJJ', which can all match 'A'.
	if x == 'JJJJJ':
		return get_type('AAAAA')
	if 'J' not in x:
		return get_type(x)
	choices = set(x)
	choices.remove('J')
	ans = []
	for i in choices:
		ans.append(get_type(x.replace('J', i)))
	return max(ans)

def get_hand(x):
	return [get_types(x), *map(rank_card, x)]

def part_2(lines):
	s = 0
	data = []
	for i in lines:
		hand, bid = i.split()
		data.append((get_hand(hand), hand, int(bid)))
	data.sort()
	for i, j in zip(data, data[1:]):
		assert i[0] != j[0]
	for index, i in enumerate(data, 1):
		s += index * i[2]
	return s

def part_1(lines):
	raise NotImplementedError

if __name__ == '__main__':
	main()

