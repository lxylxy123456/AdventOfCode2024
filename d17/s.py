import argparse, math, sys, re, functools, operator, itertools, heapq
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

INF = 1e100

E = (0, 1)
S = (1, 0)
W = (0, -1)
N = (-1, 0)
vecs = [E, S, W, N]

def vec_add(v1, v2):
	return tuple(map(operator.add, v1, v2))

def solve(lines, min_len, max_len):
	s = 0
	# dp[i][j][k] = arrive at lines[i][j] with straight line heading vecs[k]
	dp = []
	for i in lines:
		dp.append([])
		for j in i:
			dp[-1].append([INF] * 4)
	# init
	#dp[0][0][0] = 0
	I = len(lines)
	J = len(lines[0])
	in_map = lambda x, y: x in range(I) and y in range(J)
	frontier = [(0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 0, 2), (0, 0, 0, 3)]
	while frontier:
		d, i, j, k = heapq.heappop(frontier)
		if dp[i][j][k] <= d:
			continue
		#print(d, i, j, k)
		#if (d, i, j, k) == ():
		#	import pdb; pdb.set_trace()
		dp[i][j][k] = d
		for kk, (di, dj) in enumerate(vecs):
			if kk == k or kk % 2 == k % 2:
				continue
			dd = d
			ii = i
			jj = j
			for step in range(max_len):
				ii, jj = vec_add((ii, jj), (di, dj))
				if not in_map(ii, jj):
					break
				dd += int(lines[ii][jj])
				if step >= min_len:
					if dd < dp[ii][jj][kk]:
						heapq.heappush(frontier, (dd, ii, jj, kk))
	#for i in dp: print(i)
	return min(dp[I - 1][J - 1])

def part_1(lines):
	return solve(lines, 0, 3)

def part_2(lines):
	return solve(lines, 3, 10)

if __name__ == '__main__':
	main()

