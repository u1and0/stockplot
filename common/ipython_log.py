# IPython log file

# Modules import
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plotly.tools import FigureFactory as FF
from plotly import tools
import plotly.offline as pyo
import plotly.graph_objs as go
pyo.init_notebook_mode(connected=True)

# Make sample data
from randomwalk import randomwalk
df = randomwalk(60 * 24 * 90, freq='T', tick=0.01, start=pd.datetime(2017, 3, 20)
                ).resample('B').ohlc() + 115  # 90日分の1分足を日足に直す

# Convert df as StockDataFrame
from stockstats import StockDataFrame
sdf = StockDataFrame(df.copy())

from stockplot import *
