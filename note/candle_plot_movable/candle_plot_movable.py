
# coding: utf-8

# In[1]:

import sys
sys.path.append('../../common/')


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


# ```python
# # ----------Hide General Module----------
# import stockstats
# import plotly
# ```

# * General Module, Hide General Moduleは一般に配布されているパッケージなので、condaやpipといったパッケージ管理ソフトなどで追加してください。
#     * General ModuleはこのJupyter Notebook内で使います。
#     * Hide General Moduleは`stockplot`内で使用します。
# >```sh
# conda install plotly
# pip install stockstats
# ```
# * User Moduleのstockplotについては以下にソースコード貼ります。
#     * 旧バージョン[Qiita - u1and0 / plotlyでキャンドルチャートプロット](http://qiita.com/u1and0/items/0ebcf097a1d61c636eb9)
# * random_walkについては[Qiita - u1and0 / pythonでローソク足(candle chart)の描画](http://qiita.com/u1and0/items/1d9afdb7216c3d2320ef)

# ## サンプルデータの作成

# In[3]:

# Make sample data
np.random.seed(1)
df = randomwalk(60 * 60 * 24 * 90, freq='S', tick=0.01, start=pd.datetime(2017, 3, 20))    .resample('T').ohlc() + 115  # 90日分の1分足, 初期値が115


# ランダムな為替チャートを作成します。
# randomwalk関数で"2017/3/20からの1分足を90日分作成します。

# ## インスタンス化

# In[4]:

# Convert StockDataFrame as StockPlot
fx = sp.StockPlot(df)


# StockDataFrameクラスでインスタンス化を行います。
# 
# `fx = sp.StockPlot(df)`でStockPlotクラスでインスタンス化します。

# # ローソク足の描画

# `fig = sp.StockPlot(sdf)`でインスタンス化されたら時間足を変換します。
# 変換する際は`ohlc_convert`メソッドを使います。

# In[5]:

fx.ohlc_convert('D').head()


# 変換されたデータは`stock_dataframe`というインスタンス変数に格納されます。

# In[6]:

fx.stock_dataframe.head(), fx.stock_dataframe.tail()


# 2017/3/20-2017/6/17の日足が格納されました。

# 1分足として入力したデータを日足に変換したデータが返されました。

# 時間足の変換が済むと、プロットが可能です。
# プロットするときは`plot`メソッドです。

# In[7]:

fx.plot()


# `fig.plot()`で`plotly`で出力する形式`plotly.graph_objs.graph_objs.Figure`(`data`と`layout`がキーとなった辞書)が返されます。
# 
# 画像を見るには`matplotlib.pyplot`のように`show`メソッドを使います。
# `show`メソッドの第一引数`how`のデフォルト引数は`html`です。
# 引数なしで`show`するとブラウザの新しいタブが立ち上がってそこに表示されます。
# 今はJupyter Notebook上で描きたいので、`how=jupyter`、または単に`jupyter`を引数にします。

# In[8]:

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
# * ダブルクリックで元のビューに戻る
# * トリプルクリックで全体表示

# # 時間足の変更

# 日足だけじゃなくて別の時間足も見たいです。
# 
# そういうときは`ohlc_convert`メソッドを使って時間幅を変更します。

# In[9]:

fx.ohlc_convert('H')  # 1時間足に変更
fx.plot()  # ローソク足プロット
fx.show('jupyter')  # プロットの表示をJupyter Notebookで開く


# ![gif2](./candle_plot_movable_files/gif2.gif)

# 1時間足がプロットされました。
# あえて時間をかけてマウスオーバーしているのですが、1時間ごとにプロットされていることがわかりましたでしょうか。
# 
# ここで再度データを確認してみますと、1時間ごとにfigのインスタンス変数`stock_dataframe`が1時間足に変わっていることがわかると思います。

# In[10]:

fx.stock_dataframe.head(), fx.stock_dataframe.tail()


# # プロット範囲の指定

