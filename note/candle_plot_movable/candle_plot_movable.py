
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
# randomwalk関数で**2017/3/20からの1分足を90日分**作成します。

# ## インスタンス化

# In[14]:

# Convert DataFrame as StockPlot
fx = sp.StockPlot(df)


# StockPlotクラスでインスタンス化します。

# # ローソク足の描画

# `fig = sp.StockPlot(sdf)`でインスタンス化されたら時間足を変換します。
# 変換する際は`ohlc_convert`メソッドを使います。

# In[5]:

fx.ohlc_convert('D').head()


# 1分足として入力したデータを日足に変換したデータが返されました。
# 変換されたデータは`stock_dataframe`というインスタンス変数に格納されます。

# In[6]:

fx.stock_dataframe.head(), fx.stock_dataframe.tail()


# 2017/3/20-2017/6/17の日足ができたことを確認しました。
# 
# 時間足の変換が済むと、プロットが可能です。
# プロットするときは`plot`メソッドを使います。

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
# ここで再度`stock_dataframe`を確認してみますと、1時間足に変わっていることがわかります。

# In[10]:

fx.stock_dataframe.head(), fx.stock_dataframe.tail()


# `'open', 'high', 'low', 'close'`のカラムを持ったデータフレームの変換を行う`ohlc_convert`メソッドは以下のように記述されます。

# In[15]:

def ohlc_convert(self, freq: str):
    """Convert ohlc time span

    USAGE: `fx.ohlc_convert('D')  # 日足に変換`

    * Args:  変更したい期間 M(onth) | W(eek) | D(ay) | H(our) | T(Minute) | S(econd)
    * Return: スパン変更後のデータフレーム
    """
    self.freq = freq
    self.stock_dataframe = self._init_stock_dataframe.ix[:, ['open', 'high', 'low', 'close']]        .resample(freq).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})        .dropna()
    return self.stock_dataframe


# ```python
# df.resample(freq).ohlc()
# ```
# 
# とすると階層が分かれたohlcのデータフレームが出来上がってしまうので
# 
# ```python
# df.resample(freq).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})
# ```
# 
# のように`agg`メソッドを使うことです。
# 
# `freq`は`df.resample`で使える時間であれば自由なので、freq='1D4H2T24S'とすると'1日と4時間2分24秒足'といった変な時間足を作れます。

# In[17]:

fx.ohlc_convert('1D4H2T24S').head()


# # グラフ範囲の指定

# `plot`メソッドは`stock_dataframe`の中身を**すべてグラフ化しません**。
# デフォルトの場合、**最後の足から数えて300本足**がグラフ化されます。

# 例として、5分足のチャートを描きます。

# In[11]:

fx.ohlc_convert('5T')  # 5分足に変換
fx.plot()
fx.show('jupyter')


# ![gif6](./candle_plot_movable_files/gif6.gif)

# In[12]:

fx.stock_dataframe.index


# 2017/3/20-2017/6/17ののデータフレームを5分足に変換してローソク足を描きました。
# 最初の足が2017/3/20ではなく2017/6/16で途切れています。
# これはグラフ化される範囲が5分足の300本足で切られているためです。

# 描画されるデータが大きいと`show`メソッド時に大変リソースを食います。
# **グラフとして見る範囲は限定的だろうとの考えから、`plot`メソッドは`stock_dataframe`から一部切り出した形をグラフ化します。**
# 
# グラフ化する範囲は、`plot`メソッドの引数として与えることができます。

# * `plot`メソッドのプロット範囲を決める引数
#     * `start_plot`: グラフ化する最初の日付・時間
#     * `end_plot`: グラフ化する最後の日付・時間
#     * `periods_plot`: グラフ化する足の数(int型)
# * start, end, periodsのうち二つが指定されている必要がある。
# * 何も指定しなければ、デフォルト値が入力される。
# > ```python
# # Default Args
# if com._count_not_none(start_plot,
#                        end_plot, periods_plot) == 0:  # すべてNoneのままだったら
#     end_plot = 'last'  # 最後の足から
#     periods_plot = 300  # 300本足で切る
# # first/last
# start_plot = self.stock_dataframe.index[0] if start_plot == 'first' else start_plot
# end_plot = self.stock_dataframe.index[-1] if end_plot == 'last' else end_plot  # 'last'=最後の足とはindexの最後
# ```

# `start_plot, end_plot`を指定して描画してみます。

# In[ ]:

# fx.ohlc_convert('5T')  # 既に5分足に変換されているので必要ない
start = pd.datetime(2017,6,17,9,0,0)     # 2017/6/17 09:00
end = pd.datetime(2017,6,17,23,0,0)      # 2017/6/17 23:00 
fx.plot(start_plot=start, end_plot=end)  # 2017/6/17 09:00-23:00までをプロットする
fx.show('jupyter')


# ![gif7](./candle_plot_movable_files/gif7.gif)

# 2017/6/17 09:00 - 2017/6/17 23:00の5分足が描かれました。

