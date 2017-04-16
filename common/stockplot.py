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


def _append_graph(self, df):
    """
    for i in self._append_dataframe:
        self._fig.data.append(i)
    """
    pass


def _cut_frame(ts, start, end, cut=300):
    """
    start, endから両端に向かって数えて
    cutを超えたところまで数える
    ts: DatetimeIndex

    # TEST
    start, end = pd.datetime(2017,6,14), pd.datetime(2017,7,15)
    len(_cut_frame(df, start, end, cut=100))
    """
    assert len(ts) < cut, r'"cut" is too short or span between "start" & "end" is too wide'
    drawts = ts[ts.get_loc(start):ts.get_loc(end) + 1]  # 描かれるスパン
    cut -= len(drawts)  # 画面外の足の総数
    cut //= 2  # 右側、左側に必要な足の数
    tss = ts[:ts.get_loc(start)]  # startより前
    # tss.reverse()  # 逆順並び替え
    tse = ts[ts.get_loc(end) + 1:]  # endより後, 

    date_start= tss[-cut] if len(tss) > cut else tss[0]
    date_end= tse[cut] if len(tse) > cut else tse[-1]
    cut_start, cut_end = ts.get_loc(date_start), ts.get_loc(date_end)
    return ts[cut_start:cut_end]

    # if len(tse) < cut or len(tss) < cut:
    #     # less = min(len(tss), len(tse))  # 足りないほうの値
    #     # full = cut + less
    #     # Return longer list
    #     if len(tse)<len(tss):
    #         longer, shorter = tss. tse
    #         shorter_index = cut - len(shorter)
    #         longer_index = cut + shorter_index
    #         cut_end=tse[shorter_index]
    #         cut_start=tss[-longer_index]
    #     else: # longer,shorter = tse, tss
    #         longer, shorter = tse. tss
    #         shorter_index = cut - len(shorter)
    #         longer_index = cut + shorter_index
    #         cut_end=tse[-shorter_index]
    #         cut_start=tss[longer_index]

    #     else
    #     pass
    # else:
    #     cut_start = tss[-cut]
    #     cut_end = tse[cut]

    # remain = cut - max(len(tss), len(tse))

    # cut_start = start
    # cut_end = end
    # for start, end in zip(reverse_index, df.loc[end:].index):
    #     try:
    #         cut_start = start
    #         if len(df[cut_start:cut_end]) >= cut:  # cutの数を超えたら終了
    #             break
    #     except StopIteration as err:
    #         print(err)
    #         continue  # これじゃだめ
    #     try:
    #         cut_end = end
    #         print(cut_start, cut_end)
    #         if len(df[cut_start:cut_end]) >= cut:  # cutの数を超えたら終了
    #             break
    #     except StopIteration as err:
    #         print(err)
    #         continue  # これじゃだめ
    # return df.loc[cut_start: cut_end]


def to_unix_time(*dt: pd.datetime)->list:
    """datetimeをunix秒に変換
    引数: datetime(複数指定可能)
    戻り値: unix秒に直されたリスト"""
    epoch = pd.datetime.utcfromtimestamp(0)
    return [(i - epoch).total_seconds() * 1000 for i in dt]


