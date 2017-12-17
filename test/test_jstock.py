import sys
sys.path.append('../bin')
from read_nikkei import get_jstock
import pandas as pd

print(get_jstock(9302))
start = pd.datetime(2009, 11, 4)
end = pd.datetime(2009, 12, 8)
print(get_jstock(9302, freq='W', start=start, end=end))
print(get_jstock(9302, start=start, periods=5))
print(get_jstock(9302, freq='M', start='first', end='last'))
print(get_jstock(9302, freq='D', end=pd.datetime.today().date(), periods=50))
start = pd.Period(pd.datetime.today().date(), 'D') - 100
print(get_jstock(9302, freq='D', start=start.start_time, periods=50))
try:
    print(get_jstock(9302, freq='D', periods=50))
except ValueError as v:
    raise ValueError('期待通りのエラー', v)
