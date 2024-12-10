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
      -------Part 1--------   -------Part 2--------
Day       Time  Rank  Score       Time  Rank  Score
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
	lines = open(os.path.join(d, 'README.md')).read().split('\n')
	links = set()
	assert len(lines) == 4
	assert lines[0] == 'Youtube Video:'
	assert lines[1] == ''
	matched = re.fullmatch(r'\[\!\[Youtube Video\]\(http://img.youtube.com/vi/'
						r'(.{11})/0\.jpg\)\]\(http://www\.youtube\.com/watch\?'
						r'v=(.{11})\)', lines[2])
	assert matched
	links.update(matched.groups())
	assert lines[3] == ''
	line = open(os.path.join(d, 's.py')).read().split('\n')[0]
	matched = re.fullmatch(r'# Youtube: https://youtu\.be/(.{11})', line)
	assert matched
	links.update(matched.groups())
	assert len(links) == 1
	link = next(iter(links))
	return file_link('https://youtu.be/%s' % link, '`%s`' % link)

for i in range(1, 26):
	d = 'd%02d' % i
	files = sorted(os.listdir(d))
	qs = []
	exs = []
	ins = []
	sols = []
	others = []
	youtube = ''
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
			youtube = get_youtube_link(d)
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

print(t.render(**dict_render), file=open('README.md', 'w'))

