import requests
import os
from datetime import datetime
import json



def set_var():
	global username
	global token
	global repo
	token = os.environ['PAT'] # was github_token
	token2 = os.environ['github_token']
	username = os.enviro ['USER']
	#username = os.environ['CUR_REPO'].split('/')[0]
	print(username)
	repo = 'zuckung/endless-sky-plugins'

def get_date():
	now = datetime.now()
	date_time = now.strftime('%Y-%m-%d')
	return date_time

def analyze_write():
	rcount = 0
	downloads = 0
	plugins = []
	pcount = []
	if not os.path.isdir('res/dl_log/'):
		os.makedirs('res/dl_log/')
	with open('res/dl_log/' + get_date() + '.txt', 'w') as target:
		target.writelines('# DOWNLOADS FOR EACH RELEASE:\n')
		for i in range(1, 100): # call api for felease downloads, max 100 times if needed
			if username == '' or token == '':
				response = requests.get('https://api.github.com/repos/' + repo + '/releases?page=' + str(i) + '&per_page=100')
			else:
				print('user/token found')
				response = requests.get('https://api.github.com/repos/' + repo + '/releases?page=' + str(i) + '&per_page=100', auth=(username, token2))
			data = response.json()	
			if len(data) == 0:
				break
			for obj in data: # each data has max 100 releases
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


def get_usercount():
	dates, newdates, newlist = [], [], []
	now = datetime.now()
	date_time = now.strftime("%Y-%m-%d" + 'T00:00:00Z')
	response = requests.get('https://api.github.com/repos/' + repo + '/traffic/views?per_page=100', auth=(username, token))
	data = response.json()
	print(data)
	print('getting live data from last 2 days:')
	for i in range(13, len(data['views'])):
		timestamp = data['views'][i]["timestamp"]
		count = data['views'][i]["count"]
		uniques = data['views'][i]["uniques"]
		print('\t' + timestamp + '|' + str(count) + '|' + str(uniques))
		dates.append(timestamp + '|' + str(count) + '|' + str(uniques))
	print('comparing with saved:')
	with open('res/usercount.txt', 'r') as source:
		olddates = source.readlines()
	for each in dates:
		if each + '\n' in olddates:
			print ('\tduplicate', each)
		else:
			newdates.append(each + '\n')
	for each in newdates:
		print('\tchanged', each.strip())
	if len(newdates) == 0:
		print('\tno changed data')
	print('adding changed data to text:')
	if len(newdates) > 0:
		for olddate in olddates:
			found = False
			for newdate in newdates:
				newdatedate = newdate.split('|')[0]
				if olddate.startswith(newdatedate):
					newlist.append(newdate)
					found = True
					break
			if found == False:
				newlist.append(olddate)
		if not newdates[len(newdates)-1].split('|')[0] in olddates:
			newlist.append(newdates[len(newdates)-1])
	else:
		print('\tnothing to add')
	with open('res/usercount.txt', 'w') as target:
		for each in newlist:
			target.writelines(each)

def run():
	set_var()
	analyze_write()
	get_usercount()


if __name__ == "__main__":
	run()
		 
		



