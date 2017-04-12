
# coding: utf-8

# [仮タイトル]plotlyでキャンドルチャートプロット

# # 下準備

# ## サンプルデータの作成

# In[17]:

import sys, os
sys.path.append('../../common/')


# In[18]:

np.random.seed(9)
from randomwalk import randomwalk
df = randomwalk(60 * 24 * 90, freq='T', tick=0.01, start=pd.datetime(2017, 3, 20)
                ).resample('B').ohlc() + 115  # 90日分の1分足を日足に直す


# ランダムウォークの作成。
# 詳しくは[pythonでローソク足(candle chart)の描画](http://qiita.com/u1and0/items/1d9afdb7216c3d2320ef)をご覧ください。

# ## pd.DataFrame型をStockDataFrame型に変換

# In[19]:

from stockstats import StockDataFrame
sdf = StockDataFrame(df.copy())


# # StockPlotクラスの使用方法

# ## stockplot.pyのインポート

# In[20]:

from stockplot import StockPlot


# In[21]:

# StockPlotクラスのインスタンス化
x = StockPlot(sdf)


# In[22]:

# キャンドルチャートのプロット
x.candle_plot()


# キャンドルチャートが描かれました。

# # 指標

# ## 指標の追加

# 指標の追加はリスト型と同様に`append`メソッドを使います。

# In[23]:

# 終値25日移動平均線追加
x.append('close_25_sma')


# `add_indicator`関数の戻り値は`StockDataFrame`クラスで`get`メソッドを使った時と同じ結果が返ってきます。
# 
# 裏でplotly形式に直され、インスタンス変数self.figに追加されます。

# In[24]:

# キャンドルチャートと追加された指標のプロット
x.candle_plot()


# 終値25日移動平均線が追加されました。

# In[25]:

# 終値25日指数移動平均線の追加とプロット
x.append('close_25_ema')
x.candle_plot()


# 先ほど追加された終値25日移動平均線に加え、終値25日指数移動平均線が追加されました。

# ## 指標の削除

# 指標の削除はリストの削除と同様に'remove'メソッドを使います。
# 
# ここでは省略されていますが、`remove`戻り値は削除したStockDataFrameのカラムです。

# In[26]:

y = StockPlot(sdf)
# 10,11,12,13足移動平均線
for i in range(10, 14):
    y.append('close_{}_sma'.format(i))
y.candle_plot()


# 新たなインスタンスを作成し、10, 11, 12, 13足移動平均線を追加しました。

# In[27]:

# 10, 12足移動平均線の削除
for i in (10, 12):
    y.remove('close_{}_sma'.format(i))
y.candle_plot()


# 10足、12足移動平均線だけを指定して削除しました。

# # ファイルへのエクスポート

# StockPlotクラスはPlotlyのhtmlエクスポートする`plotly.offline.iplot`(Jupyter Notebook形式)で図を吐き出します。
# つまり、ファイルへのエクスポートがされません。
# 
# ファイルとして吐き出したいときは以下のメソッドを使います。
# 
# * html形式: `plotly.offline.plot(figure_or_data, filename=<拡張子htmlにしないとワーニング(勝手に拡張子つけられちゃう)>, )`
# * png, svg, jpeg, webp形式: `plotly.offline.plot(figure_or_data, image=<png|svg|jpeg|webp>, imagefilename=<拡張子抜きのファイル名>)`

# In[28]:

import plotly.offline as pyo
pyo.plot(y._fig, filename='candle_y.html', validate=False)  # 新しいタブを開いてhtml表示します


# In[29]:

pyo.plot(y._fig, image='png', image_filename='candle_y')
# 新しいtmpタブを開いて
# imageに指定した拡張子として
# デフォルトのダウンロードディレクトリに保存します


# # パッケージ紹介

# ## Plotly
# 
# グラフ描画はPlotlyに行わせます。
# 簡単なことだったら無料で使えます。
# 
# インストールは
# 
# `conda install plotly`
# 
# または
# 
# `pip install plotly`
# 
# 有名だと思うのでここでは言及しません。

# ## stockstats
# データ操作はstockstatsというパッケージを使います。
# 
# インストールは
# 
# `pip install stockstats`
# 
# `stockstats`は金融指標を簡単に取得できる改造pandas.DataFrameクラスです。

# In[30]:

# 使い方
np.random.seed(2)
df = pd.DataFrame(np.random.randn(10,4), columns=['open', 'high', 'low', 'close'])
from stockstats import StockDataFrame
sdf = StockDataFrame(df)  # pandasデータフレームをStockDataFrameに入れてあげる
sdf


# 見た目に変化はありませんが金融指標を`stockstats`の文法に従って`get`メソッド、またはディクショナリの取得をすると、金融指標のカラムが追加されます。

# In[31]:

sdf.get('close_5_sma'); sdf


# close_5_sma: 終値の5足移動平均線が追加されました。

# In[32]:

sdf['close_5_sma']; sdf


# `sdf.get('close_5_sma')`と全く同じです。
# getの方がありえない指標を打ち込んだときエラーが発生しません。
# どちら良いかは用途次第でしょう。

# 使用できる指標は以下の通り。

# * change (in percent)
# * delta
# * permutation (zero based)
# * log return
# * max in range
# * min in range
# * middle = (close + high + low) / 3
# * SMA: simple moving average
# * EMA: exponential moving average
# * MSTD: moving standard deviation
# * MVAR: moving variance
# * RSV: raw stochastic value
# * RSI: relative strength index
# * KDJ: Stochastic oscillator
# * Bolling: including upper band and lower band.
# * MACD: moving average convergence divergence. Including signal and histogram.
# * CR:
# * WR: Williams Overbought/Oversold index
# * CCI: Commodity Channel Index
# * TR: true range
# * ATR: average true range
# * line cross check, cross up or cross down.
# * DMA: Different of Moving Average (10, 50)
# * DMI: Directional Moving Index, including
# * +DI: Positive Directional Indicator
# * -DI: Negative Directional Indicator
# * ADX: Average Directional Movement Index
# * ADXR: Smoothed Moving Average of ADX
# * TRIX: Triple Exponential Mo
# ving Average
# * VR: Volatility Volume Ratio

# 詳しくは公式をご覧ください。
# 
# * [github - jealous/stockstats](https://github.com/jealous/stockstats)
# * [PyPI - stockstats](https://pypi.python.org/pypi/stockstats)

# ## stockplot

# 私が作ったやつです。
# stockstatsを楽にplotするためのクラスStockPlotを作成しました。

# stockplot.pyのソースコード

# In[31]:

import numpy as np
import pandas as pd
# ----------User Module----------
from randomwalk import randomwalk
import stockstats as ss
# ----------Plotly Module----------
from plotly.tools import FigureFactory as FF
import plotly.offline as pyo
import plotly.graph_objs as go
pyo.init_notebook_mode(connected=True)


class StockPlot:
    """StockDataFrameの可視化ツール
    # TODO
    * heikin_plot
    * pop
    * subplot
    """

    def __init__(self, sdf: ss.StockDataFrame):
        self.StockDataFrame = sdf
        self._fig = FF.create_candlestick(self.StockDataFrame.open,
                                         self.StockDataFrame.high,
                                         self.StockDataFrame.low,
                                         self.StockDataFrame.close,
                                         dates=self.StockDataFrame.index)

    def candle_plot(self, filebasename='candlestick_and_trace'):
        """StockDataFrameをキャンドルチャート化する
        引数: dfs: StockDataFrame
        戻り値: plotly plot"""
        self._fig['layout'].update(xaxis={'showgrid': True})
        ax = pyo.iplot(self._fig, filename=filebasename + '.html', validate=False)
        # pyo.plot(self._fig, image='png', image_filename=filebasename, validate=False)
        return ax

    def append(self, indicator):
        indi = self.StockDataFrame.get(indicator)
        plotter = go.Scatter(x=indi.index, y=indi,
                             name=indicator.upper().replace('_', ' '))  # グラフに追加する形式変換
        self._fig['data'].append(plotter)
        return indi

    def remove(self, indicator):
        indi = indicator.lower().replace(' ', '_')
        INDI = indicator.upper().replace('_', ' ')
        self.StockDataFrame.pop(indi)
        for dicc in self._fig['data']:
            if dicc['name'] == INDI:
                self._fig['data'].remove(dicc)
                return dicc

