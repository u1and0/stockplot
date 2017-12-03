import sys
sys.path.append('../bin')
from read_nikkei import drange
import pandas as pd

print(drange(9302, freq='D'))
print(drange(9302, freq='M', all=True))
print(drange(9302, freq='D', end=pd.datetime.today().date(), periods=50))
start = pd.Period(pd.datetime.today().date(), 'D')-100
print(drange(9302, freq='D', start=start.start_time, periods=50))
