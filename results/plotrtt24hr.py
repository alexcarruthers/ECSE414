import matplotlib.dates
import matplotlib.pyplot as plt
import json
import datetime
import numpy as np

datasets = ['alex_auckland','alex_br','alex_caltech','alex_coet','alex_engg','alex_uk','shaun_auckland','shaun_br','shaun_caltech','shaun_coet','shaun_engg','shaun_uk']
for dataset in datasets:
        print('opening ' + dataset)
        with open(dataset + '.json') as file:
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

        plt.figure(dataset + ' all', figsize=(12,9))
        plt.title(dataset + ' - all data')
        plt.xlabel('Time of Day')
        plt.ylabel('RTT (ms)')
        plt.plot_date(time, rtt, '.')
        plt.savefig(dataset + ' all', bbox_inches=0)
        
        plt.figure(dataset + ' no outliers', figsize=(12,9))

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
        plt.title(dataset + ' - outliers removed')
        plt.xlabel('Time of Day')
        plt.ylabel('RTT (ms)')
        plt.plot_date(time, rttPrune, '.')
        plt.savefig(dataset + ' no outliers', bbox_inches=0)
#plt.show()