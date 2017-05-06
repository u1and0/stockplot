
# coding: utf-8

# タイトル
# Plotlyでぐりぐり動かせる為替チャートを作る(2)

# In[1]:

import sys
sys.path.append('../../bin/')


# # 下準備

# ## モジュールインポート
# 必要なモジュールをインポートします。

# In[2]:

# ----------General Module----------
import numpy as np
import pandas as pd
# ----------User Module----------
from randomwalk import randomwalk
import stockplot as sp


# In[3]:

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

# In[4]:

# Make sample data
np.random.seed(10)
df = randomwalk(60 * 60 * 24 * 90, freq='S', tick=0.01, start=pd.datetime(2017, 3, 20))    .resample('T').ohlc() + 115  # 90日分の1分足, 初期値が115


# ランダムな為替チャートを作成します。
# randomwalk関数で**2017/3/20からの1分足を90日分**作成します。

# ## インスタンス化

# In[5]:

# Convert DataFrame as StockPlot
fx = sp.StockPlot(df)


# StockPlotクラスでインスタンス化します。

# # ローソク足の描画

# `fig = sp.StockPlot(sdf)`でインスタンス化されたら時間足を変換します。
# 変換する際は`resample`メソッドを使います。

# In[6]:

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

# In[7]:

fx.append('close_25_sma')
fx.stock_dataframe.head()


# close_25_sma(25本足単純移動平均線)が追加されました。
# `append`メソッド単体をJupyter NotebookやIpython上で実行するとclose_25_smaの値が戻り値として表示されます。

# In[8]:

fx.plot(start_view='first', end_view='last')
fx.show('jupyter')


# ## 指標の削除

# 指標の削除には`pop`メソッドを使用します。

# In[9]:

fx.pop('close_25_sma')
fx.stock_dataframe.head()


# In[10]:

fx.append('boll')  # ボリンジャーバンド真ん中(close_20_smaと同じ)
fx.append('boll_ub')  # ボリンジャーバンド上
fx.append('boll_lb')  # ボリンジャーバンド下
fx.append('high_0~20_max')  # 20足前の移動最高値
fx.append('low_0~20_min')  # 20足前の移動最低値
fx.plot(start_view='first', end_view='last')
fx.show('jupyter')


# ## 初期化

# 追加した指標をすべて消すときは初期化を行います。
# 初期化は`clear`メソッドを使います。

# In[11]:

fx.clear()
fx.stock_dataframe.head()


# * データフレーム(`fx.stock_dataframe`)を初期化します。
# * 時間足は初期化しません。
# * プロットデータ(`fx._fig`)を初期化します。
# * インジケータ(`fx._indicators`)を初期化します。
# > hardオプションをTrueにすることで時間足も初期化できます。(ハードリセット)
# > fx.stock_dataframeも`_init_`時に戻ります。
# 
# ```python
# fx.clear(hard=True)
# ```
# 
# 
# ほとんど`__init__`メソッドと同じですが、
# 
# * データとしての引数が必要ないこと
# * デフォルトでは時間足を変更しないこと
# 
# > すなわち再度プロットするときに`resample`メソッドを使う必要がないこと
# 
# の点が`__init__`と異なります。

# In[12]:

fx.clear(hard=True)
fx.stock_dataframe.head()


# `fx.stock_dataframe`が元の1分足に戻りました。

# # 応用

# `stockstats`ではボリンジャーバンドで使う移動区間と$\sigma$がクラス変数
# 
# ```
# BOLL_PERIOD = 20
# BOLL_STD_TIMES = 2
# ```
# 
# として定義されています。
# ここで移動区間を20, $\sigma$を1に変更してみます。

# In[27]:

sp.ss.StockDataFrame.BOLL_PERIOD = 5  # ボリンジャーバンド移動区間の設定
sp.ss.StockDataFrame.BOLL_STD_TIMES = 1  # ボリンジャーバンドσの設定
boll = sp.StockPlot(df)
boll.resample('4H')
boll.append('boll')  # ボリンジャーバンド真ん中(close_5_smaと同じ)
boll.append('boll_ub', name='BOLL UB_sigma_1')  # ボリンジャーバンド上
boll.append('boll_lb', name='BOLL LB_sigma_1')  # ボリンジャーバンド下
boll.plot(start_view='first', end_view='last')
boll.show('jupyter')


# $\sigma_1$と$\sigma_2$は同時に描けないのが残念です。
# 
# `BOLL_PERIOD`, `BOLL_STD_TIMES`は`stockstats`のクラス変数なので、
# `stockplot.stockstats.BOLL_STD_TIMES = 2`とか再定義する必要があります。
# 
# しかし、`stockstats`が指標を追加するとき、`_get`メソッドを使うので、一度追加した指標が上書きされてしまいます。
# 
# グラフに描くだけであれば何とかすればできそうですが、今後の課題とします。

# `append`メソッドを使った段階では`self._indicators`に値が保持され、グラフには追加されません。
# `plot`メソッドを使う段階で`self._indicators`にある値をグラフにプロットします。

# ```python
#     def plot(self, start_view=None, end_view=None, periods_view=None, shift=None,
#              start_plot=None, end_plot=None, periods_plot=None,
#              showgrid=True, validate=False, **kwargs):
#              
#         # (中略)
#         
#         # ---------Append indicators----------
#         for indicator in self._indicators.keys():
#             self._append_graph(indicator, start_plot, end_plot)  # Re-append indicator in graph
#         # ---------Set "view"----------
#              
#         # (中略)
#         
#         return self._fig
#   
#   
#     def _append_graph(self, indicator, start, end):
#         graph_value = self._indicators[indicator].loc[start:end]
#         plotter = go.Scatter(x=graph_value.index, y=graph_value,
#                              name=indicator.upper().replace('_', ' '))  # グラフに追加する形式変換
#         self._fig['data'].append(plotter)       
# ```

# In[ ]:



