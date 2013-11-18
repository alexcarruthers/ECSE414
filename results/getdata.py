import matplotlib.dates
import matplotlib.pyplot as plt
import json
import datetime
import numpy as np
with open('alex_auckland.json') as file:
	data = json.load(file)

rtt = []
time = []
fuckups = 0
for trace in data['traces']:
	for hop in reversed(trace['hops']):
		if hop['hopname'] is not "* * *":
			try:
				rtt.append(float(hop['probe1'].split()[0]))
			except:
				fuckups+=1
				break
			t = datetime.datetime.strptime(trace['datetime'], '%Y-%m-%d %H:%M:%S.%f').time()
			time.append(datetime.datetime.combine(datetime.datetime.today(), t))
			break

times = matplotlib.dates.date2num(time)
plt.plot_date(time,rtt)
plt.show()

print(len(rtt))
print(len(time))
print(fuckups)
			
