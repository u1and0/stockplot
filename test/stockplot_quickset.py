# ----------General Module----------
import numpy as np
import pandas as pd
# ----------User Module----------
from randomwalk import randomwalk
import stockplot as sp
# ----------Plotly Module----------
import plotly.offline as pyo
pyo.init_notebook_mode(connected=True)

# Make sample data
np.random.seed(1)
# 90日分の1秒tickを1分足に直す
df = randomwalk(60 * 60 * 24 * 90, freq='S', tick=0.01, start=pd.datetime(2017, 3, 20)).resample('T').ohlc() + 115

# Convert StockDataFrame as StockPlot
fx = sp.StockPlot(df)

# Resample as Day OHLC
fx.resample('H')
