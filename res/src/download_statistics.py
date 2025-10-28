import requests
import os
from datetime import datetime, timedelta
import json



def write_downloads():
	print('gathering download counts from github api')
	rcount = 0
	downloads = 0
	plugins = []
	pcount = []
	if not os.path.isdir('res/dl_log/'):
		os.makedirs('res/dl_log/')
	now = datetime.now()
	date_time = now.strftime('%Y-%m-%d')
	with open('res/dl_log/' + date_time + '.txt', 'w') as target:
		target.writelines('# DOWNLOADS FOR EACH RELEASE:\n')
		# call api for release downloads, max 100 times if needed
		for i in range(1, 100):
			if username == '' or token == '':
				response = requests.get('https://api.github.com/repos/' + repo + '/releases?page=' + str(i) + '&per_page=100')
			else:
				response = requests.get('https://api.github.com/repos/' + repo + '/releases?page=' + str(i) + '&per_page=100', auth=(username, token))
			data = response.json()	
			if len(data) == 0:
				break
			# each data has max 100 releases
			for obj in data:
				rcount += 1 # number of releases
				rname = obj['tag_name']
				rdownload = obj['assets'][0]["download_count"] # number of downloads for each release 
				if rname == 'Latest':
					break
				if rname.split('-', 1)[1] in plugins:
					index = plugins.index(rname.split('-', 1)[1])
					icount = pcount[index]
					icount += rdownload
					pcount[index] = icount
				else:
					plugins.append(rname.split('-', 1)[1])
					pcount.append(rdownload)
				target.writelines(rname + ' | downloads: ' + str(rdownload) + '\n')
				downloads += rdownload
		target.writelines('\n\n')
		target.writelines('# NUMBER OF RELEASES: ' + str(rcount) + '\n')
		target.writelines('# TOTAL DOWNLOADS: ' + str(downloads) + '\n\n\n')
		target.writelines('# TOTAL DOWNLOAD NUMBER FOR EACH PLUGIN:\n')
		for each in plugins:
			index = plugins.index(each)
			plugins[index] = each + ' ' + str(pcount[index])
		plugins.sort()
		for each in plugins:
			index = plugins.index(each)
			target.writelines(each + '\n')
	# create missing dl_log file
	print('checking dl_log files for the last 7 days')
	now = datetime.now()
	logfiles = os.listdir('res/dl_log/')
	logfiles.sort()
	if len(logfiles) > 7:
		# get last 7 logfiles
		for i in range(0, len(logfiles) -7): # only the last 7 files
			logfiles.pop(0)
		print('>7')
	else:
		# create 7 logfiles, because missing
		for i in range(0, 7):
			date_time = now - timedelta(days=i)
			file_name = date_time.strftime('%Y-%m-%d.txt')
			if os.path.isfile('res/dl_log/' + file_name):
				print('	found [' + str(i+1) + '] ' + file_name)
				with open('res/dl_log/' + file_name, 'r') as source:
					last_content = source.readlines()
			else:
				with open('res/dl_log/' + file_name, 'w') as target:
					target.writelines(last_content)
				print('	created [' + str(i+1) + ']) ' + file_name)


def write_usercount():
	dates, newdates, newlist = [], [], []
	# reading github user statistics for last 14 days
	now = datetime.now()
	date_time = now.strftime("%Y-%m-%d" + 'T00:00:00Z')
	response = requests.get('https://api.github.com/repos/' + repo + '/traffic/views?per_page=100', auth=(username, token))
	data = response.json()
	print('getting live data from last 14 days:')
	try:
		timestamp = data['views'][0]["timestamp"]
		last_date = datetime.strptime(timestamp, '%Y-%m-%dT00:00:00Z')
	except:
		last_date = datetime.strptime(now, '%Y-%m-%dT00:00:00Z')
	for i in range(0, 15):
		try:
			timestamp = data['views'][i]["timestamp"]
			count = data['views'][i]["count"]
			uniques = data['views'][i]["uniques"]
			print('	' + timestamp + '|' + str(count) + '|' + str(uniques) + '	[' + str(i) + '] found in api data ')
			newdates.append(timestamp + '|' + str(count) + '|' + str(uniques))
		except:
			last_date = last_date - timedelta(days=1)	
			timestamp = last_date.strftime('%Y-%m-%dT00:00:00Z')
			count = 0
			uniques = 0
			print('	' + timestamp + '|' + str(count) + '|' + str(uniques) + '	[' + str(i) + '] not found in api data ')
			newdates.append(timestamp + '|' + str(count) + '|' + str(uniques))
	# comparing dates list with usercount.txt
	print('integrating to usercount.txt')
	if not os.path.isfile('res/usercount.txt'):
		# no file, write all 14 dates in
		with open('res/usercount.txt', 'w') as target:
			for each in newdates:
				target.writelines(each + '\n')
	else:
		# compare and replace matching dates
		newlist = []
		with open('res/usercount.txt', 'r') as source:
			olddates = source.readlines()
		for olddate in olddates:
			if olddate == '\n':
				continue
			found = False
			for newdate in newdates:
				newdatedate = newdate.split('|')[0] # get just the date
				if olddate.startswith(newdatedate):
					# compare which has bigger views value
					oldviews = olddate.split('|')[1]
					newviews = newdate.split('|')[1]
					if int(newviews) > int(oldviews):
						newlist.append(newdate)
						bigger = 'new'
					else:
						newlist.append(olddate.strip())
						bigger = 'old'
					found = True
					# remove newdate from newdates
					newdates.remove(newdate)
					if olddate.strip() == newdate:
						print('	' + newdate + '	no change, keeping it')
					else:
						if bigger == 'new':
							print('	' + newdate + '	replaces ' + olddate.strip() + ' | remaining new dates:' + str(len(newdates)))
						else:
							print('	' + newdate + '	has lowers views than ' + olddate.strip() + '(keeping old) | remaining new dates:' + str(len(newdates)))
					break
			if found == False:
				print('	' + olddate.strip() + '	no change, keeping it.')
				newlist.append(olddate.strip())
		print('	remaining new dates:' + str(len(newdates)))
		for newdate in newdates:
			if not newdate in newlist:
				newlist.append(newdate)
				print('	' + newdate + ' added')
		newlist.sort()
		with open('res/usercount.txt', 'w') as target:
			for each in newlist:
				target.writelines(each + '\n')

def run():
	global username, token, repo
	# for local testing
	if os.getcwd() == '/storage/emulated/0/Download/mgit/statistics/res/src': # check for local testing
		os.chdir('../../')
	# get variables
	with open('res/config.txt', 'r') as s:
		lines = s.readlines()
	for line in lines:
		if line.startswith('repo :'):
			repo = line[7:].strip()
	cur_repo = os.environ['CUR_REPO']
	username = cur_repo.split('/')[0]
	token =  os.environ['github_token']
	# test if token is there
	print('Token Check')
	print('	Token?: ', bool(token))
	print('	Lenght: ', len(token) if token else 0)
	# real statistics gathering
	write_downloads()
	write_usercount()


if __name__ == "__main__":
	run()
