import os, re, jinja2

t = jinja2.Template('''
# Advent of Code 2023

<https://adventofcode.com/2023>

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
 25   00:38:19   910      0   00:38:35   795      0
 24   00:15:28    84     17   02:43:26  1228      0
 23   00:16:28   439      0   00:49:53   199      0
 22   00:25:18   177      0   00:56:34   706      0
 21   00:09:10   646      0   01:16:59    90     11
 20   00:26:19   150      0   01:01:21   346      0
 19   00:12:03   173      0   00:31:12   143      0
 18   00:13:57   390      0   00:57:23  1068      0
 17   00:39:52  1010      0   00:43:50   768      0
 16   00:13:27   195      0   00:18:08   199      0
 15   00:05:04  1272      0   00:20:51   993      0
 14   00:08:47   881      0   00:24:42   320      0
 13   00:14:47   497      0   00:19:50   363      0
 12   00:08:55   128      0   00:29:31   283      0
 11   00:09:48   419      0   00:12:00   252      0
 10   00:15:02   253      0   00:32:08    69     32
  9   00:05:28   256      0   00:06:14   135      0
  8   00:06:25   867      0   00:15:52   370      0
  7   00:11:29   166      0   00:17:01   127      0
  6   00:04:28   360      0   00:05:39   168      0
  5   00:11:40   324      0   00:37:46   351      0
  4   00:08:56  2585      0   00:13:42   905      0
  3   00:11:20   398      0   00:13:40   170      0
  2   00:09:43  1175      0   00:13:05  1098      0
  1   00:01:59   193      0   00:10:58   454      0
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

