# https://youtu.be/gUqzAUnT-b8

import argparse, math, sys, re, functools, operator, itertools, heapq, random
from collections import defaultdict, Counter, deque, namedtuple
from fractions import Fraction
import sympy
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

Vec = namedtuple('Vec', ['x', 'y', 'z'])

class Hailstone:
	def __init__(self, **kwargs):
		for k, v in kwargs.items():
			self.__setattr__(k, v)
	@property
	def p(self):
		return Vec(self.px, self.py, self.pz)
	@property
	def v(self):
		return Vec(self.vx, self.vy, self.vz)

def vec_add(v1, v2):
	return tuple(map(operator.add, v1, v2))

def vec_mul(c, v):
	return tuple(map(lambda x: c * x, v))

def read_input(lines):
	hs = []
	for i in lines:
		exp = '(-?\d+), +(-?\d+), +(-?\d+) @ +(-?\d+), +(-?\d+), +(-?\d+)'
		matched = re.fullmatch(exp, i)
		px, py, pz, vx, vy, vz = map(int, matched.groups())
		hs.append(Hailstone(px=px, py=py, pz=pz, vx=vx, vy=vy, vz=vz))
	return hs

def part_1(lines):
	hs = read_input(lines)
	s = 0
	#test_min, test_max = 7, 27
	test_min, test_max = 200000000000000, 400000000000000
	for index, i in enumerate(hs):
		for j in hs[:index]:
			# i_px + t_i * i_vx = j_px + t_j * j_vx
			# i_py + t_i * i_vy = j_py + t_j * j_vy
			# t_i = ((-j_px*j_vy)+i_px*j_vy+(j_py-i_py)*j_vx)/
			#       (i_vy*j_vx-i_vx*j_vy)
			# t_j = -(i_vx*(i_py-j_py)+i_vy*j_px-i_px*i_vy)/
			#       (i_vy*j_vx-i_vx*j_vy)
			t_i_n = (-j.px*j.vy)+i.px*j.vy+(j.py-i.py)*j.vx
			t_i_d = (i.vy*j.vx-i.vx*j.vy)
			t_j_n = -(i.vx*(i.py-j.py)+i.vy*j.px-i.px*i.vy)
			t_j_d = (i.vy*j.vx-i.vx*j.vy)
			if t_i_d == 0 or t_j_d == 0:
				continue
			t_i = Fraction(t_i_n, t_i_d)
			t_j = Fraction(t_j_n, t_j_d)
			#print(t_i, t_j)
			if t_i == 0 or t_j == 0:
				print(i.px, i.py, j.px, j.py)
				0/0
			if not (t_i >= 0 and t_j >= 0):
				continue
			x = i.px + t_i * i.vx
			y = i.py + t_i * i.vy
			if test_min <= x <= test_max and test_min <= y <= test_max:
				s += 1
	return s

# f(p, v, t) := p + t * v;
# solve([
# 	f(r_px, r_vx, t_1) = f(h1_px, h1_vx, t_1),
# 	f(r_py, r_vy, t_1) = f(h1_py, h1_vy, t_1),
# 	f(r_pz, r_vz, t_1) = f(h1_pz, h1_vz, t_1),
# 	f(r_px, r_vx, t_2) = f(h2_px, h1_vx, t_2),
# 	f(r_py, r_vy, t_2) = f(h2_py, h1_vy, t_2),
# 	f(r_pz, r_vz, t_2) = f(h2_pz, h1_vz, t_2),
# 	f(r_px, r_vx, t_3) = f(h3_px, h1_vx, t_3),
# 	f(r_py, r_vy, t_3) = f(h3_py, h1_vy, t_3),
# 	f(r_pz, r_vz, t_3) = f(h3_pz, h1_vz, t_3)
# ], [r_px, r_py, r_pz, r_vx, r_vy, r_vz, t_1, t_2, t_3]);

def part_2(lines):
	# https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/kepqwbr/
	# https://docs.sympy.org/latest/modules/solvers/solvers.html
	hs = read_input(lines)

	r_px = sympy.Symbol('r_px')
	r_py = sympy.Symbol('r_py')
	r_pz = sympy.Symbol('r_pz')
	r_vx = sympy.Symbol('r_vx')
	r_vy = sympy.Symbol('r_vy')
	r_vz = sympy.Symbol('r_vz')
	t_1 = sympy.Symbol('t_1')
	t_2 = sympy.Symbol('t_2')
	t_3 = sympy.Symbol('t_3')
	symbols = [r_px, r_py, r_pz, r_vx, r_vy, r_vz, t_1, t_2, t_3]

	h1, h2, h3 = hs[0], hs[1], hs[2]
	eqs = [
		(r_px + r_vx * t_1) - (h1.p.x + h1.v.x * t_1),
		(r_py + r_vy * t_1) - (h1.p.y + h1.v.y * t_1),
		(r_pz + r_vz * t_1) - (h1.p.z + h1.v.z * t_1),
		(r_px + r_vx * t_2) - (h2.p.x + h2.v.x * t_2),
		(r_py + r_vy * t_2) - (h2.p.y + h2.v.y * t_2),
		(r_pz + r_vz * t_2) - (h2.p.z + h2.v.z * t_2),
		(r_px + r_vx * t_3) - (h3.p.x + h3.v.x * t_3),
		(r_py + r_vy * t_3) - (h3.p.y + h3.v.y * t_3),
		(r_pz + r_vz * t_3) - (h3.p.z + h3.v.z * t_3),
	]
	solution = sympy.solve(eqs, symbols)
	s = sum(solution[0][:3])
	return s

if __name__ == '__main__':
	main()

