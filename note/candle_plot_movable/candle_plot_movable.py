
# coding: utf-8

# In[1]:

import sys
sys.path.append('../../common/')


# # 使い方

# ## 下準備

# ### モジュールインポート

# 必要なモジュールをインポートします。

# In[31]:

# ----------General Module----------
import numpy as np
import pandas as pd
import stockstats as ss
# ----------User Module----------
from randomwalk import randomwalk
import stockplot as sp


# * General Moduleは一般に配布されているパッケージなのでcondaやpipといったパッケージ管理ソフトでインストールしてください。
# * User Moduleのstockplotについては[Qiita - u1and0 / plotlyでキャンドルチャートプロット](http://qiita.com/u1and0/items/0ebcf097a1d61c636eb9)
# * random_walkについては[Qiita - u1and0 / pythonでローソク足(candle chart)の描画](http://qiita.com/u1and0/items/1d9afdb7216c3d2320ef)

# ### サンプルデータの作成

# In[ ]:

# Make sample data
np.random.seed(1)
df = randomwalk(60 * 60 * 24 * 90, freq='S', tick=0.01, start=pd.datetime(2017, 3, 20)).resample('T').ohlc() + 115  # 90日分の1分足


# ランダムな為替チャートを作成します。
# randomwalk関数で"2017/3/20からの1分足を90日分作成します。

# ### インスタンス化

# In[42]:

# Convert DataFrame as StockDataFrame
sdf = ss.StockDataFrame(df)

# Convert StockDataFrame as StockPlot
fx = sp.StockPlot(sdf)


# StockDataFrameクラスでインスタンス化を行います。
# 今回の記事では指標の追加は行いませんので、必ずしも必要ではありません。
# 
# `fig = sp.StockPlot(sdf)`でStockPlotクラスでインスタンス化します。
# インスタンス化すると同時に日足に変換され、StockPlotのインスタンス変数`stock_dataframe`に格納されます。
# 2017/3/20-2017/6/17の日足が格納されました。

# In[46]:

fx.stock_dataframe.head(), fx.stock_dataframe.tail()


# ## ローソク足の描画

# In[47]:

fx.candle_plot()


# `fig = sp.StockPlot(sdf)`でインスタンス化されたら即、日足としてプロットが可能です。
# `fig.candle_plot()`で`plotly`で出力する形式`plotly.graph_objs.graph_objs.Figure`(`data`と`layout`がキーとなった辞書)が返されます。
# 
# 画像を見るには`matplotlib.pyplot`のように`show`メソッドを使います。
# `show`メソッドの第一引数`how`のデフォルト引数は`html`です。
# 故に引数なしで`show`するとブラウザの新しいタブが立ち上がってそこに表示されます。
# 今はJupyter Notebook上で描きたいので、`how=jupyter`、または単に`jupyter`を引数にします。

# In[48]:

fx.show(how='jupyter')


# ![gif1](./candle_plot_movable_files/gif1.gif)

# 2017/3/20-2017/6/17の日足が描かれました。
# 
# plotlyの操作は
# 
# * グラフ上のマウスオーバーで値の表示
# * グラフ上のドラッグでズームイン
# * 軸上(真ん中)のドラッグでスクロール
# * 軸上(端)のドラッグでズームアウト
# * ダブルクリックで元のビューに戻る？
# * トリプルクリックで全体表示？

# ## 時間足の変更

# 日足だけじゃなくて別の時間足も見たいです。
# 
# そういうときは`ohlc_convert`メソッドを使って時間幅を変更します。

# In[53]:

fx.ohlc_convert('H')  # 1時間足に変更
fx.candle_plot()  # ローソク足プロット
fx.show('jupyter')  # プロットの表示をJupyter Notebookで開く


# ![gif2](./candle_plot_movable_files/gif2.gif)

# 1時間足がプロットされました。
# あえて時間をかけてマウスオーバーしているのですが、1時間ごとにプロットされていることがわかりましたでしょうか。
# 
# ここで再度データを確認してみますと、1時間ごとにfigのインスタンス変数`stock_dataframe`が1時間足に変わっていることがわかると思います。

# In[50]:

fx.stock_dataframe.head(), fx.stock_dataframe.tail()


# ## プロット範囲の指定

# plotlyのズームイン / アウト、スクロールを使えば表示範囲外のところも見れます。
# しかし「この期間だけを見たい！」というとき、プロットしてからいちいちスクロールするのはメンドウです。
# 
# そこで、`candle_plot`メソッドは見える範囲(view)の指定ができます。
# 例えば2017/5/8から2017/6/5の4時間足が見たいとしましょう。

# In[81]:

fx.ohlc_convert('4H')  # 4時間足に変換
fx.candle_plot(start_view=pd.datetime(2017,5,8), end_view=pd.Timestamp('20170605'))
    # 表示位置(view)のstart / endを指定
    # datetime / Timestamp両方使える
fx.show('png')  # png形式で保存


# ![png1](./candle_plot_movable_files/png1.png)

# * 時間足を変更します。
#     * 4時間足に変換するときは、時間足を表す'H'の前に数字の'4'を付けて`ohlc_convert`メソッドの引数に入れます。
#     * 元のデータが1分足なので、1分足より下の時間足(例えば30秒'30S'など)には変更できません、
# > ```python
# ohlc_convert('4H')
# ```
# * 表示位置を指定します。
#     * 開始位置は`start_view`
#     * 終了位置は`end_view`
#     * dateitme, Timestampの形式で指定できます。
# > ```python
# fx.candle_plot(start_view=pd.datetime(2017,5,8), end_view=pd.Timestamp('20170605'))
# ```
# * グラフを表示します。
#     * 引数にpngを入れることでpng形式として保存します。
#     * いったん新しいタブでhtmlとして表示してから、pngを保存します。
#     * ダイアログボックスがでますのでOKを押してください。
#     * 保存先はブラウザのデフォルトのダウンロードディレクトリです。
# > ```python
# fx.show('png')
# ```

# また、ビューの指定は次のようにすることもできます。

# In[93]:

fx.ohlc_convert('D')  # 日足に変換
fx.candle_plot(periods_view=20, end_view='last')
    # `end_view`を'last'　最後の足に設定する
    # `periods_view`で20足分まで表示する
fx.show('html')  # html形式で表示


# ![gif4](./candle_plot_movable_files/gif4.gif)

# * ohlc_convertメソッドで日足に変換します。
# > ```python
# fx.ohlc_convert('D')
# ```
# * ビューの設定をします。
#     * `end_view`を'last'、すなわち最後の足に設定します。
#     * `start_view`を指定するときは同様に'first'が使えます。`start_view`を最初の足に設定できます。
#     * `periods_view`で20足分まで表示します。
# > ```python
# fx.candle_plot(periods_view=20, end_view='last')
# ```
# * html形式で表示します。
#     * ブラウザの新しいタブが立ち上がり、グラフが表示されます。
# > ```python
# fx.show('html')
# ```

# ## プロット範囲を詰める

# 見てもらった方がわかりやすいかもしれません

# In[ ]:



fig.candle_plot(oh)
# # ソースコード

# # ソースコード解説と応用

# # ごみ

# In[ ]:

# # Add indicator
# for i in range(10, 17):
#     fig.append('close_{}_sma'.format(i))

# # Remove indicator
# for i in [13, 11]:
#     fig.remove('close_{}_sma'.format(i))

# # Pop indicator
# fig.pop()

# # Plot Candle chart

# fig.candle_plot(end='last', periods=50, freq='D')
# # 日足の表示。freqは省略可

# fig.candle_plot(end='last', periods=50, freq='15T')
# # 15分足の表示

# fig.candle_plot(end='last', periods=50, freq='5T')
# # 5分足の表示。5分足でも描画が重くならないのは、cutという引数が、グラフ化してくれるインスタンス変数self.sdfを300足で切り取ってくれるから。
# # **tailじゃなくてixかlocで抜き出すべし**

# fig.candle_plot(end='last', periods=50, freq='H')
# fig.candle_plot(end='last', periods=50, freq='H', cut=None)
# # 時間足の表示
# # cut=None にすれば300で切られずにすべて表示。

# fig.sdf
# fig.StockDataFrame
# # sdfがプロットされているデータ、StockDataFrameはinitされたときに格納されたデータフレーム。時間足変更のために、保存されている

# fig.candle_plot(end='last', periods=50, freq='H', fix=30)
# fig.candle_plot(end='last', periods=50, freq='H', fix=5)
# fig.candle_plot(end='last', periods=50, freq='H', fix=60)
# fig.candle_plot(start=pd.Timestamp('20170401'), end=pd.Timestamp('20170501'), freq='H')
# fig.candle_plot(start=pd.datetime(2017,4,1), end=pd.datetime(2017,5,1), freq='H')
# fig.candle_plot(start=pd.datetime(2017,4,1), end=pd.datetime(2017,5,1), freq='H')
# fig.candle_plot(start=pd.datetime(2017,4,1), end=pd.datetime(2017,5,1), freq='H', cut=False)

# fig.ohlc_convert('4H')
# fig.candle_plot(start_view=start, end_view=end)
# fig.show()
# fig.ohlc_convert('4H')
# fig.candle_plot(start_view=start, end_view='last')
# fig.show()
# fig.ohlc_convert('4H')
# fig.candle_plot(periods_view=150, end_view='last')
# fig.show()
# fig.ohlc_convert('4H')
# fig.candle_plot(periods_view=450, end_view='last')
# fig.show()
# fig.ohlc_convert('4H')
# fig.candle_plot(periods_view=450, end_view='last', periods_data=5)
# fig.show()
# fig.ohlc_convert('4H')
# fig.candle_plot(periods_view=450, end_view='last', periods_data=5, end_data='last')
# fig.show()
# fig.ohlc_convert('4H')
# fig.candle_plot(periods_view=1, end_view='last', periods_data=5, end_data='last')
# fig.show()
# fig.ohlc_convert('4H')
# fig.candle_plot(periods_view=3, end_view='last', periods_data=5, end_data='last')
# fig.show()
# fig.ohlc_convert('4H')
# fig.candle_plot(periods_data=50, end_data='last')
# fig.show()

# fig.ohlc_convert('4H')
# fig.candle_plot(start_data=start, end_data=end, start_view='first', periods_view=100, fix=60)
# fig.show()
# fig.ohlc_convert('4H')
# fig.candle_plot(start_data=start, end_data=end, start_view='first', periods_view=100)
# fig.show()
# fig.ohlc_convert('4H')
# fig.candle_plot(start_data=start, end_data=end, start_view='first', periods_view=100, fix=60)
# fig.show()
# fig.ohlc_convert('4H')
# fig.candle_plot(start_data=start, end_data=end, start_view='first', end_view='last')
# fig.show()
# fig.ohlc_convert('4H')
# fig.candle_plot(start_data=start, end_data=end, start_view='first', end_view='last', fix=60)
# fig.show()

