# %load ipython_log
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
df = randomwalk(60 * 60 * 24 * 90, freq='S', tick=0.01, start=pd.datetime(2017, 3, 20)).resample('T').ohlc() + 115  # 90日分の1分足を日足に直す

# Convert StockDataFrame as StockPlot
fx = sp.StockPlot(df)

# # Add indicator
# for i in range(10, 17):
#     fx.append('close_{}_sma'.format(i))

# # Remove indicator
# for i in [13, 11]:
#     fx.remove('close_{}_sma'.format(i))

# # Pop indicator
# fx.pop()

# # Plot Candle chart

# fx.candle_plot(end='last', periods=50, freq='D')
# # 日足の表示。freqは省略可

# fx.candle_plot(end='last', periods=50, freq='15T')
# # 15分足の表示

# fx.candle_plot(end='last', periods=50, freq='5T')
# # 5分足の表示。5分足でも描画が重くならないのは、cutという引数が、グラフ化してくれるインスタンス変数self.sdfを300足で切り取ってくれるから。
# # **tailじゃなくてixかlocで抜き出すべし**

# fx.candle_plot(end='last', periods=50, freq='H')
# fx.candle_plot(end='last', periods=50, freq='H', cut=None)
# # 時間足の表示
# # cut=None にすれば300で切られずにすべて表示。

# fx.sdf
# fx.StockDataFrame
# # sdfがプロットされているデータ、StockDataFrameはinitされたときに格納されたデータフレーム。時間足変更のために、保存されている

# fx.candle_plot(end='last', periods=50, freq='H', fix=30)
# fx.candle_plot(end='last', periods=50, freq='H', fix=5)
# fx.candle_plot(end='last', periods=50, freq='H', fix=60)
# fx.candle_plot(start=pd.Timestamp('20170401'), end=pd.Timestamp('20170501'), freq='H')
# fx.candle_plot(start=pd.datetime(2017,4,1), end=pd.datetime(2017,5,1), freq='H')
# fx.candle_plot(start=pd.datetime(2017,4,1), end=pd.datetime(2017,5,1), freq='H')
# fx.candle_plot(start=pd.datetime(2017,4,1), end=pd.datetime(2017,5,1), freq='H', cut=False)
