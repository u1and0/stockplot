
# coding: utf-8

# In[25]:

import sys
sys.path.append('../../bin/')


# # 下準備

# ## モジュールインポート
# 必要なモジュールをインポートします。

# In[26]:

# ----------General Module----------
import numpy as np
import pandas as pd
# ----------User Module----------
from randomwalk import randomwalk
import stockplot as sp


# In[27]:

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
#     * [Qiita - u1and0 / Plotlyでぐりぐり動かせる為替チャートを作る](http://qiita.com/u1and0/items/e2273bd8e03c670be45a)
#     * [Qiita - u1and0 / plotlyでキャンドルチャートプロット](http://qiita.com/u1and0/items/0ebcf097a1d61c636eb9)
# * random_walkについては[Qiita - u1and0 / pythonでローソク足(candle chart)の描画](http://qiita.com/u1and0/items/1d9afdb7216c3d2320ef)

# ## サンプルデータの作成

# In[28]:

# Make sample data
np.random.seed(10)
df = randomwalk(60 * 60 * 24 * 90, freq='S', tick=0.01, start=pd.datetime(2017, 3, 20))    .resample('T').ohlc() + 115  # 90日分の1分足, 初期値が115


# ランダムな為替チャートを作成します。
# randomwalk関数で**2017/3/20からの1分足を90日分**作成します。

# ## インスタンス化

# In[63]:

# Convert DataFrame as StockPlot
fx = sp.StockPlot(df)


# StockPlotクラスでインスタンス化します。

# # ローソク足の描画

# `fig = sp.StockPlot(sdf)`でインスタンス化されたら時間足を変換します。
# 変換する際は`resample`メソッドを使います。

# In[64]:

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

# In[65]:

fx.append('close_25_sma').head()


# In[66]:

fx.stock_dataframe.head()


# In[57]:

fx.plot(start_view='first', end_view='last')
fx.show('jupyter')


# ## 初期化

# 追加した指標をすべて消すときは初期化を行います。
# 初期化は`clear`メソッドを使います。

# In[43]:

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

# In[37]:

fx.clear(hard=True)
fx.stock_dataframe.head()


# In[ ]:



