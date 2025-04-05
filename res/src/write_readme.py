import os
import PIL
from PIL import Image, ImageDraw, ImageFont


def local_check():
	# for local testing
	if os.getcwd() == '/storage/emulated/0/Download/pytests/test/res/src':
		os.chdir('../../')


def create_image(countnumber, plugin):
	iFont = 'DejaVuSans.ttf'
	im = PIL.Image.open('pics/new.png')
	font = ImageFont.truetype(font=iFont, size=12)
	draw = ImageDraw.Draw(im, 'RGBA')
	draw.text((5, 2) , 'downloads: ' + countnumber, fill=(255,255,255), font=font)
	im = im.convert('RGB')
	im.save('pics/' + plugin + '.png')
	#print('created image: ' + countnumber + ' ' + plugin)


def findp(list, p):
	# search for the plugin return the number
	count = '0'
	for check in list:
		if check.startswith(p + ' '):
			count = check.split(' ')[1]
			break
	return count


def write_readme():
	logfiles = os.listdir('res/dl_log/')
	logfiles.sort()
	for i in range(0, len(logfiles) - 7): # only the last 7 files
		logfiles.pop(0)
	# get the relevant part of the sourcefiles
	relevant = ['', '', '', '', '', '', '', ]
	ignorelist = ['real.fluff', 'additional.command.buttons', 'devil-run.unhidden', 'unique.fix', 'pirate.warlords']
	for i in range(0,7):
		relevant[i] += logfiles[i] + '\n'
		with open('res/dl_log/' + logfiles[i], 'r') as sourcefile:
			all = sourcefile.readlines()
		started = False
		for line in all:
			if line.startswith('# TOTAL DOWNLOAD NUMBER FOR EACH PLUGIN'):
				started = True
				continue
			if started == True:
				stopped = False
				for ignore in ignorelist:
					if line.startswith(ignore + ' '):
						stopped = True
						break
				if stopped == True:
					continue
				relevant[i] += line
	rows1 = relevant[0].split('\n') # these are the plugin lists for all days
	rows2 = relevant[1].split('\n')
	rows3 = relevant[2].split('\n')
	rows4 = relevant[3].split('\n')
	rows5 = relevant[4].split('\n')
	rows6 = relevant[5].split('\n')
	rows7 = relevant[6].split('\n')
	# write the readme
	with open('README.md', 'w') as target:
		target.writelines('<h6>Plugin download count for https://github.com/zuckung/endless-sky-plugins</h6><br>\n<br>\n')
		# get a nested list, sorted by latest download anount
		rows7split = [[] for i in range(len(rows7) - 1)]
		first = True
		for row in rows7:
			index = rows7.index(row)
			if row == '':
				continue
			if first == True:
				first = False
				continue
			splitted = row.split(' ')
			rows7split[index-1].append(int(splitted[1]))
			rows7split[index-1].append(splitted[0])
		rows7split.sort(reverse=True)
		# first table, sorted by name
		# split the 7 variable contents to lists
		target.writelines('<h6>Plugin download count, sorted by name</h6><sub><sup><br>\n')
		first = True
		for row in rows7:
			if row == '':
					continue
			if first == True:
				# write the dates
				target.writelines('<table>\n')
				target.writelines('\t<tr>\n')
				target.writelines('\t\t<td></td>\n')
				target.writelines('\t\t<td>' + rows1[0].replace('.txt', '').replace('2024-', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows2[0].replace('.txt', '').replace('2024-', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows3[0].replace('.txt', '').replace('2024-', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows4[0].replace('.txt', '').replace('2024-', '')  + '</td>\n')
				target.writelines('\t\t<td>' + rows5[0].replace('.txt', '').replace('2024-', '')  + '</td>\n')
				target.writelines('\t\t<td>' + rows6[0].replace('.txt', '').replace('2024-', '')  + '</td>\n')
				target.writelines('\t\t<td>' + rows7[0].replace('.txt', '').replace('2024-', '')  + '</td>\n')
				target.writelines('\t\t<td>today +</td>\n')
				target.writelines('\t</tr>\n')
				first = False
			else:
				# write the numbers
				target.writelines('\t<tr>\n')
				target.writelines('\t\t<td>' + row.split(' ')[0] + '</td>\n')
				target.writelines('\t\t<td>' + findp(rows1, row.split(' ')[0]) + '</td>\n')
				target.writelines('\t\t<td>' + findp(rows2, row.split(' ')[0]) + '</td>\n')
				target.writelines('\t\t<td>' + findp(rows3, row.split(' ')[0]) + '</td>\n')
				target.writelines('\t\t<td>' + findp(rows4, row.split(' ')[0]) + '</td>\n')
				target.writelines('\t\t<td>' + findp(rows5, row.split(' ')[0]) + '</td>\n')
				target.writelines('\t\t<td>' + findp(rows6, row.split(' ')[0]) + '</td>\n')
				target.writelines('\t\t<td>' + findp(rows7, row.split(' ')[0]) + '</td>\n')
				create_image(findp(rows7, row.split(' ')[0]) ,row.split(' ')[0])
				difference = str(int(findp(rows7, row.split(' ')[0])) - int(findp(rows6, row.split(' ')[0])))
				if difference == '0':
					difference = ''
				else:
					difference = '+ ' + difference 
				target.writelines('\t\t<td>' + difference + '</td>\n')
				target.writelines('\t</tr>\n')
		target.writelines('</table>\n</sub></sup>\n')		
		# second table, sorted by latest download counts		
		# split the 7 variable contents to lists
		target.writelines('<h6>Plugin download count, sorted by download count</h6><sub><sup><br>\n')
		first = True
		index = 0
		for row in rows7split:
			if first == True:
				# write the dates
				target.writelines('<table>\n')
				target.writelines('\t<tr>\n')
				target.writelines('\t\t<td></td>\n')
				target.writelines('\t\t<td>' + rows1[0].replace('.txt', '').replace('2024-', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows2[0].replace('.txt', '').replace('2024-', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows3[0].replace('.txt', '').replace('2024-', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows4[0].replace('.txt', '').replace('2024-', '')  + '</td>\n')
				target.writelines('\t\t<td>' + rows5[0].replace('.txt', '').replace('2024-', '')  + '</td>\n')
				target.writelines('\t\t<td>' + rows6[0].replace('.txt', '').replace('2024-', '')  + '</td>\n')
				target.writelines('\t\t<td>' + rows7[0].replace('.txt', '').replace('2024-', '')  + '</td>\n')
				target.writelines('\t\t<td>today +</td>\n')
				target.writelines('\t</tr>\n')
				first = False
			else:
				# write the numbers
				target.writelines('\t<tr>\n')
				target.writelines('\t\t<td>' + rows7split[index][1] + '</td>\n')
				target.writelines('\t\t<td>' + findp(rows1, rows7split[index][1]) + '</td>\n')
				target.writelines('\t\t<td>' + findp(rows2, rows7split[index][1]) + '</td>\n')
				target.writelines('\t\t<td>' + findp(rows3, rows7split[index][1]) + '</td>\n')
				target.writelines('\t\t<td>' + findp(rows4, rows7split[index][1]) + '</td>\n')
				target.writelines('\t\t<td>' + findp(rows5, rows7split[index][1]) + '</td>\n')
				target.writelines('\t\t<td>' + findp(rows6, rows7split[index][1]) + '</td>\n')
				target.writelines('\t\t<td>' + findp(rows7, rows7split[index][1]) + '</td>\n')
				difference = str(int(findp(rows7, rows7split[index][1])) - int(findp(rows6,rows7split[index][1])))
				if difference == '0':
					difference = ''
				else:
					difference = '+ ' + difference 
				target.writelines('\t\t<td>' + difference + '</td>\n')
				target.writelines('\t</tr>\n')
				index += 1
		target.writelines('</table>\n</sub></sup>\n')
		

				
		 
		
local_check()
write_readme()
