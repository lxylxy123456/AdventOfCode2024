import argparse, math, sys, re, functools, operator, itertools, heapq
from collections import defaultdict, Counter, deque
from fractions import Fraction
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

class Hailstone:
	def __init__(self, **kwargs):
		for k, v in kwargs.items():
			self.__setattr__(k, v)
	@property
	def p(self):
		return (self.px, self.py, self.pz)
	@property
	def v(self):
		return (self.vx, self.vy, self.vz)

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

def line_intersect(p1, v1, p2, v2):
	p1x, p1y, p1z = p1
	v1x, v1y, v1z = v1
	p2x, p2y, p2z = p2
	v2x, v2y, v2z = v2
	# p1x + v1x * t1 = p2x + v2x * t2
	# p1y + v1y * t1 = p2y + v2y * t2
	# p1z + v1z * t1 = p2z + v2z * t2
	# solve([
	# 	p1x + v1x * t1 = p2x + v2x * t2,
	# 	p1y + v1y * t1 = p2y + v2y * t2
	# ], [t1, t2]);
	t1n = ((-p2x*v2y)+p1x*v2y+(p2y-p1y)*v2x)
	t1d = (v1y*v2x-v1x*v2y)
	t2n = ((-p2x*v1y)+p1x*v1y+(p2y-p1y)*v1x)
	t2d = (v1y*v2x-v1x*v2y)
	print(t1n, t1d, t2n, t2d)
	if t1d == 0 or t2d == 0:
		return False
	t1 = Fraction(t1n, t1d)
	t2 = Fraction(t2n, t2d)
	print(p1z + v1z * t1, p2z + v2z * t2)
	return p1z + v1z * t1 == p2z + v2z * t2

def part_2(lines):
	hs = read_input(lines)
	assert line_intersect(
		(0, 0, 0),
		(1, 1, 1),
		(2, 0, 0),
		(1, -1, -1),
	)

	for i in range(10):
		for j in range(10):
			p1x, p1y, p1z = vec_add(hs[0].p, vec_mul(i, hs[0].v))
			p2x, p2y, p2z = vec_add(hs[1].p, vec_mul(j, hs[1].v))
			p3x, p3y, p3z = hs[2].p
			v3x, v3y, v3z = hs[2].v
			# p1x + (p1x - p2x) * t1 = p3x + v3x * t3
			# p1y + (p1y - p2y) * t1 = p3y + v3y * t3
			# p1z + (p1z - p2z) * t1 = p3z + v3z * t3
			t1n = -((-p3x*v3y)+p1x*v3y+(p3y-p1y)*v3x)
			t1d = ((-p2x*v3y)+p1x*v3y+(p2y-p1y)*v3x)
			t3n = -(p1x*(p3y-p2y)+p2x*(p1y-p3y)+(p2y-p1y)*p3x)
			t3d = ((-p2x*v3y)+p1x*v3y+(p2y-p1y)*v3x)
			if t1d == 0 or t3d == 0:
				continue
			t1 = Fraction(t1n, t1d)
			t3 = Fraction(t3n, t3d)
			if p1z + (p1z - p2z) * t1 == p3z + v3z * t3:
				print('Found:', i, j)
				assert line_intersect(hs[0].p, vec_add(hs[1].p, vec_mul(-1, hs[0].p)), hs[2].p, hs[2].v)
			else:
				assert not line_intersect(hs[0].p, vec_add(hs[1].p, vec_mul(-1, hs[0].p)), hs[2].p, hs[2].v)
	s = 0
	for i in lines:
		i
	return s

if __name__ == '__main__':
	main()

