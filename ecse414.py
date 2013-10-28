import subprocess
import datetime
from pymongo import MongoClient

def runtrace(host, collection):
    res = subprocess.check_output(['traceroute', host])
    result = {}
    result['hostname'] = host
    lines = res.splitlines()
    result['hostip'] = lines[0][lines[0].find('(')+1:lines[0].find(')')]
    result['hops'] = []

    for line in lines[1:]:
        line = line.split('  ')
        hop = {}
        hop['number'] = line[0]

        if line[1] == '* * *':
            hop['hopname'] = line[1]

        else:
            try:
                hop['hopname'] = line[1].split(' ')[0]
                hop['hopip'] = line[1][line[1].find('(')+1:line[1].find(')')]
                hop['probe1'] = line[2]
                hop['probe2'] = line[3]
                hop['probe3'] = line[4]
            except:
                hop['hopname'] = '* * *'

        result['hops'].append(hop)

    result['datetime'] = datetime.datetime.now().__str__()
    result['numhops'] = len(result['hops'])

    collection.insert(result)

if __name__ == '__main__':
    MONGO_URL = 'mongodb://alex:alexisgreat@paulo.mongohq.com:10055/ecse414'
    client = MongoClient(MONGO_URL)
    db = client.ecse414
    collection = db.traceroutes
    hosts = ['www.google.com', 'www.facebook.com', 'www.microsoft.com']
    for host in hosts:
        runtrace(host, collection)