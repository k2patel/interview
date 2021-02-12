import os
import shlex
import pandas as pd
from datetime import datetime

filename = os.getcwd() + '/problem1/test_data/01-input'
loglines = []

types_dict = {'time': float, 'request': str}
test = pd.read_csv(filename, sep=" ", doublequote=True, index_col=None, header = None, usecols= [0,2], names = ['time', 'request'])

test['date'] = pd.to_datetime(test['time'], unit='s')

test = test.set_index(test['date'])

for hr in ("%02d" % x for x in range(23)):
    hr_start = test['date'][0].strftime('%Y-%m-%d')+' ' + hr + ':00:00.0'
    hr_end = test['date'][0].strftime('%Y-%m-%d')+' ' + hr + ':59:59'
    HOUR_start =  datetime.strptime(hr_start, '%Y-%m-%d %H:%M:%S.%f')
    HOUR_end =  datetime.strptime(hr_end, '%Y-%m-%d %H:%M:%S')
    printer = test.loc[HOUR_start : HOUR_end]
    try:
        fvalue = printer['request'].value_counts().idxmax()
        print(fvalue)
        fcal = printer['request'].value_counts().max()
        print(HOUR_start.isoformat(), fcal, fvalue)
    except ValueError:
        continue
    