# # ビュー範囲の指定

# plotlyのズームイン / アウト、スクロールを使えば表示範囲外のところも見れます。
# しかし、見たい期間が最初から決まっているのにもかかわらず、グラフ化してからスクロールするのはメンドウです。
# 
# そこで、`plot`メソッドではグラフ化して最初に見えるビュー範囲(view)を指定できます。

# 例えば2017/5/8から2017/6/5の4時間足が見たいとしましょう。

# In[ ]:

fx.ohlc_convert('4H')  # 4時間足に変換
start = pd.datetime(2017,5,8)   # 2017/5/8
end = pd.Timestamp('20170605')  # 2017/6/5(Timestampでも指定可能)
fx.plot(start_view=start, end_view=end) # 2017/5/8 - 2017/6/5を表示する
fx.show('jupyter')


# ![gif8](./candle_plot_movable_files/gif8.gif)

# 次は`start_view, end_view`の指定ではなく、`end_view, periods_view`を使って表示してみます。

# In[ ]:

fx.ohlc_convert('D')  # 日足に変換
fx.plot(periods_view=20, end_view='last')
    # `end_view`を'last'　最後の足に設定する
    # `periods_view`で20本足表示する
fx.show('html')  # html形式で表示


# ![gif4](./candle_plot_movable_files/gif4.gif)

# * `plot`メソッドのビュー範囲を決める引数
#     * `start_view`: 表示する最初の日付・時間
#     * `end_view`: 表示する最後の日付・時間
#     * `periods_view`: 表示する足の数(int型)
# * start, end, periodsのうち二つが指定されている必要がある。
# * 何も指定しなければ、デフォルト値が入力される。
# > ```python
# # Default Args
# if com._count_not_none(start_view,
#                        end_view, periods_view) == 0:  # すべてNoneのままだったら
#     end_view = 'last'  # 最後の足から
#     periods_view = 50  # 50本足までを表示する
# # first/last
# start_view = plot_dataframe.index[0] if start_view == 'first' else start_view
# end_view = plot_dataframe.index[-1] if end_view == 'last' else end_view  # 'last'はindexの最後
# ```

# `periods`の指定は`end`が指定された場合は`start`、`start`が指定された場合は`end`を計算します。
# 計算する関数は次のようにしました。

# In[19]:

from pandas.core import common as com
def set_span(start=None, end=None, periods=None, freq='D'):
    """ 引数のstart, end, periodsに対して
    startとendの時間を返す。

    * start, end, periods合わせて2つの引数が指定されていなければエラー
    * start, endが指定されていたらそのまま返す
    * start, periodsが指定されていたら、endを計算する
    * end, periodsが指定されていたら、startを計算する
    """
    if com._count_not_none(start, end, periods) != 2:  # 引数が2個以外であればエラー
        raise ValueError('Must specify two of start, end, or periods')
    start = start if start else (pd.Period(end, freq) - periods).start_time
    end = end if end else (pd.Period(start, freq) + periods).start_time
    return start, end


# 呼び出すときは次のようにします。
# ```python
# start_view, end_view = set_span(start_view, end_view, periods_view, self.freq)
# ```
# > 説明は省きましたが、`periods_plot`引数として、グラフ化する時間足の指定も`view`と同様にできます。

# # 右側に空白を作る

# 引数`shift`に指定した足の本数だけ、右側に空白を作ります。
# > 時間足が短いとうまくいきません。原因究明中です。
# 
# 予測線を引いたり一目均衡表では必要になる機能だと思います。

# In[ ]:

fx.plot()
fx.show('jupyter')


# In[21]:

fx.plot(shift=30)
fx.show('jupyter')


# ![gif5](./candle_plot_movable_files/gif5.gif)

# `plot`メソッドの`fix`引数を30とし、30本の足だけの空白を右側(時間の遅い側)に作ることができました。
# `start_view, end_view`の位置は指定した日付通りで変わりません。
# 今回の場合、`start_view, end_view`は指定していないので、デフォルトの`end_view='last', periods_view=50`が指定されたことになります。

# ## data範囲、plot範囲, view範囲、shiftまとめ

# 図示すると以下のような感じです。

# ![png4](./candle_plot_movable_files/png4.png)

# # まとめ

# * `ohlc_convert`メソッド
#     * `freq`引数で時間足を決める。
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
#     * グラフの右側の空白(shift)を決める。
#         * `shift`
# * `show`メソッド
#     * 出力形式を決める。
#         * `how='jupyter', 'html', 'png', 'jpeg', 'webp', 'svg'`
#     * ファイル名を決める。
#         * `filebasename`

# # ごみ

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

# |    |  stock_dataframe  |  plot_dataframe  |  view  |
# |----|-------------------|------------------|----------|
# |  `show`で最初に表示される  |  x  |  x  |  o  |
# |  `show`でドラッグすれば見ることができる  | x  |   o  |  o  |
# |  インスタンス変数としてアクセス可  |  o  |  x  |  x  |

# In[ ]:



