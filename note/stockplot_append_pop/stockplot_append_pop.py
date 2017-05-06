
# coding: utf-8

# タイトル
# Plotlyでぐりぐり動かせる為替チャートを作る(2)

# In[2]:

import sys
sys.path.append('../../bin/')


# # 下準備

# ## モジュールインポート
# 必要なモジュールをインポートします。

# In[3]:

# ----------General Module----------
import numpy as np
import pandas as pd
# ----------User Module----------
from randomwalk import randomwalk
import stockplot as sp


# In[4]:

# ----------Hide General Module----------
import stockstats
import plotly


# * General Module, Hide General Moduleは一般に配布されているパッケージなので、condaやpipといったパッケージ管理ソフトなどで追加してください。
#     * General ModuleはこのJupyter Notebook内で使います。
#     * Hide General Moduleは`stockplot`内で使用します。
# >```sh
# conda install plotly
# pip install stockstats
# ```
# * User Moduleのstockplotについては過去記事も併せてご覧ください。今回は**指標の追加・削除ができるようになりました。**
#     * [Qiita - u1and0 / Plotlyでぐりぐり動かせる為替チャートを作る(1)](http://qiita.com/u1and0/items/e2273bd8e03c670be45a)
#     * [Qiita - u1and0 / plotlyでキャンドルチャートプロット](http://qiita.com/u1and0/items/0ebcf097a1d61c636eb9)
# * random_walkについては[Qiita - u1and0 / pythonでローソク足(candle chart)の描画](http://qiita.com/u1and0/items/1d9afdb7216c3d2320ef)

# ## サンプルデータの作成

# In[5]:

# Make sample data
np.random.seed(10)
df = randomwalk(60 * 60 * 24 * 90, freq='S', tick=0.01, start=pd.datetime(2017, 3, 20))    .resample('T').ohlc() + 115  # 90日分の1分足, 初期値が115


# ランダムな為替チャートを作成します。
# randomwalk関数で**2017/3/20からの1分足を90日分**作成します。

# ## インスタンス化

# In[6]:

# Convert DataFrame as StockPlot
fx = sp.StockPlot(df)


# StockPlotクラスでインスタンス化します。

# # ローソク足の描画

# `fig = sp.StockPlot(sdf)`でインスタンス化されたら時間足を変換します。
# 変換する際は`resample`メソッドを使います。

# In[39]:

fx.resample('4H').head()


# In[40]:

fx.plot(start_view='first', end_view='last')
fx.show('png', filebasename='png1')


# ![png1](stockplot_append_pop_files/png1.png)

# 時間足の設定が済んだらプロットしてみます。
# 
# ここまでが[前回記事](http://qiita.com/u1and0/items/e2273bd8e03c670be45a)の復習です。
# 
# ---

# # 指標の操作

# ## 指標の追加

# 指標をプロットしてみます。
# 最もポピュラーな単純移動平均(Simple Moving Average)をプロットします。
# 追加するには`append`メソッドを使います。

# In[40]:

fx.append('close_25_sma')
fx.stock_dataframe.head()


# In[34]:

fx.plot(start_view='first', end_view='last')
fx.show('jupyter')


# close_25_sma(25本足単純移動平均線)が追加されました。
# なお、`append`メソッド単体をJupyter NotebookやIpython上で実行するとclose_25_smaの値が戻り値として表示されます。

# 追加された指標は時間足を変えても、その時間足に合わせて値を変更してくれます。

# In[41]:

fx.resample('15T')
fx.plot(start_view='first', end_view='last')
fx.show('jupyter')


# `resample`メソッドで15分足に変えた後、`append`メソッドを使わなくとも`close_25_sma`が追加されたままです。
# 
# これは`append`メソッドを実行した際ではなく、`plot`メソッドを実行した際にグラフに指標を追加するようにしたためです。
# 
# `append`メソッドが行うのは`self._indicators`に値を格納するだけです。

# ```python
# # ========self._indicatorに指標を蓄える==========
#     def append(self, indicator):
#         indicator_value = self.stock_dataframe[indicator]
#         self._indicators[indicator] = indicator_value  # self._indicatorsに辞書形式で
#         return indicator_value
# ```

# ```python
#     def plot(self, (略)):
#         # (中略)
#         # =======plotメソッド実行時にself._indicatorに蓄えられている指標を_append_graphに渡す==========
#         # ---------Append indicators----------
#         for indicator in self._indicators.keys():
#             self._append_graph(indicator, start_plot, end_plot)  # Re-append indicator in graph
#         # (中略)
#         return self._fig
# 
#     # =======self._indicatorに蓄えられている指標をself._figのデータ部分に追加する==========
#     def _append_graph(self, indicator, start, end):
#         graph_value = self._indicators[indicator].loc[start:end]
#         plotter = go.Scatter(x=graph_value.index, y=graph_value,
#                              name=indicator.upper().replace('_', ' '))  # グラフに追加する形式変換
#         self._fig['data'].append(plotter)
# ```

# ## 指標の削除

# 指標の削除には`pop`メソッドを使用します。

# In[42]:

fx.pop('close_25_sma')
fx.stock_dataframe.head()


# close_25_smaが削除されました。

# 単純移動平均以外の指標も描いてみます。

# In[43]:

fx.append('close_20_ema')  # 終値の指数移動平均線
fx.append('boll')  # ボリンジャーバンド真ん中(close_20_smaと同じ)
fx.append('boll_ub')  # ボリンジャーバンド上
fx.append('boll_lb')  # ボリンジャーバンド下
fx.append('high_0~20_max')  # 20足前の移動最高値
fx.append('low_0~20_min')  # 20足前の移動最安値
fx.plot(start_view='first', end_view='last')
fx.show('jupyter')


#  * 20本足ボリンジャーバンド
#  * 20本足移動最高値
#  * 20本足最安値
#  
#  がプロットされました。

# 追加した指標名がわからなくなったらインスタンス変数からアクセスできます。

# In[12]:

fx._indicators.keys()


# `append`メソッドを使ったときの引数がkey、戻り値がvalueとして、`_indicators`にディクショナリ形式で保存されます。
# そのため、`keys`メソッドで追加した指標名を呼び出すことができます。
# > `fx.stock_dataframe.columns`でも表示できますが、推奨できません。
# > `stockstats.StockDataFrame`は指標の生成時に補助的なカラムも発生させます。
# > そのため、補助指標(グラフにプロットされていないデータ)も混在していて、どれがプロットされているのか見分けづらいためです。

# In[45]:

fx.stock_dataframe.columns


# `fx.stock_dataframe.columns`による指標の表示は、追加していない指標名も表示されます。

# ごちゃごちゃしてきたので`high_20_max`, `low_20_min`を削除します。

# In[28]:

fx.pop('high_0~20_max')
fx.pop('low_0~20_min')
fx.plot(start_view='first', end_view='last')
fx.show('jupyter')


# `high_20_max`, `low_20_min`だけがグラフから削除されました。

# `pop`メソッドは以下の手順で進みます。
# 
# 1. `self._indicator`の中からindicatorで指定された値を削除します。
# 2. `self.stock_dataframe`から`open, high, low, close`だけ抜き出します。
# 3. `self._indicators`に残っている指標を再度プロットします。

# ```python
#     def pop(self, indicator):
#         popper = self._indicators.pop(indicator)  # (1)
#         self.stock_dataframe = reset_dataframe(self.stock_dataframe)  # (2)
#         for reindicator in self._indicators.keys():
#             self.stock_dataframe.get(reindicator)  # (3)
#         return popper
# ```

# `self.stock_dataframe`に入っている指標は、追加した指標によっては補助的に作られたカラムなどが混在します。
# そのため、「ある指標によって作られたカラムだけ」を特定し、`self.stock_dataframe`から削除するのが困難です。
# よって、一度`self.stock_dataframe`を`resample`がかかった状態まで戻し(2)、再度指標を追加しています(3)。
# 
# (3)は`append`メソッドとほとんど同じことですが、`self._indicators`に追加しません。
# (1)の段階で`self._indicators`からは余計な指標を取り除いていないため、`self._indicators`に再度追加する必要がないからです。

# ## 初期化

# 追加した指標をすべて消すときは初期化を行います。
# 初期化は`clear`メソッドを使います。

# In[50]:

fx.clear()
fx.stock_dataframe.head()


# In[51]:

fx.plot(start_view='first', end_view='last')
fx.show('jupyter')


# * データフレーム(`fx.stock_dataframe`)を初期化します。
# * プロットデータ(`fx._fig`)を初期化します。
# * インジケータ(`fx._indicators`)を初期化します。
# * **時間足は初期化しません。**
# > hardオプションをTrueにする(`fx.clear(hard=True)`として実行する)ことで時間足も初期化できます(ハードリセット)。
# > `self.stock_dataframe`は`None`に戻ります。
# > ハードリセットをかけた後に再度プロットしたいときは`resample`メソッドから実行してください。

# ```python
#     def clear(self, hard=False):
#         self._fig = None  # <-- plotly.graph_objs
#         self._indicators = {}
#         if hard:
#             self.stock_dataframe = None
#             self.freq = None  # 足の時間幅
#         else:
#             self.stock_dataframe = reset_dataframe(self.stock_dataframe)
# ```

# `clear`メソッドはほとんど`__init__`メソッドと同じですが、
# 
# * データとしての引数が必要ないこと
# * デフォルトでは時間足を変更しないこと
# 
# > すなわち再度プロットするときに`resample`メソッドを使う必要がないこと
# 
# の点が`__init__`と異なります。

# # 応用

# `stockstats`ではボリンジャーバンドで使う移動区間と$\sigma$がクラス変数として定義されています。
# 
# ```
# BOLL_PERIOD = 20
# BOLL_STD_TIMES = 2
# ```
# 
# ここで移動区間を5, $\sigma$を1に変更してみます。

# In[15]:

sp.ss.StockDataFrame.BOLL_PERIOD = 5  # ボリンジャーバンド移動区間の設定
sp.ss.StockDataFrame.BOLL_STD_TIMES = 1  # ボリンジャーバンドσの設定
boll = sp.StockPlot(df)
boll.resample('4H')
boll.append('boll')  # ボリンジャーバンド真ん中(close_5_smaと同じ)
boll.append('boll_ub')  # ボリンジャーバンド上
boll.append('boll_lb')  # ボリンジャーバンド下
boll.plot(start_view='first', end_view='last')
boll.show('jupyter')


# $\sigma_1$と$\sigma_2$は同時に描けないのが残念です。
# 
# `BOLL_PERIOD`, `BOLL_STD_TIMES`は`stockstats`のクラス変数なので、
# `stockplot.stockstats.BOLL_STD_TIMES = 2`のようにして再定義する必要があります。
# 
# しかし、`stockstats`が指標を追加するとき、`_get`メソッドを使うので、一度追加した指標が上書きされてしまいます。
# 
# グラフに描くだけであれば何とかすればできそうですが、今後の課題とします。
