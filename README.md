```python
import sys
sys.path.append('../../bin/')
```

# 下準備

## モジュールインポート

必要なモジュールをインポートします。


```python
# ----------General Module----------
import numpy as np
import pandas as pd
# ----------User Module----------
from randomwalk import randomwalk
import stockplot as sp
```


<script>requirejs.config({paths: { 'plotly': ['https://cdn.plot.ly/plotly-latest.min']},});if(!window.Plotly) {{require(['plotly'],function(plotly) {window.Plotly=plotly;});}}</script>


```python
# ----------Hide General Module----------
import stockstats
import plotly
```

* General Module, Hide General Moduleは一般に配布されているパッケージなので、condaやpipといったパッケージ管理ソフトなどで追加してください。
    * General ModuleはこのJupyter Notebook内で使います。
    * Hide General Moduleは`stockplot`内で使用します。
>```sh
conda install plotly
pip install stockstats
```
* User Moduleのstockplotについては以下にソースコード貼ります。
    * 旧バージョン[Qiita - u1and0 / plotlyでキャンドルチャートプロット](http://qiita.com/u1and0/items/0ebcf097a1d61c636eb9)
* random_walkについては[Qiita - u1and0 / pythonでローソク足(candle chart)の描画](http://qiita.com/u1and0/items/1d9afdb7216c3d2320ef)

## サンプルデータの作成


```python
# Make sample data
np.random.seed(1)
df = randomwalk(60 * 60 * 24 * 90, freq='S', tick=0.01, start=pd.datetime(2017, 3, 20))\
    .resample('T').ohlc() + 115  # 90日分の1分足, 初期値が115
```

ランダムな為替チャートを作成します。
randomwalk関数で**2017/3/20からの1分足を90日分**作成します。

## インスタンス化


```python
# Convert DataFrame as StockPlot
fx = sp.StockPlot(df)
```

StockPlotクラスでインスタンス化します。

# ローソク足の描画

`fig = sp.StockPlot(sdf)`でインスタンス化されたら時間足を変換します。
変換する際は`resample`メソッドを使います。


```python
fx.resample('D').head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>low</th>
      <th>open</th>
      <th>close</th>
      <th>high</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-03-20</th>
      <td>112.71</td>
      <td>115.00</td>
      <td>114.22</td>
      <td>116.80</td>
    </tr>
    <tr>
      <th>2017-03-21</th>
      <td>113.67</td>
      <td>114.23</td>
      <td>115.52</td>
      <td>116.23</td>
    </tr>
    <tr>
      <th>2017-03-22</th>
      <td>112.23</td>
      <td>115.51</td>
      <td>112.29</td>
      <td>117.44</td>
    </tr>
    <tr>
      <th>2017-03-23</th>
      <td>111.88</td>
      <td>112.28</td>
      <td>116.02</td>
      <td>116.08</td>
    </tr>
    <tr>
      <th>2017-03-24</th>
      <td>114.76</td>
      <td>116.03</td>
      <td>118.60</td>
      <td>119.10</td>
    </tr>
  </tbody>
</table>
</div>



1分足として入力したデータを日足に変換したデータが返されました。
変換されたデータは`stock_dataframe`というインスタンス変数に格納されます。


```python
fx.stock_dataframe.head(), fx.stock_dataframe.tail()
```




    (               low    open   close    high
     2017-03-20  112.71  115.00  114.22  116.80
     2017-03-21  113.67  114.23  115.52  116.23
     2017-03-22  112.23  115.51  112.29  117.44
     2017-03-23  111.88  112.28  116.02  116.08
     2017-03-24  114.76  116.03  118.60  119.10,
                    low    open   close    high
     2017-06-13  103.18  106.19  106.12  106.28
     2017-06-14  104.59  106.13  108.07  108.51
     2017-06-15  103.97  108.06  105.66  108.86
     2017-06-16  104.94  105.66  108.25  108.59
     2017-06-17  107.31  108.24  109.22  110.73)



2017/3/20-2017/6/17の日足ができたことを確認しました。

時間足の変換が済むと、プロットが可能です。
プロットするときは`plot`メソッドを使います。


```python
fx.plot()
```

`fig.plot()`で`plotly`で出力する形式`plotly.graph_objs.graph_objs.Figure`(`data`と`layout`がキーとなった辞書)が返されます。

画像を見るには`matplotlib.pyplot`のように`show`メソッドを使います。
`show`メソッドの第一引数`how`のデフォルト引数は`html`です。
引数なしで`show`するとブラウザの新しいタブが立ち上がってそこに表示されます。
今はJupyter Notebook上で描きたいので、`how=jupyter`、または単に`jupyter`を引数にします。

```python
def show(self, how='html', filebasename='candlestick_and_trace'):
    """Export file type"""
    if how == 'html':
        ax = pyo.plot(self._fig, filename=filebasename + '.html',
                      validate=False)  # for HTML
    elif how == 'jupyter':
        ax = pyo.iplot(self._fig, filename=filebasename + '.html',
                       validate=False)  # for Jupyter Notebook
    elif how in ('png', 'jpeg', 'webp', 'svg'):
        ax = pyo.plot(self._fig, image=how, image_filename=filebasename,
                      validate=False)  # for file exporting
    else:
        raise KeyError(how)
    return ax
```


```python
fx.show(how='jupyter')
```



![gif1](https://github.com/u1and0/stockplot/blob/master/note/candle_plot_movable/candle_plot_movable_files/gif1.gif)

2017/3/20-2017/6/17の日足が描かれました。

plotlyの操作は

* グラフ上のマウスオーバーで値の表示
* グラフ上のドラッグでズームイン
* 軸上(真ん中)のドラッグでスクロール
* 軸上(端)のドラッグでズームアウト
* ダブルクリックで元のビューに戻る
* トリプルクリックで全体表示

# 時間足の変更

日足だけじゃなくて別の時間足も見たいです。

そういうときは`resample`メソッドを使って時間幅を変更します。


```python
fx.resample('H')  # 1時間足に変更
fx.plot()  # ローソク足プロット
fx.show('jupyter')  # プロットの表示をJupyter Notebookで開く
```



![gif2](https://github.com/u1and0/stockplot/blob/master/note/candle_plot_movable/candle_plot_movable_files/gif2.gif)

1時間足がプロットされました。
あえて時間をかけてマウスオーバーしているのですが、1時間ごとにプロットされていることがわかりましたでしょうか。

ここで再度`stock_dataframe`を確認してみますと、1時間足に変わっていることがわかります。


```python
fx.stock_dataframe.head(), fx.stock_dataframe.tail()
```




    (                        low    open   close    high
     2017-03-20 00:00:00  114.76  115.00  115.26  115.49
     2017-03-20 01:00:00  115.27  115.27  116.11  116.47
     2017-03-20 02:00:00  115.69  116.10  115.69  116.53
     2017-03-20 03:00:00  115.62  115.68  116.02  116.19
     2017-03-20 04:00:00  115.74  116.01  116.00  116.31,
                             low    open   close    high
     2017-06-17 19:00:00  108.50  108.65  109.91  109.93
     2017-06-17 20:00:00  109.56  109.90  109.76  110.03
     2017-06-17 21:00:00  109.47  109.76  109.77  110.06
     2017-06-17 22:00:00  109.27  109.77  109.31  110.10
     2017-06-17 23:00:00  108.96  109.30  109.22  109.70)



`'open', 'high', 'low', 'close'`のカラムを持ったデータフレームの変換を行う`resample`メソッドは以下のように記述しました。

```python
def resample(self, freq: str):
    """Convert ohlc time span

    USAGE: `fx.resample('D')  # 日足に変換`

    * Args:  変更したい期間 M(onth) | W(eek) | D(ay) | H(our) | T(Minute) | S(econd)
    * Return: スパン変更後のデータフレーム
    """
    self.freq = freq  # plotやviewの範囲を決めるために後で使うのでインスタンス変数に入れる
    self.stock_dataframe = self._init_stock_dataframe.ix[:, ['open', 'high', 'low', 'close']]\
        .resample(freq).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})\
        .dropna()
    return self.stock_dataframe
```

```python
df.resample(freq).ohlc()
```

とすると階層が分かれたohlcのデータフレームが出来上がってしまうので

```python
df.resample(freq).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})
```

のように`agg`メソッドを使います。

`freq`は`df.resample`で使える時間であれば自由なので、例えばfreq='1D4H2T24S'とすると'1日と4時間2分24秒足'といった変な時間足を作れます。


```python
fx.resample('1D4H2T24S').head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>low</th>
      <th>open</th>
      <th>close</th>
      <th>high</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-03-20 00:00:00</th>
      <td>112.71</td>
      <td>115.00</td>
      <td>114.28</td>
      <td>116.80</td>
    </tr>
    <tr>
      <th>2017-03-21 04:02:24</th>
      <td>113.67</td>
      <td>114.28</td>
      <td>116.92</td>
      <td>117.44</td>
    </tr>
    <tr>
      <th>2017-03-22 08:04:48</th>
      <td>111.93</td>
      <td>116.91</td>
      <td>112.38</td>
      <td>117.26</td>
    </tr>
    <tr>
      <th>2017-03-23 12:07:12</th>
      <td>111.88</td>
      <td>112.38</td>
      <td>117.79</td>
      <td>118.01</td>
    </tr>
    <tr>
      <th>2017-03-24 16:09:36</th>
      <td>116.71</td>
      <td>117.80</td>
      <td>120.74</td>
      <td>121.27</td>
    </tr>
  </tbody>
</table>
</div>



# plot範囲の指定

`plot`メソッドは`stock_dataframe`の中身を**すべてグラフ化しません**。
デフォルトの場合、**最後の足から数えて300本足**がグラフ化されます。

例として、5分足のチャートを描きます。


```python
fx.resample('5T')  # 5分足に変換
fx.plot()
fx.show('jupyter')
```


![gif6](https://github.com/u1and0/stockplot/blob/master/note/candle_plot_movable/candle_plot_movable_files/gif6.gif)


```python
# stock_dataframeは2017/3/20から
fx.stock_dataframe.index
```




    DatetimeIndex(['2017-03-20 00:00:00', '2017-03-20 00:05:00',
                   '2017-03-20 00:10:00', '2017-03-20 00:15:00',
                   '2017-03-20 00:20:00', '2017-03-20 00:25:00',
                   '2017-03-20 00:30:00', '2017-03-20 00:35:00',
                   '2017-03-20 00:40:00', '2017-03-20 00:45:00',
                   ...
                   '2017-06-17 23:10:00', '2017-06-17 23:15:00',
                   '2017-06-17 23:20:00', '2017-06-17 23:25:00',
                   '2017-06-17 23:30:00', '2017-06-17 23:35:00',
                   '2017-06-17 23:40:00', '2017-06-17 23:45:00',
                   '2017-06-17 23:50:00', '2017-06-17 23:55:00'],
                  dtype='datetime64[ns]', length=25920, freq='5T')



2017/3/20-2017/6/17ののデータフレームを5分足に変換してローソク足を描きました。
最初の足が2017/3/20ではなく2017/6/16で途切れています。
これはグラフ化される範囲が5分足の300本足で切られているためです。

描画されるデータが大きいと`show`メソッド時に大変リソースを食います。
**グラフとして見る範囲は限定的だろうとの考えから、`plot`メソッドは`stock_dataframe`から一部切り出した形をグラフ化(plot)します。**

グラフ化する範囲は、`plot`メソッドの引数として与えることができます。

* `plot`メソッドのプロット範囲を決める引数
    * `start_plot`: グラフ化する最初の日付・時間
    * `end_plot`: グラフ化する最後の日付・時間
    * `periods_plot`: グラフ化する足の数(int型)
* start, end, periodsのうち二つが指定されている必要がある。
* 何も指定しなければ、デフォルト値が入力される。
> ```python
# Default Args
if com._count_not_none(start_plot,
                       end_plot, periods_plot) == 0:  # すべてNoneのままだったら
    end_plot = 'last'  # 最後の足から
    periods_plot = 300  # 300本足で切る
# first/last
start_plot = self.stock_dataframe.index[0] if start_plot == 'first' else start_plot
end_plot = self.stock_dataframe.index[-1] if end_plot == 'last' else end_plot  # 'last'=最後の足とはindexの最後
```

`start_plot, end_plot`を指定して描画してみます。


```python
# fx.resample('5T')  # 既に5分足に変換されているので必要ない
start = pd.datetime(2017,6,17,9,0,0)     # 2017/6/17 09:00
end = pd.datetime(2017,6,17,23,0,0)      # 2017/6/17 23:00 
fx.plot(start_plot=start, end_plot=end)  # 2017/6/17 09:00-23:00までをプロットする
fx.show('jupyter')
```


![gif7](https://github.com/u1and0/stockplot/blob/master/note/candle_plot_movable/candle_plot_movable_files/gif7.gif)

2017/6/17 09:00 - 2017/6/17 23:00の5分足が描かれました。

# view範囲の指定

plotlyのズームイン / アウト、スクロールを使えば表示範囲外のところも見れます。
しかし、見たい期間が最初から決まっているのにもかかわらず、グラフ化してからスクロールするのはメンドウです。

そこで、`plot`メソッドではグラフ化して最初に見えるビュー範囲(view)を指定できます。

例えば2017/5/8から2017/6/5の4時間足が見たいとしましょう。


```python
fx.resample('4H')  # 4時間足に変換
start = pd.datetime(2017,5,8)   # 2017/5/8
end = pd.Timestamp('20170605')  # 2017/6/5(Timestampでも指定可能)
fx.plot(start_view=start, end_view=end) # 2017/5/8 - 2017/6/5を表示する
fx.show('jupyter')
```


![gif8](https://github.com/u1and0/stockplot/blob/master/note/candle_plot_movable/candle_plot_movable_files/gif8.gif)

次は`start_view, end_view`の指定ではなく、`end_view, periods_view`を使って表示してみます。


```python
fx.resample('D')  # 日足に変換
fx.plot(periods_view=20, end_view='last')
    # `end_view`を'last'　最後の足に設定する
    # `periods_view`で20本足表示する
fx.show('html')  # html形式で表示
```




    'file://C:\\Users\\U1and0\\Dropbox\\Program\\python\\fxpy\\note\\candle_plot_movable\\candlestick_and_trace.html'



![gif4](https://github.com/u1and0/stockplot/blob/master/note/candle_plot_movable/candle_plot_movable_files/gif4.gif)

* `plot`メソッドのビュー範囲を決める引数
    * `start_view`: 表示する最初の日付・時間
    * `end_view`: 表示する最後の日付・時間
    * `periods_view`: 表示する足の数(int型)
* start, end, periodsのうち二つが指定されている必要がある。
* 何も指定しなければ、デフォルト値が入力される。
> ```python
# Default Args
if com._count_not_none(start_view,
                       end_view, periods_view) == 0:  # すべてNoneのままだったら
    end_view = 'last'  # 最後の足から
    periods_view = 50  # 50本足までを表示する
# first/last
start_view = plot_dataframe.index[0] if start_view == 'first' else start_view
end_view = plot_dataframe.index[-1] if end_view == 'last' else end_view  # 'last'はindexの最後
```

`periods`の指定は`end`が指定された場合は`start`、`start`が指定された場合は`end`を計算します。
計算する関数は次のようにしました。

```python
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
    # `start`が指定されていれば`start`をそのまま返し、そうでなければ`end`から`periods`引いた時間を`start`とする。
    start = start if start else (pd.Period(end, freq) - periods).start_time
    # `end`が指定されていれば`end`をそのまま返し、そうでなければ`start`から`periods`足した時間を`end`とする。
    end = end if end else (pd.Period(start, freq) + periods).start_time
    return start, end
```

呼び出すときは次のようにします。
```python
start_view, end_view = set_span(start_view, end_view, periods_view, self.freq)
```
> 説明は省きましたが、グラフ化する時間足も`view`と同様に`periods_plot`引数として指定できます。

`view`は`self._fig`の`layout`において、xaxisの範囲(range)を変更するのに使います。

変更する際、unix時間に変換する必要があるので、`to_unix_time`関数に通します。

```python
def to_unix_time(*dt: pd.datetime)->iter:
    """datetimeをunix秒に変換
    引数: datetime(複数指定可能)
    戻り値: unix秒に直されたイテレータ"""
    epoch = pd.datetime.utcfromtimestamp(0)
    return ((i - epoch).total_seconds() * 1000 for i in dt)
```


```python
view = list(to_unix_time(start_view, end_view))
# ---------Plot graph----------
self._fig['layout'].update(xaxis={'showgrid': showgrid, 'range': view},
                           yaxis={"autorange": True})
```

# 右側に空白を作る

引数`shift`に指定した足の本数だけ、右側に空白を作ります。
> 時間足が短いとうまくいきません。原因究明中です。
> 想定より多めに足の数を設定することでとりあえず回避しています。

予測線を引いたり一目均衡表を使うとき必要になる機能だと思います。


```python
fx.plot()
fx.show('jupyter')
```



```python
fx.plot(shift=30)
fx.show('jupyter')
```


![gif5](https://github.com/u1and0/stockplot/blob/master/note/candle_plot_movable/candle_plot_movable_files/gif5.gif)

`plot`メソッドの`fix`引数を30とし、30本の足だけの空白を右側(時間の遅い側)に作ることができました。
処理としては、先ほど出てきた`set_span`関数を使って、`end_view`に30本足分の時間足を足してあげます。

```python
end_view = set_span(start=end_view, periods=shift,
                    freq=self.freq)[-1] if shift else end_view
```

## data範囲、plot範囲, view範囲、shiftまとめ

図示すると以下のような感じです。

![png4](https://github.com/u1and0/stockplot/blob/master/note/candle_plot_movable/candle_plot_movable_files/png4.PNG)

# まとめ

## メソッド一覧

* `__init__`
    * pandas.Dataframeをインスタンス化
    * open, high, low, closeのカラムを持たないとエラー
    * indexがDatetimeIndexでなければエラー
* `resample`メソッド
    * `freq`引数で時間足を決める。
    * `stock_dataframe`を決める。
* `plot`メソッド
    * plot範囲(`plot_dataframe`)を決める。
        * `start_plot`
        * `end_plot`
        * `periods_plot`
    * view範囲を決める。
        * `start_view`
        * `end_view`
        * `periods_view`
    * グラフの右側の空白(shift)を決める。
        * `shift`
* `show`メソッド
    * 出力形式を決める。
        * `how='jupyter', 'html', 'png', 'jpeg', 'webp', 'svg'`
    * ファイル名を決める。
        * `filebasename`

## フローチャート
各メソッドの呼び出しに使う引数と戻り値、プロットに使うフローは以下の図の通りです。

![figure1](https://github.com/u1and0/stockplot/blob/master/note/candle_plot_movable/candle_plot_movable_files/figure1.PNG)



# 追記

__2017/4/21__
Qiitaに投稿しました。
[Plotlyでぐりぐり動かせる為替チャートを作る](http://qiita.com/u1and0/items/e2273bd8e03c670be45a)


__2017/4/22__
デイリーランキング4位に入りました。ありがとうございます^^
![daily_iine](https://github.com/u1and0/stockplot/blob/master/note/picture/daily_iine.PNG)
