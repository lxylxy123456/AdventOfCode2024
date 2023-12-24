def solve_2(h1, h2, h3):
	var = []
	print(h1.p.x)
	eqs = [
		lambda r_px, r_py, r_pz, r_vx, r_vy, r_vz, t_1, t_2, t_3: ((r_px + r_vx * t_1) - (h1.p.x + h1.v.x * t_1)),
		lambda r_px, r_py, r_pz, r_vx, r_vy, r_vz, t_1, t_2, t_3: ((r_py + r_vy * t_1) - (h1.p.y + h1.v.y * t_1)),
		lambda r_px, r_py, r_pz, r_vx, r_vy, r_vz, t_1, t_2, t_3: ((r_pz + r_vz * t_1) - (h1.p.z + h1.v.z * t_1)),
		lambda r_px, r_py, r_pz, r_vx, r_vy, r_vz, t_1, t_2, t_3: ((r_px + r_vx * t_2) - (h2.p.x + h1.v.x * t_2)),
		lambda r_px, r_py, r_pz, r_vx, r_vy, r_vz, t_1, t_2, t_3: ((r_py + r_vy * t_2) - (h2.p.y + h1.v.y * t_2)),
		lambda r_px, r_py, r_pz, r_vx, r_vy, r_vz, t_1, t_2, t_3: ((r_pz + r_vz * t_2) - (h2.p.z + h1.v.z * t_2)),
		lambda r_px, r_py, r_pz, r_vx, r_vy, r_vz, t_1, t_2, t_3: ((r_px + r_vx * t_3) - (h3.p.x + h1.v.x * t_3)),
		lambda r_px, r_py, r_pz, r_vx, r_vy, r_vz, t_1, t_2, t_3: ((r_py + r_vy * t_3) - (h3.p.y + h1.v.y * t_3)),
		lambda r_px, r_py, r_pz, r_vx, r_vy, r_vz, t_1, t_2, t_3: ((r_pz + r_vz * t_3) - (h3.p.z + h1.v.z * t_3)),
	]
	eval_eqs = lambda y: list(map(lambda x: x(*y), eqs))
	calc_score = lambda diffs: sum(map(abs, diffs))
	def apply_delta(v, i, d):
		v2 = v.copy()
		v2[i] += d
		return v2
	vals = [0] * 9
	while True:
		#print('vals', vals)
		cur_diffs = eval_eqs(vals)
		# Find derivatives
		derivatives = []
		for i in range(9):
			new_score = eval_eqs(apply_delta(vals, i, 1))
			derivatives.append(list(map(operator.sub, new_score, cur_diffs)))
		cur_score = calc_score(cur_diffs)
		print(float(cur_score))
		#print(float(cur_score), list(map(float, cur_diffs)))
		#print(*derivatives, sep='\n')
		old_vals = vals
		for i in random.sample(range(9), 9):
			if vals != old_vals:
				break
			if not any(derivatives[i]):
				continue
			c, d = random.choice(list(filter(lambda x: x[1],
											zip(cur_diffs, derivatives[i]))))
			best_score = cur_score
			best_delta = 0
			delta = c / (4 * d)#Fraction(c, d * 4)
			while True:
				score = calc_score(eval_eqs(apply_delta(vals, i, delta)))
				if score < best_score:
					best_score = score
					best_delta = delta
				else:
					break
				delta *= 1.1#Fraction(11, 10)
			vals[i] -= best_delta
		print(old_vals == vals, end='\t')
#		if old_vals == vals:
#			vals[random.randrange(9)] += random.randint(-10, 11)

	#eqs = [
	#	lambda r_px, r_vx,
	#]

def part_2(lines):
	hs = read_input(lines)
	s = solve_2(hs[0], hs[1], hs[2])
	return s

################################################################################

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

