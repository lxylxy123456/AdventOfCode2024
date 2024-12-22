import os, re, jinja2

t = jinja2.Template('''
# Advent of Code 2024

<https://adventofcode.com/2024>

## Files

| day | question | example | input | solution | Youtube | other |
|-----|----------|---------|-------|----------|---------|----------|
{%- for day in days %}
|{{ day.dir }}|{{ day.qs }}|{{ day.exs }}|{{ day.ins }}|{{ day.sols }}|{{ day.youtube }}|{{ day.others }}|
{%- endfor %}

## My time

```
{{ my_time }}
```

'''.lstrip('\n'))

dict_render = {
	'days': []
}

def file_link(href, name=None):
	if name is None:
		name = os.path.basename(href)
	return '[%s](%s)' % (name, href)

def get_youtube_link(d):
	line = open(os.path.join(d, 's.py')).read().split('\n')[0]
	matched = re.fullmatch(r'# Youtube: https://youtu\.be/(.{11})', line)
	if not matched:
		return ''
	link, = matched.groups()
	readme_content = ''.join([
		'Youtube Video:\n',
		'\n',
		'[![Youtube Video](http://img.youtube.com/vi/%s/0.jpg)]' % link,
		'(http://www.youtube.com/watch?v=%s)\n' % link,
	])
	readme_path = os.path.join(d, 'README.md')
	if os.path.exists(readme_path):
		assert open(readme_path).read() == readme_content
	else:
		open(readme_path, 'w').write(readme_content)
	return file_link('https://youtu.be/%s' % link, '`%s`' % link)

for i in range(1, 26):
	d = 'd%02d' % i
	if not os.path.exists(d):
		print('Does not exist:', repr(d))
		continue
	files = sorted(os.listdir(d))
	qs = []
	exs = []
	ins = []
	sols = []
	others = []
	youtube = get_youtube_link(d)
	for i in list(files):
		matched = re.fullmatch(r'ex(.*)\.txt', i)
		if matched:
			if i == 'ex.txt':
				exs.append(file_link(d + '/' + i))
			else:
				exs.append(file_link(d + '/' + i, matched.groups()[0]))
			files.remove(i)
			continue
		if i == 'in.txt':
			ins.append(file_link(d + '/' + i))
			files.remove(i)
			continue
		if i == 'q.txt':
			qs.append(file_link(d + '/' + i))
			files.remove(i)
			continue
		matched = re.fullmatch(r's(.*)\.py', i)
		if matched:
			if i == 's.py':
				sols.append(file_link(d + '/' + i))
			else:
				sols.append(file_link(d + '/' + i, matched.groups()[0]))
			files.remove(i)
			continue
		if i == 'README.md':
			#youtube = get_youtube_link(d)
			files.remove(i)
			continue
		if i in ['compute.sh']:
			files.remove(i)
			continue
		if 1:
			others.append(file_link(d + '/' + i))
	day = {
		'name': d,
		'dir': file_link(d),
		'qs': ', '.join(qs),
		'exs': ', '.join(exs),
		'ins': ', '.join(ins),
		'sols': ', '.join(sols),
		'others': ', '.join(others),
		'youtube': youtube,
	}
	dict_render['days'].append(day)

lines = open('time.txt').read().split('\n')[1:]
while lines and '-Part 1-' not in lines[0] and '-Part 2-' not in lines[0]:
	lines.pop(0)
while lines and lines[-1] == '':
	lines.pop()
dict_render['my_time'] = '\n'.join(lines)

print(t.render(**dict_render), file=open('README.md', 'w'))

