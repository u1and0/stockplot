# ----------General Module----------
import numpy as np
import pandas as pd
# ----------User Module----------
import sys
sys.path.append('./bin/')
from randomwalk import randomwalk
import stockplot as sp
# ----------Plotly Module----------
import plotly.offline as pyo
pyo.init_notebook_mode(connected=True)

# Make sample data
np.random.seed(1)
df = randomwalk(60 * 60 * 24 * 90, freq='S', tick=0.01, start=pd.datetime(2017, 3, 20)).resample('T').ohlc() + 115  # 90日分の1分足を日足に直す

# Convert StockDataFrame as StockPlot
fx = sp.StockPlot(df)

# Resample as Day
fx.resample('D')

# Add indicator
# fx.append('close_10_sma')
# fx.plot()
for i in range(25, 76, 25):
    fx.append('close_{}_sma'.format(i))
    fx.plot()

print(fx._indicators)
# Remove indicator
# for i in [13, 11]:
#     fx.remove('close_{}_sma'.format(i))

# # Pop indicator
# fx.pop()
