import pandas as pd
import numpy as np
import sys
sys.path.append('../common/')
from set_span import *
n = 10
# indexes = [pd.date_range(periods=n, start=pd.datetime.today()),
#            pd.date_range(periods=n, end=pd.datetime.today()),
#            pd.date_range(start=pd.datetime(2017, 1, 1), end=pd.datetime.today())]
index = pd.date_range(pd.datetime(2017, 1, 1), pd.datetime(2018, 1, 1))
df = pd.DataFrame(np.random.randn(len(index), 4), index=index)
print(set_span(df, start=pd.datetime(2017, 2, 1), end=pd.datetime(2017, 5, 1), freq='H'))
print(set_span(df, periods=n, end=pd.datetime(2017, 5, 1), freq='H'))
print(set_span(df, start=pd.datetime(2017, 2, 1), periods=n, freq='H'))
