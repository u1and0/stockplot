
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
from datetime import datetime
from randomwalk import *
from plotly.tools import FigureFactory as FF
import plotly.offline as pyo
import plotly.graph_objs as pyg
pyo.init_notebook_mode(connected=True)


class base:
    """candlec chartとその指標を描くクラス
    入力: ohlcデータフレーム
    出力: plrtolyファイル(htmlファイル)"""

    def __init__(self, df):
        self.df = df
        self.add_line = []
        # self.dt = dt
        self.fig = self.fig()

    # ----------DATA MAKE----------

    # resampleは中でやったほうがいいのか外でやったほうがいいのか
    # def resamp(self, ashi):
    #     return df.ix[:, :4].resample(ashi).agg({'open':'first',
    #                                          'high':'max', 'low':'min', 'close':'last'}).dropna()

    def sma(self, window, columns='close'):
        # adding = pyg.Scatter(x=self.df.index, y=ro, name='SMA5', line=pyg.Line(color='r'))
        # self.add_line.extend(list(adding))
        self.df['sma%d'% window] = self.df[columns].rolling(window).mean()
        return self.df

    # ---------PLOT----------
    def fig(self):
        return FF.create_candlestick(self.df.open, self.df.high,
                                     self.df.low, self.df.close, dates=self.df.index)
    def indicator(self):
        add_line = [pyg.Scatter(x=self.df.index, y=self.df.ix[:, 4:].value, name='SMA', line=pyg.Line(color='r'))]
        self.fig['data'].extend(add_line)

    def plot(self, filename='candlestick_and_trace.html'):
        self.indicator()
        self.fig['layout'].update(xaxis={'showgrid': True})
        pyo.iplot(self.fig, filename=filename, validate=False)

if __name__ == '__main__':
    np.random.seed(1)
    df = randomwalk(60 * 24 * 90, freq='T', tick=0.01,
                    start=pd.datetime(2017, 3, 20)).resample('B').ohlc() + 115
    x = base(df)  # ohlcをbaseに渡す
    k = x.sma(5)
    print(k.head(5))
    x.plot()


# In[5]:

np.array(df.ix[:, 4:])


# In[6]:

df.close.rolling(25).mean()


# In[ ]:



