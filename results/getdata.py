import matplotlib.dates
import matplotlib.pyplot as plt
import json
import datetime
import numpy as np

with open('alex_caltech.json') as file:
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


plt.plot_date(time, rtt, '.')
plt.figure("Figure2")

deletions = []


std = 2.0*np.std(rtt)
md = np.median(rtt)
for i in range(0, len(rtt)-1):
    if abs(rtt[i] - md) >= std:
        deletions.append(i)

for i in reversed(range(0, len(deletions) - 1)):
    del(rtt[deletions[i]])
    del(time[deletions[i]])

rttPrune = np.array(rtt)

times = matplotlib.dates.date2num(time)
plt.plot_date(time, rttPrune, '.')
plt.show()

print(len(rtt))
print(len(time))
print(fuckups)