class StockPlot:
    """StockDataFrameの可視化ツール

    # USAGE

    ## Convert DataFrame as StockDataFrame
    ## `df` is a pandas.DataFrame which has [open, high, low, close] columns.
    sdf = ss.StockDataFrame(df)

    # Convert StockDataFrame as StockPlot
    sp = StockPlot(sdf)

    ## Add indicator
    `sp.append('close_25_sma')`

    ## Remove indicator
    `sp.append('close_25_sma')`

    ## Plot candle chart
    `sp.candle_chart()`


    # What do i want do

    * StockDataFrameにプロット能力を持たせたい。
    * StockPlotの属性
        * StockDataFrame: 金融指標を取得しやすい改造pandas.DataFrame
        * _fig: plotlyのプロットデータ

    ```python
    df = randomwalk(60 * 24 * 90, freq='T', tick=0.01,
                    start=pd.datetime(2017, 3, 20)).resample('B').ohlc() + 115  # 90日分の1分足を日足に直す
    dfs = stockstats.StockDataFrame(df)
    dfs.add('hoge'): インジケーターの追加
    dfs.candle_plot(): キャンドルチャートとインジケータの表示
    dfs.remove('hoge'): インジケーターの削除
    ```

    # メソッド詳細
    * dfs.append('hoge')
        * dfs.get('hoge')を実行して、グラフに挿入するデータフレームを入手する
            > `indi = dfs.get('hoge')`
        * プロットするための形plotterに変換してやる
            > `plotter = go.Scatter(x=..., y=...) <- indiを使う`
        * plotterをStockPlotのattributeである`fig`に入れてやる
            > `fig['data'].append(plotter)`

    * dfs.candle_plot()
        * `fig = FF.create_candlestick... `でキャンドルチャートを取得できる
        * figに対してadd / remove_inidcatorで指標の追加 / 削除が行われる。
        * self_figを返す

    * dfs.show()
        * plt.show()に当たる

        ```python
        self._fig['layout'].update(xaxis={'showgrid': True})  # figのレイアウト調整をして
        pyo.plot(self._fig, filename=filename, validate=False)  # plotlyでhtmlとしてプロットする
        ```


    * `Base.df` is a dataframe. datafraemeの削除の仕方に従うこと
        * カラムの削除
            * `Base.df.pop(*'column_name'*)
            * `del Base.df[*'column_name'*]
            * `Base.df.drop(*'column_name'*. axis=1)`
    * `Base.add_line` is a list of graph line.pythonのリスト形式の削除の仕方に従うこと
        * 要素の削除
            * `Base.add_line.pop(*'index'*)`:
                 * `[x.add_line[i]['name'] for i in range(len(x.add_line)) ]`:
                    リスト内辞書のnameだけ抜き出せる
                 * x.add_iine.index('*name*')でなんとかならないかな
            * `del Base.add_line[*num1* : *num2*]`
            * list.removeは使えない。なぜなら、長い長いデータフレームのような辞書形式をリストに格納しているから、実用的には打ち込めない。
        * 初期化
            * `Base.add_line.clear(): clear関数
            * `del Base.add_line[:]`: すべての要素をdel
            * `Base.add_line = []`: 空のリストの代入

    # 指標の重複追加、追加削除の情報保存
        append, removeして残った指標を記憶
        追加したindicatorの情報をインスタンス変数に保持しておいて
        freq変えたり、session保存するときに、自動で追加してくれる機能

    # TODO
        * heikin_plot
        * pop, del
        * clear
        * subplot
        * 拡大縮小(足の数を決める)
        * 時間足の変更メソッド(インスタンス化する前、外で決めたほうが汎用性あるのかな)
    """

    def __init__(self, sdf: ss.StockDataFrame):
        co = ['open', 'high', 'low', 'close']
        assert all(i in sdf.columns for i in co), 'arg\'s columns is {}, but it is {}'\
            .format(co, sdf.columns)  # Arg Check
        self._init_StockDataFrame = sdf  # スパン変更前のデータフレーム
        self.StockDataFrame = None  # スパン変更後、インジケータ追加後のデータフレーム
        self._plot_dataframe = None  # プロットするデータ(ドラッグで行ける範囲)
        self._fig = None  # -> plotly.graph_objs
        self._append_indicator = []  # 追加された指標
        self._freq = None

    def ohlc_convert(self, freq: str)->ss.StockDataFrame:
        """ohlcデータのタイムスパンを変える
        引数:
            self: open. high, low, closeをカラムに持ち、
                indpdがdatetime型のpd.DataFrame
            freq: 変更したい期間(str型)
        戻り値: スパン変更後のデータフレーム
        """
        self._freq = freq
        self.StockDataFrame = self._init_StockDataFrame.ix[:, ['open', 'high', 'low', 'close']]\
            .resample(freq).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'}).dropna()
        return self.StockDataFrame

    def candle_plot(self, filebasename='candlestick_and_trace',
                    cut=300, fix=False, showgrid=True, validate=False, **kwargs):
        """Draw candle chart
        StockDataFrame must have [open, high, low, close] columns!

        USAGE:
            `sp.candle_plot()`

        fix: 時間軸右側の空白。fixの数の足分だけ空白
        cut: 画面外で切る足の数。Falseですべて表示。

        スパンの変更をされたself.StockDataFrameを_plot_dataframeに変える
        """
        # Append indicators in graph
        append_graph(self.StockDataFrame)

        # Converting _plot_dataframe from StockDataFrame
        cut_start, cut_end = _cut_frame(_plot_datafraeme)
        self._plot_dataframe = self.StockDataFrame.loc[cut_start:cut_end]

        # Adjust layout
        self._fig = FF.create_candlestick(self._plot_dataframe.open, self._plot_dataframe.high,
                                          self._plot_dataframe.low, self._plot_dataframe.close, dates=self._plot_dataframe.index)

        # グラフの表示範囲指定
        """spanの変更
        疲れた
        ユーザーにStockDataFrameの範囲と
        viewの範囲決めさせちゃダメかね
        sp.candle_plot(view_end=pd.datetime.today(), view_periods=10,
                                    end=pd.datetime.today(), periods=300)

        引数:
            sdf: indexがdatetimeのデータフレーム
            start, end: 最初と最後のdatetime, 'first'でsdfの最初、'last'でsdfの最後
            periods: datetimeの個数
            start, end, periods合わせて2つの引数が必要
            freq: M(onth) | W(eek) | D(ay) | H(our) | T(Minute) | S(econd)
        戻り値: datetime index

        # NOTE
        self._plot_dataframeのスパンを変える
        """
        # Args check
        count_not_none = sum(x is not None for x in [start, end, periods])
        if count_not_none != 2:  # Like a pd.date_range Error
            raise ValueError('Must specify two of start, end, or periods')

        # source = self.StockDataFrame.copy().ohlc_convert(freq)  # if freq else sdf.copy()
        start = self._plot_dataframe.index[0] if start == 'first' else start
        end = self._plot_dataframe.index[-1] if end == 'last' else end

        # start, end, periodsどれかが与えられていない場合
        if not periods:
            time_span = pd.date_range(start=start, end=end, freq=freq, tz=None,
                                      normalize=False, closed=None, **kwargs)
        elif not end:
            time_span = pd.date_range(start=start, periods=periods, freq=freq,
                                      tz=None, normalize=False, closed=None, **kwargs)
        elif not start:
            time_span = pd.date_range(end=end, periods=periods, freq=freq,
                                      tz=None, normalize=False, closed=None, **kwargs)
        start = time_span[0]
        end = time_span[-1]
        endfix = pd.date_range(start=end, periods=fix, freq=freq)[-1] if fix else end
        rangestart, rangeend = to_unix_time(start, endfix)

        # Plot graph
        self._fig['layout'].update(xaxis={'showgrid': showgrid, 'range': [rangestart, rangeend]},
                                   yaxis={"autorange": True})
        return self._fig

    def show(self, how='html'):
        # Export file type
        if how == 'html':
            ax = pyo.plot(self._fig, filename=filebasename + '.html',
                          validate=validate)  # for HTML
        elif how == 'jupyter':
            ax = pyo.iplot(self._fig, filename=filebasename + '.html',
                           validate=validate)  # for Jupyter Notebook
        elif how in ('png', 'jpeg', 'webp', 'svg'):
            ax = pyo.plot(self._fig, image=how, image_filename=filebasename,
                          validate=False)  # for file exporting
        else:
            raise KeyError(how)
        return ax


