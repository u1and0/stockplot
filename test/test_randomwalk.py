import sys
sys.path.append('../bin')
from randomwalk import randomwalk
import datetime
import pandas as pd

print(randomwalk(100))  # only periods
today = datetime.datetime.today()
print(randomwalk(periods=100, end=today, freq='4H'))  # periods, end
print(randomwalk(start=today, periods=100, freq='10S'))  # start, periods
after60min = (pd.Period(today, 'T') + 60).start_time
print(randomwalk(start=today, end=after60min, tick=0.01, freq='T'))  # start, end
print(randomwalk(periods=100, start=today, tick=0.1, freq='H', name='TEST'))
print(randomwalk(periods=1000, freq='H').resample('D').ohlc())  # resample ohlc
