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
        self.add_line = []  # self.indicator()

    # ----------DATA MAKE----------
    def sma(self, window, columns='close'):
        """Simple Moving Average
        windowの足の分だけ移動平均
        dfに格納する
        column名はSMA{移動した足}

        引数:
            window: 移動足
            columns: 平均を適用する足{open, high, low, close}どれか
        戻り値: smaを格納したdf"""
        colname = 'sma%d' % window
        self.df[colname] = self.df[columns].rolling(window).mean()
        plotter = pyg.Scatter(x=self.df.index, y=self.df[colname],
                              name='SMA%d' % window, line=pyg.Line())
        self.add_line.append(plotter)
        return self.df

    def ema(self, span, columns='close'):
        """Exponential Moving Average
        spanの足の分だけ移動平均
        dfに格納する
        column名はEMA{移動した足}

        引数:
            span: 移動足
            columns: 平均を適用する足{open, high, low, close}どれか
        戻り値: emaを格納したdf"""
        colname = 'ema%d' % span
        self.df[colname] = self.df[columns].ewm(span).mean()
        plotter = pyg.Scatter(x=self.df.index, y=self.df[colname],
                              name='EMA%d' % span, line=pyg.Line())
        self.add_line.append(plotter)
        return self.df

    def bollinger(self, window, columns='close', snum=2):
        """Bollinger Bands
        windowの足の分だけ移動平均
        dfに格納する
        column名はEMA{移動した足}

        引数:
            window: 移動足
            columns: 平均を適用する足{open, high, low, close}どれか
        戻り値: bolを格納したdf

        a = [50, 1, 66]
        r = np.mean(a)

        In [47]: r
        Out[47]: 39.0

        In [48]: a-r
        Out[48]: array([ 11., -38.,  27.])

        In [49]: (a-r)**2
        Out[49]: array([  121.,  1444.,   729.])

        In [50]: np.sum((a-r)**2)
        Out[50]: 2294.0

        In [51]: np.sqrt(np.sum((a-r)**2)/(len(a)-1))
        Out[51]: 33.867388443752198 <==corrected sample standard deviation

        In [52]: np.std(a, ddof=1)
        Out[52]: 33.867388443752198"""

        # name define
        colname = 'sma%d'% window
        m1, p1 = '-s1_%d' % window, '+s1_%d' % window
        # m2, p2 = '-$\sigma$_2 %d' % window, '+$\sigma$_2 %d' % window,
        # m3, p3 = '-$\sigma$_3 %d' % window, '+$\sigma$_3 %d' % window,

        # moving corrected sample standard deviation
        sma = self.df[columns].rolling(window).mean()
        s = self.df[columns].rolling(window).std()

        # add self df
        self.df[colname] = sma
        self.df[m1] = sma - s
        self.df[p1] = sma + s
        plotter = [pyg.Scatter(x=self.df.index, y=self.df[colname], name=colname, line=pyg.Line()),
                   pyg.Scatter(x=self.df.index, y=self.df[p1], name=p1, line=pyg.Line()),
                   pyg.Scatter(x=self.df.index, y=self.df[m1], name=m1, line=pyg.Line())]
        self.add_line.extend(plotter)
        return self.df

    # ---------PLOT----------
    def plot(self, filename='candlestick_and_trace.html'):
        fig = FF.create_candlestick(self.df.open, self.df.high,
                                    self.df.low, self.df.close, dates=self.df.index)
        fig['data'].extend(self.add_line)
        fig['layout'].update(xaxis={'showgrid': True})
        pyo.plot(fig, filename=filename, validate=False)


if __name__ == '__main__':
    np.random.seed(1)
    df = randomwalk(60 * 24 * 90, freq='T', tick=0.01,
                    start=pd.datetime(2017, 3, 20)).resample('B').ohlc() + 115
    x = base(df)  # ohlcをbaseに渡す
    x.bollinger(20)
    # x.sma(5)
    # x.sma(25)
    # x.ema(5)
    # x.ema(25)
    print(x.df.head(5))
    x.plot()
