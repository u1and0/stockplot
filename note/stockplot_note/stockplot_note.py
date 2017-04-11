
# coding: utf-8

# [仮タイトル]plotlyでキャンドルチャートプロット

# # 下準備

# ## モジュールインポート

# In[1]:

import sys, os
sys.path.append('../../common/')


# ## サンプルデータの作成

# In[2]:

np.random.seed(9)
from randomwalk import randomwalk
df = randomwalk(60 * 24 * 90, freq='T', tick=0.01, start=pd.datetime(2017, 3, 20)
                ).resample('B').ohlc() + 115  # 90日分の1分足を日足に直す


# ランダムウォークの作成。
# 詳しくは[pythonでローソク足(candle chart)の描画](http://qiita.com/u1and0/items/1d9afdb7216c3d2320ef)をご覧ください。

# ## pd.DataFrame型をStockDataFrame型に変換

# In[ ]:

from stockstats import StockDataFrame
sdf = StockDataFrame(df.copy())


# # StockPlotクラスの使用方法

# ## stockplot.pyのインポート

# In[ ]:

from stockplot import StockPlot


# In[ ]:

# StockPlotクラスのインスタンス化
x = StockPlot(sdf)


# In[ ]:

# キャンドルチャートのプロット
x.candle_plot()


# # 指標

# ## 指標の追加

# In[ ]:

# 終値25日移動平均線追加
x.add_indicator('close_25_sma')


# `add_indicator`関数の戻り値は`StockDataFrame`クラスで`get`メソッドを使った時と同じ結果が返ってきます。
# 
# 裏でplotly形式に直され、インスタンス変数self.figに追加されます。

# In[ ]:

# キャンドルチャートと追加された指標のプロット
x.candle_plot()


# 終値25日移動平均線が追加されました。

# In[ ]:

# 終値25日指数移動平均線の追加とプロット
x.add_indicator('close_25_ema')
x.candle_plot()


# 先ほど追加された終値25日移動平均線に加え、終値25日指数移動平均線が追加されました。

# ## 指標の削除

# In[ ]:

y = StockPlot(sdf)
# 10,11,12,13足移動平均線
for i in range(10, 14):
    y.add_indicator('close_{}_sma'.format(i))
y.candle_plot()


# In[ ]:

# 10, 12足移動平均線の削除
for i in (10, 12):
    y.remove_indicator('close_{}_sma'.format(i))
y.candle_plot()


# # ファイルへのエクスポート

# StockPlotクラスはPlotlyのhtmlエクスポートする`plotly.offline.iplot`(Jupyter Notebook形式)で図を吐き出します。
# つまり、ファイルへのエクスポートがされません。
# 
# ファイルとして吐き出したいときは以下のメソッドを使います。
# 
# * html形式: `plotly.offline.plot()`
# * png, svg, jpeg, webp形式: `plotly.offline.image`

# In[ ]:

pyo.plot(y.fig, filename='candle_y.html', validate=False)


# In[ ]:

pyo.plot(y.fig, image='png', image_filename='candle_y')


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

# In[ ]:

# 使い方
np.random.seed(2)
df = pd.DataFrame(np.random.randn(10,4), columns=['open', 'high', 'low', 'close'])
from stockstats import StockDataFrame
sdf = StockDataFrame(df)  # pandasデータフレームをStockDataFrameに入れてあげる
sdf


# 見た目に変化はありませんが金融指標を`stockstats`の文法に従って`get`メソッド、またはディクショナリの取得をすると、金融指標のカラムが追加されます。

# In[ ]:

sdf.get('close_5_sma'); sdf


# close_5_sma: 終値の5足移動平均線が追加されました。

# In[ ]:

sdf['close_5_sma']; sdf


# `sdf.get('close_5_sma')`と全く同じです。
# getの方がありえない指標を打ち込んだときエラーが発生しません。
# どちら良いかは用途次第でしょう。

# 詳しくは公式をご覧ください。
# 
# * [github - jealous/stockstats](https://github.com/jealous/stockstats)
# * [PyPI - stockstats](https://pypi.python.org/pypi/stockstats)

# ## stockplot

# これが今、紹介した私が作ったやつです。
# stockstatsを楽にplotするためのクラスStockPlotを作成しました。
# 
# プログラミンg府初心者故クラスの引継ぎとかよくわかんなくてこんな感じになりました。
# 
# できたら
# 
# ```python
# df = randomwalk(60 * 24 * 90, freq='T', tick=0.01, start=pd.datetime(2017, 3, 20)
#                 ).resample('B').ohlc() + 115  # 90日分の1分足を日足に直す
# sdf = StockDataFrame(df)
# x = StockPlot(sdf)
# x.candle_plot()
# ```

# stockplot.pyのソースコード

# In[52]:

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

    # なにがしたい

    * StockDataFrameにプロット能力を持たせたい。
    * プロット能力はStockDataFrameクラスにメソッドを付与してあげる。

    ```python
    df = randomwalk(60 * 24 * 90, freq='T', tick=0.01,
                    start=pd.datetime(2017, 3, 20)).resample('B').ohlc() + 115  # 90日分の1分足を日足に直す
    dfs = stockstats.StockDataFrame(df)
    dfs.add_indicator('hoge'): インジケーターの追加
    dfs.candle_plot(): キャンドルチャートとインジケータの表示
    dfs.remove_indicator('hoge'): インジケーターの削除
    ```

    # メソッド詳細
    * dfs.add_indicator('hoge')
        * dfs.get('hoge')を実行して、グラフに挿入するデータフレームを入手する
            > `indi = dfs.get('hoge')`
        * プロットするための形plotterに変換してやる
            > `plotter = go.Scatter(x=..., y=...) <- indiを使う`
        * plotterをStockPlotのattributeである`fig`に入れてやる
            > `fig['data'].append(plotter)`

    * dfs.candle_plot()
        * `fig = FF.create_candlestick... `でキャンドルチャートを取得できる
        * figに対してadd_indicator / remove_inidcatorで指標の追加 / 削除が行われる。

    * dfs.plot()
        * plt.show()に当たるのかな

        ```python
                self.fig['layout'].update(xaxis={'showgrid': True})  # figのレイアウト調整をして
                pyo.plot(self.fig, filename=filename, validate=False)  # plotlyでhtmlとしてプロットする
        ```

        別にdataframe的な操作は必要ないから、
        StockDataFrameのサブクラスになる必要はないので

        強いていうなら、StockDataFrameにfigという属性持たせて、
        plotlyとつなげたいから
        def __init()__をStockDataFrameにあてがってあげればいいのか
        StockDataFrame.__init__ = __init__

    # TODO
    * koma_ashi
    * subplot

    """

    def __init__(self, sdf):
        self.StockDataFrame = sdf
        self.fig = FF.create_candlestick(self.StockDataFrame.open,
                                         self.StockDataFrame.high,
                                         self.StockDataFrame.low,
                                         self.StockDataFrame.close,
                                         dates=self.StockDataFrame.index)

    def candle_plot(self, filebasename='candlestick_and_trace'):
        """StockDataFrameをキャンドルチャート化する
        引数: dfs: StockDataFrame
        戻り値: plotly plot"""
        self.fig['layout'].update(xaxis={'showgrid': True})
        ax = pyo.iplot(self.fig, filename=filebasename + '.html', validate=False)
        # pyo.plot(self.fig, image='png', image_filename=filebasename, validate=False)
        return ax

    def add_indicator(self, indicator):
        indi = self.StockDataFrame.get(indicator)
        plotter = go.Scatter(x=indi.index, y=indi,
                             name=indicator.upper().replace('_', ' '))  # グラフに追加する形式変換
        self.fig['data'].append(plotter)
        return indi

    def remove_indicator(self, indicator):
        indi = indicator.lower().replace(' ', '_')
        INDI = indicator.upper().replace('_', ' ')
        self.StockDataFrame.pop(indi)
        for dicc in self.fig['data']:
            if dicc['name'] == INDI:
                self.fig['data'].remove(dicc)
                return dicc

