import numpy as np
import pandas as pd
from randomwalk import *
from plotly.tools import FigureFactory as FF
import plotly.offline as pyo
import plotly.graph_objs as go
import stockstats as ss
pyo.init_notebook_mode(connected=True)

# class plot(object):
#     """StockDataFrame plotter"""
#     def __init__(self, df):
#         # super(plot, self).__init__()
#         self.df = df
#     def


__add_line__ = []


def candle_plot(dfs, filename='candlestick_and_trace.html'):
    """StockDataFrameをキャンドルチャート化する
    引数: dfs: StockDataFrame
    戻り値: plotly plot"""
    fig = FF.create_candlestick(dfs.open, dfs.high,
                                dfs.low, dfs.close, dates=dfs.index)
    fig['data'].extend(__add_line__)
    fig['layout'].update(xaxis={'showgrid': True})
    pyo.plot(fig, filename=filename, validate=False)


def sma(dfs, window, ohlc='close'):
    name = '%s_%s_sma' % (ohlc, window)  # indicator name
    sma = dfs.get(name)  # indicator
    plotter = go.Scatter(x=sma.index, y=sma,
                         name=name.upper().replace('_', ' '))  # グラフに追加する形式変換
    __add_line__.append(plotter)  # グラフに追加
    return sma


def ema(dfs, window, ohlc='close'):
    return dfs.get('%s_%s_ema' % (ohlc, window))


def rsi(dfs, window):
    return dfs.get('rsi_%s' % window)


def add_indicator(dfs, indicator):
    return dfs.get(indicator)


ss.StockDataFrame.candle_plot = candle_plot
ss.StockDataFrame.sma = sma
ss.StockDataFrame.add_indicator = add_indicator


if __name__ == '__main__':
    # Make sample data
    np.random.seed(1)
    df = randomwalk(60 * 24 * 90, freq='T', tick=0.01,
                    start=pd.datetime(2017, 3, 20)).resample('B').ohlc() + 115  # 90日分の1分足を日足に直す

    # Convert DataFrame as StockDataFrame
    dfs = ss.StockDataFrame(df)

    # Add indicator
    dfs.sma(5, 'open')

    # Plot Candle chart
    dfs.candle_plot()
