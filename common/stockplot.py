import pandas as pd
from pandas.core import common as com
import stockstats as ss
from plotly.tools import FigureFactory as FF
import plotly.offline as pyo
pyo.init_notebook_mode(connected=True)


def set_span(start=None, end=None, periods=None, freq='D'):
    """ 引数のstart, end, periodsに対して
    startとendの時間を返す。

    * start, end, periods合わせて2つの引数が指定されていなければエラー
    * start, endが指定されていたらそのまま返す
    * start, periodsが指定されていたら、endを計算する
    * end, periodsが指定されていたら、startを計算する
    """
    if com._count_not_none(start, end, periods) != 2:  # Like a pd.date_range Error
        raise ValueError('Must specify two of start, end, or periods')
    start = start if start else (pd.Period(end, freq) - periods).start_time
    end = end if end else (pd.Period(start, freq) + periods).start_time
    return start, end


def _append_graph(self, df):
    """
    for i in self._append_dataframe:
        self._fig.data.append(i)
    """
    pass


def to_unix_time(*dt: pd.datetime)->iter:
    """datetimeをunix秒に変換
    引数: datetime(複数指定可能)
    戻り値: unix秒に直されたリスト"""
    epoch = pd.datetime.utcfromtimestamp(0)
    return ((i - epoch).total_seconds() * 1000 for i in dt)


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
    dfs.plot(): キャンドルチャートとインジケータの表示
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

    * dfs.plot()
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

    def __init__(self, df: pd.core.frame.DataFrame):
        # Arg Check
        co = ['open', 'high', 'low', 'close']
        assert all(i in df.columns for i in co), 'arg\'s columns must have {}, but it has {}'\
            .format(co, df.columns)
        if not type(df.index) == pd.tseries.index.DatetimeIndex:
            raise TypeError(df.index)
        self._init_stock_dataframe = ss.StockDataFrame(df)  # スパン変更前のデータフレーム
        self.stock_dataframe = None  # スパン変更後、インジケータ追加後のデータフレーム
        self.freq = None  # 足の時間幅
        self._fig = None  # <-- plotly.graph_objs

    def ohlc_convert(self, freq: str)->ss.StockDataFrame:
        """Convert ohlc time span

        USAGE: `fx.ohlc_convert('D')  # 日足に変換`

        * Args:  変更したい期間(str型)
        * Return: スパン変更後のデータフレーム
        """
        self.freq = freq
        self.stock_dataframe = self._init_stock_dataframe.ix[:, ['open', 'high', 'low', 'close']]\
            .resample(freq).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})\
            .dropna()
        return self.stock_dataframe

    def plot(self, start_view=None, end_view=None, periods_view=None, shift=None,
             start_plot=None, end_plot=None, periods_plot=None,
             showgrid=True, validate=False, **kwargs):
        """Retrun plotly candle chart graph

        USAGE: `fx.plot()`

        * Args:
            * start, end: 最初と最後のdatetime, 'first'でindexの最初、'last'でindexの最後
            * periods: 足の本数
            > **start, end, periods合わせて2つの引数が必要**
            * freq: M(onth) | W(eek) | D(ay) | H(our) | T(Minute) | S(econd)
            * shift: shiftの本数の足だけ右側に空白
        * Return: グラフデータとレイアウト(plotly.graph_objs.graph_objs.Figure)
        """
        # ---------Set "plot_dataframe"----------
        # Default Args
        if com._count_not_none(start_plot,
                               end_plot, periods_plot) == 0:
            end_plot = 'last'
            periods_plot = 300
        # first/last
        start_plot = self.stock_dataframe.index[0] if start_plot == 'first' else start_plot
        end_plot = self.stock_dataframe.index[-1] if end_plot == 'last' else end_plot
        # Set "plot_dataframe"
        start_plot, end_plot = set_span(start_plot, end_plot, periods_plot, self.freq)
        plot_dataframe = self.stock_dataframe.loc[start_plot:end_plot]
        self._fig = FF.create_candlestick(plot_dataframe.open,
                                          plot_dataframe.high,
                                          plot_dataframe.low,
                                          plot_dataframe.close,
                                          dates=plot_dataframe.index)
        # ---------Set "view"----------
        # Default Args
        if com._count_not_none(start_view,
                               end_view, periods_view) == 0:
            end_view = 'last'
            periods_view = 50
        # first/last
        start_view = plot_dataframe.index[0] if start_view == 'first' else start_view
        end_view = plot_dataframe.index[-1] if end_view == 'last' else end_view
        # Set "view"
        start_view, end_view = set_span(start_view, end_view, periods_view, self.freq)
        end_view = set_span(start=end_view, periods=shift,
                            freq=self.freq)[-1] if shift else end_view
        view = list(to_unix_time(start_view, end_view))
        # ---------Plot graph----------
        self._fig['layout'].update(xaxis={'showgrid': showgrid, 'range': view},
                                   yaxis={"autorange": True})
        return self._fig

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


# ---------Doesn't work because of changing above----------
#     def append(self, indicator):
#         """Add indicator designated by index (default is last appended one)
#         from StockDataFrame & figure

#         USAGE:
#             `sp.append('close_25_sma')`
#             add indicator of 'close 25 sma'
#         """
#         indi = self.stock_dataframe.get(indicator)
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
#         rem = self.stock_dataframe.pop(indi)
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
#         rem = self.stock_dataframe.pop(self.stock_dataframe.columns[index])
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
#     sp.plot(how='html')
