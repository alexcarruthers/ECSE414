import matplotlib.dates
import matplotlib.pyplot as plt
import json
import datetime
import numpy as np

def ave(hops):
	rtts = []
	for hop in reversed(hops):
		if hop['hopname'] is not "* * *":
			try:
				rtts.append(float(hop['probe1'].split()[0]))
			except:
				fuckups+=1
			break
	return sum(v)/len(v)

datasets = ['alex_auckland','alex_br','alex_caltech','alex_coet','alex_engg','alex_uk','shaun_auckland','shaun_br','shaun_caltech','shaun_coet','shaun_engg','shaun_uk']
for dataset in datasets:
	print('opening ' + dataset)
	with open(dataset + '.json') as file:
		data = json.load(file)

	rtt = []
	time = {}
	changes = []
	
	previous = data['traces'][0]			
	for trace in data['traces'][1:]:
		tracetime = datetime.datetime.strptime(trace['datetime'], '%Y-%m-%d %H:%M:%S.%f').replace(minute=0, second=0, microsecond=0)
		if previous['numhops'] != trace['numhops']:
			#changes.append(1)
			try:
				time[tracetime] += 1
			except KeyError:
				time[tracetime] = 1
		else:
			for (prevhop, trhop) in zip(previous['hops'], trace['hops']):
				if bool('hopip' in prevhop.keys()) != bool('hopip' in trhop.keys()):
					try:
						time[tracetime] += 1
					except KeyError:
						time[tracetime] = 1					
					break
				try:
					if prevhop['hopip'] != trhop['hopip']:
						#changes.append(1)
						try:
							time[tracetime] += 1
						except KeyError:
							time[tracetime] = 1					
						break
				except KeyError:
					continue
			#changes.append(0)
			#time[datetime.datetime.strptime(trace['datetime'], '%Y-%m-%d %H:%M:%S.%f').replace(minute=0, second=0, microsecond=0)] += 1
		previous = trace

	plt.figure(dataset + ' all', figsize=(16,12))
	plt.title(dataset)
	plt.xlabel('Day')
	plt.ylabel('Route Changes per Hour')
	plt.ylim(0,14)
	plt.plot_date(time.keys(), ave, '.')
	plt.savefig(dataset + ' changes', bbox_inches=0)
	#plt.figure(dataset + ' no outliers', figsize=(16,12))

	deletions = []


	# std = 2.0*np.std(rtt)
	# md = np.median(rtt)
	# for i in range(0, len(rtt)-1):
		# if abs(rtt[i] - md) >= std:
			# deletions.append(i)

	# for i in reversed(range(0, len(deletions) - 1)):
		# del(rtt[deletions[i]])
		# del(time[deletions[i]])

	# rttPrune = np.array(rtt)

	# times = matplotlib.dates.date2num(time)
	# plt.title(dataset + ' - outliers removed')
	# plt.xlabel('Day')
	# plt.ylabel('RTT (ms)')
	# plt.plot_date(time, rttPrune, '.')
	# plt.savefig(dataset + ' no outliers', bbox_inches=0)
#plt.show()

