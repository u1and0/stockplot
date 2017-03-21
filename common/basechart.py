import numpy as np
import pandas as pd
from datetime import datetime
from randomwalk import *
from plotly.tools import FigureFactory as FF
import plotly.offline as pyo
import plotly.graph_objs as go
pyo.init_notebook_mode(connected=True)


class base:
    """candlec chartとその指標を描くクラス
    入力: ohlcデータフレーム
    出力: plrtolyファイル(htmlファイル)"""

    def __init__(self, df):
        self.df = df
        self.add_line = []  # indicatorプロットの入れ子
        self.bollinger_boolen = False  # ボリンジャーバンドのSMA一回目はplotする

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
        colname = 'SMA%d' % window
        self.df[colname] = self.df[columns].rolling(window).mean()
        plotter = go.Scatter(x=self.df.index, y=self.df[colname],
                             name=colname)
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
        colname = 'EMA%d' % span
        self.df[colname] = self.df[columns].ewm(span).mean()
        plotter = go.Scatter(x=self.df.index, y=self.df[colname],
                             name=colname)
        self.add_line.append(plotter)
        return self.df

    def bollinger(self, window, snum=2, columns='close'):
        """Bollinger Bands
        windowの足の分だけ移動平均
        dfに格納する
        column名はBOL{移動した足}

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
        colname = 'SMA%d' % window
        m1, p1 = '-SIG%d' % snum, '+SIG%d' % snum

        # moving corrected sample standard deviation
        sma = self.df[columns].rolling(window).mean()
        s = self.df[columns].rolling(window).std() * snum

        # add self df
        if not self.bollinger_boolen:  # 一度このfunctionによってsmaをdfに加えてしてたら、次は加えない
            self.df[colname] = sma
        self.df[m1] = sma - s
        self.df[p1] = sma + s

        # plot
        plotter = [
            go.Scatter(x=self.df.index, y=self.df[p1], name=p1,
                       line=dict(color='rgba(0,0,255,255)')),
            go.Scatter(x=self.df.index, y=self.df[m1], name=m1,
                       line=dict(color='rgba(0,0,255,255)'))]
        if not self.bollinger_boolen:  # 一度このfunctionによってsmaをplotしてたら、次はplotしない
            plotter.append(go.Scatter(x=self.df.index, y=self.df[
                           colname], name=colname,
                line=dict(color='rgba(0,0,255,100)', dash='dash')))
            self.bollinger_boolen = True
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
    x.bollinger(20, 1)
    x.sma(5)
    x.sma(25)
    x.ema(5)
    x.ema(25)
    print(x.df.tail(5))
    x.plot()
