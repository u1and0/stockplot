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
        column名はSMA{移動した足}

        引数:
            span: 移動足
            columns: 平均を適用する足{open, high, low, close}どれか
        戻り値: smaを格納したdf"""
        colname = 'ema%d' % span
        self.df[colname] = self.df[columns].ewm(span).mean()
        plotter = pyg.Scatter(x=self.df.index, y=self.df[colname],
                              name='EMA%d' % span, line=pyg.Line())
        self.add_line.append(plotter)
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
    x.sma(5)
    x.sma(25)
    x.ema(5)
    x.ema(25)
    print(x.df.head(5))
    x.plot()
