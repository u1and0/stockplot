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

        # self.dt = dt
        self.fig = self.fig()
        # self.add_line =

    # def to_unix_time(self):
    #     """datetimeをunix秒に変換
    #     引数: datetime(複数指定可能)
    #     戻り値: unix秒に直されたリスト"""
    #     epoch =  datetime.utcfromtimestamp(0)
    #     return [(i - epoch).total_seconds() * 1000 for i in self.dt]

    def fig(self):
        return FF.create_candlestick(self.df.open, self.df.high,
                                     self.df.low, self.df.close, dates=self.df.index)

    def sma(self, window, columns='close'):
        return self.data[columns].rolling(window).mean()

    def plot(self, figname='candlestick_and_trace'):
        pyo.plot(self.fig, filename=figname, validate=False)


if __name__ == '__main__':
    np.random.seed(1)
    df = randomwalk(60 * 24 * 90, freq='T', tick=0.01,
                    start=pd.datetime(2017, 3, 20)).resample('B').ohlc() + 115
    base(df).plot()
