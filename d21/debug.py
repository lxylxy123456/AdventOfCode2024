LOC_NUM = {
	'7': (0, 0),
	'8': (0, 1),
	'9': (0, 2),
	'4': (1, 0),
	'5': (1, 1),
	'6': (1, 2),
	'1': (2, 0),
	'2': (2, 1),
	'3': (2, 2),
	'0': (3, 1),
	'A': (3, 2),
}

LOC_DIR = {
	'^': (0, 1),
	'A': (0, 2),
	'<': (1, 0),
	'v': (1, 1),
	'>': (1, 2),
}

def simulate1(text, level):
	loc = {'n': LOC_NUM, 'd': LOC_DIR}[level]
	rev_loc = dict(map(lambda x: (x[1], x[0]), loc.items()))
	cx, cy = loc['A']
	ans = ''
	for i in text:
		if i == 'A':
			ans += rev_loc[(cx, cy)]
		elif i == '<':
			cy -= 1
		elif i == 'v':
			cx += 1
		elif i == '>':
			cy += 1
		elif i == '^':
			cx -= 1
		else:
			raise ValueError
		#print(i, cx, cy)
	assert rev_loc[(cx, cy)] == 'A'
	return ans

def simulate_levels1(text, levels):
	cur = text
	for level in levels:
		cur = simulate1(cur, level)
	return cur

_0 = '<vA<AA>^>AAvA<^A>AvA^Av<<A>^>AAvA^A<vA>^AA<A>Av<<A>A>^AAAvA<^A>A'
_1 = 'v<<AA>^A>A<AA>AvAA^A<vAAA>^A'
_2 = '<<^A^^A>>AvvvA'
_3 = '179A'
assert len(_0) == 64
assert simulate1(_0, 'd') == _1
assert simulate1(_1, 'd') == _2
assert simulate1(_2, 'n') == _3

r0 = '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'
r1 = '<Av<AA>>^A<AA>AvAA^A<vAAA>^A'
r2 = '^<<A^^A>>AvvvA'
r3 = '179A'
assert len(r0) == 68
assert simulate1(r0, 'd') == r1
assert simulate1(r1, 'd') == r2
assert simulate1(r2, 'n') == r3

for i in [
	'<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A',
	'<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A',
	'<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
	'<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A',
	'<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
]:
	print(simulate_levels1(i, 'ddn'))