# `plot`メソッドで描かれるデータ範囲(`plot_dataframe`)と蓄えられているデータ範囲(`stock_dataframe`)は区別されます。
# > 「株」の意味のstockと「蓄え」としての意味のstockをかけています。
# 
# `plot_dataframe, stock_dataframe`はインスタンス変数としてアクセスできます。
# 
# 5分足のチャートを描き、それぞれのインスタンス変数を表示してみます。

# In[28]:

fx.ohlc_convert('5T')  # 5分足に変換
fx.plot()
fx.show('jupyter')


# ![gif6](./candle_plot_movable_files/gif6.gif)

# 2017/3/20-2017/6/17の5分足が描かれましたが、最初の足が2017/6/16で終わっています。
# 
# これはプロットされるデータの範囲`plot_dataframe`が2017/6/16までで切られているためです。

# In[21]:

# データとして保存される`stock_dataframe`
fx.stock_dataframe.index


# In[19]:

# プロットするデータとして保存される`plot_dataframe`
fx.plot_dataframe.index


# 2017/3/20から2017/6/17までを5分足に変換すると、`stock_dataframe`のインデックスは大変長い列(長さ{{len(fx.stock_dataframe)}})になります。  一方で、`plot_dataframe`のインデックスは短い列(長さ{{len(fx.plot_dataframe)}})になります。
# 
# `stock_dataframe`のようにデータとして保持している分にはいくら長くてもメモリを食いつぶす程度ですが、`plot_dataframe`は描画に用いられるデータですので、長いと`show`メソッド時に大変リソースを食います。**グラフとして表示したところで、見る範囲は限定的だろうとの考えから、`plot_dataframe`は`stock_dataframe`から一部切り出した形にしています。**
# 
# `plot_dataframe`の長さは、`plot`メソッドの引数として与えることができます。

# * `plot`メソッドのプロット範囲を決める引数
#     * `start_plot`: グラフ化する最初の日付・時間
#     * `end_plot`: グラフ化する最後の日付・時間
#     * `periods_plot`: グラフ化する足の数(int型)
# * start, end, periodsのうち二つが指定されている必要がある。
# * 何も指定しなければ、デフォルト値が入力される。
# > ```python
# # デフォルト値
# end_plot= self.stock_dataframe.index[-1]
# periods_plot=300
# ```

# `start_plot, end_plot`を指定して描画してみます。

# In[40]:

# fx.ohlc_convert('5T')  # 既に5分足に変換されているので必要ない
start = pd.datetime(2017,6,17,9,0,0)     # 2017/6/17 09:00
end = pd.datetime(2017,6,17,23,0,0)      # 2017/6/17 23:00 
fx.plot(start_plot=start, end_plot=end)  # 2017/6/17 09:00-23:00までをプロットする
fx.show('jupyter')


# ![gif7](./candle_plot_movable_files/gif7.gif)

# 2017/6/17 09:00 - 2017/6/17 23:00の5分足が描かれました。

# # ビュー範囲の指定

# `plot_dataframe`の期間を指定すれば、インスタンス化する前のデータフレームに入っている日付・時間内のプロットを見れます。
# plotlyのズームイン / アウト、スクロールを使えば表示範囲外のところも見れます。
# しかし、見たい期間が最初から決まっているのにもかかわらず、グラフ化してからスクロールするのはメンドウです。
# 
# そこで、`plot`メソッドではグラフ化して最初に見えるビュー範囲(view)を指定できます。

# * `plot`メソッドのビュー範囲を決める引数
#     * `start_view`: 表示する最初の日付・時間
#     * `end_view`: 表示する最後の日付・時間
#     * `periods_view`: 表示する足の数(int型)
# * start, end, periodsのうち二つが指定されている必要がある。
# * 何も指定しなければ、デフォルト値が入力される。
# > ```python
# # デフォルト値
# end_view = self.plot_dataframe.index[-1]
# periods_view = 50
# ```

# 例えば2017/5/8から2017/6/5の4時間足が見たいとしましょう。

# In[43]:

fx.ohlc_convert('4H')  # 4時間足に変換
start = pd.datetime(2017,5,8)   # 2017/5/8
end = pd.Timestamp('20170605')  # 2017/6/5(Timestampでも指定可能)
fx.plot(start_view=start, end_view=end) # 2017/5/8 - 2017/6/5を表示する
fx.show('jupyter')


# ![gif8](./candle_plot_movable_files/gif8.gif)

# `end_view, periods_view`引数を使って表示してみます。

# In[44]:

fx.ohlc_convert('D')  # 日足に変換
fx.plot(periods_view=20, end_view='last')
    # `end_view`を'last'　最後の足に設定する
    # `periods_view`で20本足表示する
fx.show('html')  # html形式で表示


# ![gif4](./candle_plot_movable_files/gif4.gif)

# * ohlc_convertメソッドで日足に変換します。
# > ```python
# fx.ohlc_convert('D')
# ```
# * ビューの設定をします。
#     * `pd.date_range`関数のように、`start, end, periods`のうち二つが指定されなければエラーです。
#     * 指定できる変数は以下の3つです。
#         * `start_view`(datetime)
#         * `end_view`(datetime)
#         * `periods_view`(int)
#     * `end_view`を'last'、すなわち最後の足に設定します。
#         * `start_view`を指定するときは`end_view`の'last'に対応して、'first'が使えます。
#         * 'first'は最初の足、を意味します。
#     * `periods_view`で20本の足まで表示します。
# > ```python
# fx.plot(periods_view=20, end_view='last')
# ```
# * html形式で表示します。
#     * ブラウザの新しいタブが立ち上がり、グラフが表示されます。
#     * 対応しているフォーマット
#         * jupyter, html, png, jpeg, webp, svg
# > ```python
# fx.show('html')
# ```

# # 右側に空白を作る

# 右側に空白を作ります。
# 引数`fix`に指定した足の本数だけ、右側に空白を作ります。
# > 時間足が短いとうまくいきません。原因究明中です。
# 
# 予測線を引いたり一目均衡表では必要になる機能だと思います。

# In[13]:

fx.plot()
fx.show('jupyter')


# In[14]:

fx.plot(fix=30)
fx.show('jupyter')


# ![gif5](./candle_plot_movable_files/gif5.gif)

# `plot`メソッドの`fix`引数を30とし、30本の足だけの空白を右側(時間の遅い側)に作ることができました。
# `start_view, end_view`の位置は指定した日付通りで変わりません。
# 今回の場合、`start_view, end_view`は指定していないので、デフォルトの`end_view='last', periods_view=50`が指定されたことになります。

# ## data範囲、plot範囲, view範囲、fixまとめ

# 図示すると以下のような感じです。

# ![png4](./candle_plot_movable_files/png4.png)

# |    |  stock_dataframe  |  plot_dataframe  |  view  |
# |----|-------------------|------------------|----------|
# |  `show`で最初に表示される  |  x  |  x  |  o  |
# |  `show`でドラッグすれば見ることができる  | x  |   o  |  o  |
# |  インスタンス変数としてアクセス可  |  o  |  o  |  x  |

# # まとめ

# * `ohlc_convert`メソッド
#     * 時間足を決める。
#         * `freq`
#     * `stock_dataframe`を決める。
# * `plot`メソッド
#     * plot範囲(`plot_dataframe`)を決める。
#         * `start_plot`
#         * `end_plot`
#         * `periods_plot`
#     * view範囲を決める。
#         * `start_view`
#         * `end_view`
#         * `periods_view`
#     * グラフの右側の空白(fix)を決める。
#         * `fix`
# * `show`メソッド
#     * 出力形式を決める。
#         * `how='jupyter', 'html', 'png', 'jpeg', 'webp', 'svg'`
#     * ファイル名を決める。
#         * `filebasename`

# In[ ]:



