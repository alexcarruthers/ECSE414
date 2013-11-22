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

	changes = {}
	
	previous = data['traces'][0]			
	for trace in data['traces'][1:]:
		tracetime = datetime.datetime.strptime(trace['datetime'], '%Y-%m-%d %H:%M:%S.%f').replace(minute=0, second=0, microsecond=0)
		if previous['numhops'] != trace['numhops']:
			try:
				changes[tracetime] += 1
			except KeyError:
				changes[tracetime] = 1
		else:
			for (prevhop, trhop) in zip(previous['hops'], trace['hops']):
				if bool('hopip' in prevhop.keys()) != bool('hopip' in trhop.keys()):
					try:
						changes[tracetime] += 1
					except KeyError:
						changes[tracetime] = 1					
					break
				try:
					if prevhop['hopip'] != trhop['hopip']:
						try:
							changes[tracetime] += 1
						except KeyError:
							changes[tracetime] = 1					
						break
				except KeyError:
					continue
		previous = trace

	plt.figure(dataset + ' all', figsize=(12,9))
	plt.title(dataset)
	plt.xlabel('Day')
	plt.ylabel('Route Changes per Hour')
	plt.ylim(0,14)
	plt.plot_date(changes.keys(), changes.values(), '.')
	plt.savefig(dataset + ' changes', bbox_inches=0)