# ---------Doesn't work because of changing above----------
#     def append(self, indicator):
#         """Add indicator designated by index (default is last appended one)
#         from StockDataFrame & figure

#         USAGE:
#             `sp.append('close_25_sma')`
#             add indicator of 'close 25 sma'
#         """
#         indi = self.StockDataFrame.get(indicator)
#         plotter = go.Scatter(x=indi.index, y=indi,
#                              name=indicator.upper().replace('_', ' '))  # グラフに追加する形式変換
#         self._fig['data'].append(plotter)
#         return indi

#     def remove(self, indicator):
#         """Remove indicator designated by 'index name'
#         from StockDataFrame & figure

#         USAGE:
#             `sp.remove('close_25_sma')`
#             remove indicator named 'close_25_sma'. """
#         indi = indicator.lower().replace(' ', '_')
#         INDI = indicator.upper().replace('_', ' ')
#         rem = self.StockDataFrame.pop(indi)
#         for dicc in self._fig['data']:
#             if dicc['name'] == INDI:
#                 self._fig['data'].remove(dicc)
#                 return rem

#     def pop(self, index=-1):
#         """Remove indicator designated by 'index' (default is last appended one)
#         from StockDataFrame & figure

#         USAGE:
#             * `sp.pop()`
#             > remove indicator last appended.
#             * `sp.pop(-2)`
#             > remove indicator last 2 before appended.

#         ISSUE:
#             There are some indicator generate multi columns in StockDataFrame.
#             The columns don't remove from StockDataFrame & figure by using pop method.

#         SOLLUTION:
#             Another attribute can be added for stock the columns key and index.
#         """
#         rem = self.StockDataFrame.pop(self.StockDataFrame.columns[index])
#         self._fig['data'].pop(index)
#         return rem


# if __name__ == '__main__':
#     # Make sample data
#     np.random.seed(1)
#     df = randomwalk(60 * 24 * 90, freq='T', tick=0.01,
#                     start=pd.datetime(2017, 3, 20)).resample('B').ohlc() + 115  # 90日分の1分足を日足に直す

#     # Convert DataFrame as StockDataFrame
#     sdf = ss.StockDataFrame(df)

#     # Convert StockDataFrame as StockPlot
#     sp = StockPlot(sdf)

#     # Add indicator
#     for i in range(10, 17):
#         sp.append('close_{}_sma'.format(i))

#     # Remove indicator
#     for i in [13, 11]:
#         sp.remove('close_{}_sma'.format(i))

#     # Pop indicator
#     sp.pop()

#     # # Plot Candle chart
#     sp.candle_plot(how='html')
