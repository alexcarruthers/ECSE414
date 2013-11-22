import matplotlib.dates
import matplotlib.pyplot as plt
import json
import datetime
import numpy as np

def rtt(hops):
	rtts = []
	for hop in reversed(hops):
		if hop['hopname'] is not "* * *":
			try:
				return float(hop['probe1'].split()[0])
			except:
				pass
			break
	return 0

datasets = ['alex_auckland','alex_br','alex_caltech','alex_coet','alex_engg','alex_uk','shaun_auckland','shaun_br','shaun_caltech','shaun_coet','shaun_engg','shaun_uk']

for dataset in datasets:
	print('opening ' + dataset)
	with open(dataset + '.json') as file:
		data = json.load(file)

	numchanges = {}
	times = {}
	changes = []
	
	
	previous = data['traces'][0]			
	for trace in data['traces'][1:]:
		tracetime = datetime.datetime.strptime(trace['datetime'], '%Y-%m-%d %H:%M:%S.%f').replace(minute=0, second=0, microsecond=0)
		if previous['numhops'] != trace['numhops']:
			try:
				numchanges[tracetime] += 1
			except KeyError:
				numchanges[tracetime] = 1
				times[tracetime] = []
			times[tracetime].append(rtt(trace['hops']))
		else:
			for (prevhop, trhop) in zip(previous['hops'], trace['hops']):
				if bool('hopip' in prevhop.keys()) != bool('hopip' in trhop.keys()):
					try:
						numchanges[tracetime] += 1
					except KeyError:
						numchanges[tracetime] = 1	
						times[tracetime] = []
					times[tracetime].append(rtt(trace['hops']))
					break
				try:
					if prevhop['hopip'] != trhop['hopip']:
						try:
							numchanges[tracetime] += 1
						except KeyError:
							numchanges[tracetime] = 1
							times[tracetime] = []
						times[tracetime].append(rtt(trace['hops']))
						break
				except KeyError:
					continue
		previous = trace

	x = []
	y = []
		
	for k,v in numchanges.iteritems():
		x.append(v)
		y.append(sum(times[k])/len(times[k]))
	
	plt.figure(dataset + ' all', figsize=(12,9))
	plt.title(dataset)
	plt.xlabel('Average RTT per hour')
	plt.ylabel('Route Changes per Hour')
	plt.ylim(0,14)
	plt.plot(y,x,'.')
	plt.savefig(dataset + ' changes', bbox_inches=0)
