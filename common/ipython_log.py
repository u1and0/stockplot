# IPython log file
# ----------General Module----------
import numpy as np
import pandas as pd
import stockstats as ss
# ----------User Module----------
from randomwalk import randomwalk
import stockplot as sp
# ----------Plotly Module----------
import plotly.offline as pyo
pyo.init_notebook_mode(connected=True)

# Make sample data
np.random.seed(1)
df = randomwalk(60 * 24 * 90, freq='T', tick=0.01, start=pd.datetime(2017, 3, 20)).resample('T').ohlc() + 115  # 90日分の1分足を日足に直す

# Convert DataFrame as StockDataFrame
sdf = ss.StockDataFrame(df.copy())

# Convert StockDataFrame as StockPlot
fig = sp.StockPlot(sdf.copy())

# # Add indicator
# for i in range(10, 17):
#     fig.append('close_{}_sma'.format(i))

# # Remove indicator
# for i in [13, 11]:
#     fig.remove('close_{}_sma'.format(i))

# # Pop indicator
# fig.pop()

# # Plot Candle chart
# fig.candle_plot(how='html')
# fig.candle_plot(how='html', freq='4h', periods=20)
