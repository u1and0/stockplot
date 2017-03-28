# IPython log file

import stockstats as ss
from randomwalk import randomwalk
df = randomwalk(10000, freq='T').resample('H').ohcl(); df
df = randomwalk(10000, freq='T').resample('H').ohlc(); df
# random OHLC made END
get_ipython().system('less candle2.py')
import base_chart as B
import base_chart as B
x = B.base(df)
x.plot()
import base_chart as B
x = B.base(df)
x.plot()
get_ipython().magic('pinfo B.pyo.plot')
get_ipython().magic('pinfo B.pyo.iplot')
import base_chart as B
x = B.base(df)
x.plot()
get_ipython().magic('pinfo ss')
dfs = ss.StockDataFrame(df)
dfs.get('sma_5')
ss.StockDataFrame._Ge
get_ipython().magic('pinfo ss.StockDataFrame._get_sma')
get_ipython().magic('pinfo2 ss.StockDataFrame._get_sma')
dfs.get('close_5_sma')
dfs
get_ipython().magic('logstart')
get_ipython().magic('pwd ')
get_ipython().magic('gd base_chart.py')
get_ipython().magic('logstop')
