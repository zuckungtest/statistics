import os
import PIL
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta



def create_image(countnumber, plugin):
	im = PIL.Image.open('pics/' + counterbg + '.png')
	font = ImageFont.truetype(font=iFont, size=60)
	draw = ImageDraw.Draw(im, 'RGBA')
	draw.text((20, 15) , 'downloads:', fill=(255,255,255), font=font)
	draw.text((380, 15) ,  countnumber, fill=(255,255,255), font=font)
	im = im.convert('RGBA')
	im.save('pics/' + plugin + '.png')


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
		target.writelines('<h6>Plugin download count for https://github.com/' + repo + '</h6><br>\n<br>\n')
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
		totaldownloads = 0
		totaldifference = 0
		for row in rows7:
			if row == '':
					continue
			if first == True:
				# write the dates
				target.writelines('<table>\n')
				target.writelines('\t<tr>\n')
				target.writelines('\t\t<td></td>\n')
				target.writelines('\t\t<td>' + rows1[0].replace('.txt', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows2[0].replace('.txt', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows3[0].replace('.txt', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows4[0].replace('.txt', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows5[0].replace('.txt', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows6[0].replace('.txt', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows7[0].replace('.txt', '') + '</td>\n')
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
				totaldownloads += int(findp(rows7, row.split(' ')[0]))
				totaldifference += int(difference)
				if difference == '0':
					difference = ''
				else:
					difference = '+ ' + difference 
				target.writelines('\t\t<td>' + difference + '</td>\n')
				target.writelines('\t</tr>\n')
		create_image(str(totaldownloads), 'total')
		target.writelines('\t<tr>\n\t\t<td></td>\n\t\t<td></td>\n\t\t<td></td>\n\t\t<td></td>\n\t\t<td></td>\n\t\t<td></td>\n\t\t<td></td>\n')
		target.writelines('\t\t<td>' + str(totaldownloads) + '</td>\n')
		target.writelines('\t\t<td>' + str(totaldifference) + '</td>\n\t</tr>\n')
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
				target.writelines('\t\t<td>' + rows1[0].replace('.txt', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows2[0].replace('.txt', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows3[0].replace('.txt', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows4[0].replace('.txt', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows5[0].replace('.txt', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows6[0].replace('.txt', '') + '</td>\n')
				target.writelines('\t\t<td>' + rows7[0].replace('.txt', '') + '</td>\n')
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
		target.writelines('\t<tr>\n\t\t<td></td>\n\t\t<td></td>\n\t\t<td></td>\n\t\t<td></td>\n\t\t<td></td>\n\t\t<td></td>\n\t\t<td></td>\n')
		target.writelines('\t\t<td>' + str(totaldownloads) + '</td>\n')
		target.writelines('\t\t<td>' + str(totaldifference) + '</td>\n\t</tr>\n')
		target.writelines('</table>\n</sub></sup>\n')

		
def write_users():
	def parse(line):
		date = line.split('|')[0]
		views = line.split('|')[1]
		uniques = line.split('|')[2].strip()
		return date, views, uniques
	with open('res/usercount.txt', 'r') as source:
		userdata = source.readlines()
		# 2025-10-18T00:00:00Z|0|0
	# sort for seven days
	print('CREATE TABLE FOR SEVEN DAYS')
	sevendays, row1, row2, row3 = [], [], [], []
	for i in range(len(userdata)-1, len(userdata)-10, -1):
		sevendays.append(userdata[i].strip())
	for line in sevendays:
		date, views, uniques = parse(line)
		row1.append(date.replace('T00:00:00Z', ''))
		row2.append(views)
		row3.append(uniques)
		print('\t', date, views, uniques)
	row1.append(' ')
	row2.append('page views')
	row3.append('unique visitors')
	row1.reverse()
	row2.reverse()
	row3.reverse()
	# calculate stats
	allviews, alluniques, highviews, highuniques = 0, 0, 0, 0
	firstread = False
	for line in userdata:
		date, views, uniques = parse(line)
		if firstread == False:
			firstdate = date.replace('T00:00:00Z', '')
			firstread = True
		allviews += int(views)
		alluniques += int(uniques)
		if int(views) > highviews:
			highviews = int(views)
		if int(uniques) > highuniques:
			highuniques = int(uniques)
	div = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d') - datetime.strptime(firstdate, '%Y-%m-%d')
	div = int(div.days)
	print(firstdate, allviews, alluniques, highviews, highuniques)
	# write table
	with open('README.md', 'a') as target:
		target.writelines('<h6>Other statistics</h6><sub><sup><br>\n')
		target.writelines('<table>\n')
		target.writelines('\t<tr>\n')
		for each in row1:
			target.writelines('\t\t<td>' + each + '</td>\n')
		target.writelines('\t</tr>\n')
		target.writelines('\t<tr>\n')
		for each in row2:
			target.writelines('\t\t<td>' + each + '</td>\n')
		target.writelines('\t</tr>\n')
		target.writelines('\t<tr>\n')
		for each in row3:
			target.writelines('\t\t<td>' + each + '</td>\n')
		target.writelines('\t</tr>\n')
		target.writelines('</table>\n')
		# write stats
		target.writelines('<br>\n')
		target.writelines('<table>\n')
		target.writelines('\t<tr>\n')
		target.writelines('\t\t<td>statistics start</td>\n')
		target.writelines('\t\t<td>all page views</td>\n')
		target.writelines('\t\t<td>all unique visitors</td>\n')
		target.writelines('\t\t<td>highest page view</td>\n')
		target.writelines('\t\t<td>highest unique visitors</td>\n')
		target.writelines('\t</tr>\n')
		target.writelines('\t<tr>\n')
		target.writelines('\t\t<td>' + firstdate + '</td>\n')
		target.writelines('\t\t<td>' + str(allviews) + '</td>\n')
		target.writelines('\t\t<td>' + str(alluniques) + '</td>\n')
		target.writelines('\t\t<td>' + str(highviews) + '</td>\n')
		target.writelines('\t\t<td>' + str(highuniques) + '</td>\n')
		target.writelines('\t</tr>\n')
		target.writelines('\t<tr>\n')
		target.writelines('\t\t<td>days since start</td>\n')
		target.writelines('\t\t<td>average daily page views</td>\n')
		target.writelines('\t\t<td>average daily visitors</td>\n')
		target.writelines('\t\t<td></td>\n')
		target.writelines('\t\t<td></td>\n')
		target.writelines('\t</tr>\n')
		target.writelines('\t<tr>\n')
		target.writelines('\t\t<td>' + str(div) + '</td>\n')
		target.writelines('\t\t<td>' + str('%.2f' % (allviews/div)) + '</td>\n')
		target.writelines('\t\t<td>' + str('%.2f' % (alluniques/div)) + '</td>\n')
		target.writelines('\t\t<td></td>\n')
		target.writelines('\t\t<td></td>\n')
		target.writelines('\t</tr>\n')
		target.writelines('</table>\n</sub></sup>\n')
				
		 
def run():
	global iFont, repo, counterbg, ignorelist
	iFont = 'DejaVuSans.ttf'
	ignorelist = ['pirate.warlords', 'unique.fix', 'real.fluff', 'devil-run.unhidden', 'free.worlds.5.years.later',
				  'planet.pluto', 'additional.command.buttons', 'avgi.licenses', 'navy.licenses', 'landing.images.android']
	if os.getcwd() == '/storage/emulated/0/Download/mgit/statistics/res/src': # check for local android testing
		os.chdir('../../')
		iFont = '/system/fonts/Roboto-Regular.ttf' # android font
	with open('res/config.txt', 'r') as s:
		lines = s.readlines()
	for line in lines:
		if line.startswith('repo :'):
			repo = line[7:].strip()
		elif line.startswith('counterbg : '):
			counterbg = line[12:].strip()
	write_readme()
	write_users()


if __name__ == "__main__":
	run()		
