#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from pandas.core import common as com
from pandas.core import resample
import stockstats as ss
from plotly import figure_factory as FF
import plotly.offline as pyo
import plotly.graph_objs as go
pyo.init_notebook_mode(connected=True)


def cleansing(df):
    """Columns must set OHLC(V)"""
    df.columns = map(lambda x: x.lower(), df.columns)  # columns -> lower case
    co = ['open', 'high', 'low', 'close']
    if not all(i in df.columns for i in co):  # Columns check
        raise KeyError("columns must have {} (, 'volume')], but it has {}".format(co, df.columns))
    df = df.loc[:, co + ['volume']].dropna(1)  # Extract OHLC (and Volume)
    return df


def heikin_ashi(self):
    """Return HEIKIN ASHI columns"""
    self['hopen'] = (self.open.shift() + self.close.shift()) / 2
    self['hclose'] = (self[['open', 'high', 'low', 'close']]).mean(1)
    self['hhigh'] = self[['high', 'hopen', 'hclose']].max(1)
    self['hlow'] = self[['low', 'hopen', 'hclose']].min(1)
    return self[['hopen', 'hhigh', 'hlow', 'hclose']]


pd.DataFrame.heikin_ashi = heikin_ashi


def ohlc2(self):
    """`pd.DataFrame.resample(<TimeFrame>).ohlc2()`
    Resample method converting OHLC to OHLC
    """
    agdict = {'open': 'first',
              'high': 'max',
              'low': 'min',
              'close': 'last'}
    columns = list(agdict.keys())
    if all(i in columns for i in self.columns):
        pass
    elif all(i in columns + ['volume'] for i in self.columns):
        agdict['volume'] = 'sum'
    else:
        raise KeyError("columns must have ['open', 'high', 'low', 'close'(, 'volume')]")
    return self.agg(agdict)


# Add instance as `pd.DataFrame.resample('<TimeFrame>').ohlc2()`
resample.DatetimeIndexResampler.ohlc2 = ohlc2


def reset_dataframe(df):
    """Reset dataframe as stockstats"""
    return ss.StockDataFrame(df.loc[:, ['open', 'high', 'low', 'close']])


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


def to_unix_time(*dt):
    """datetimeをunix秒に変換
    引数: datetime(複数指定可能)
    戻り値: unix秒に直されたイテレータ"""
    epoch = pd.datetime.fromtimestamp(0)
    return ((i - epoch).total_seconds() * 1000 for i in dt)


class StockPlot:
    """Plot candle chart using Plotly & StockDataFrame
    # USAGE

    ```
    # Convert StockDataFrame as StockPlot
    fx = StockPlot(sdf)

    # Add indicator
    fx.append('close_25_sma')

    # Remove indicator
    fx.append('close_25_sma')

    # Plot candle chart
    fx.plot()
    fx.show()
    ```

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

    # removeメソッドについて
    * `fx.df` is a dataframe. datafraemeの削除の仕方に従うこと
        * カラムの削除
            * `fx.df.pop(*'column_name'*)
            * `del fx.df[*'column_name'*]
            * `fx.df.drop(*'column_name'*. axis=1)`
    * `fx.add_line` is a list of graph line.pythonのリスト形式の削除の仕方に従うこと
        * 要素の削除
            * `fx.add_line.pop(*'index'*)`:
                 * `[x.add_line[i]['name'] for i in range(len(x.add_line)) ]`:
                    リスト内辞書のnameだけ抜き出せる
                 * x.add_iine.index('*name*')でなんとかならないかな
            * `del fx.add_line[*num1* : *num2*]`
            * list.removeは使えない。なぜなら、長い長いデータフレームのような辞書形式をリストに格納しているから、実用的には打ち込めない。
        * 初期化
            * `fx.add_line.clear(): clear関数
            * `del fx.add_line[:]`: すべての要素をdel
            * `fx.add_line = []`: 空のリストの代入

    # 指標の重複追加、追加削除の情報保存
        append, removeして残った指標を記憶
        追加したindicatorの情報をインスタンス変数に保持しておいて
        freq変えたり、session保存するときに、自動で追加してくれる機能

    # TODO
        * heikin_plot
        * pop, del
        * clear
        * subplot
    """

    def __init__(self, df: pd.core.frame.DataFrame, freq='D'):
        sdf = cleansing(df.copy())
        self._init_stock_dataframe = ss.StockDataFrame(sdf)  # スパン変更前のデータフレーム
        self.freq = freq  # 足の時間幅
        self._indicators = {}  # Plotするときに使う指標
        self.stock_dataframe = self.resample(freq)  # スパン変更後、インジケータ追加後のデータフレーム
        self._fig = None  # <-- plotly.graph_objs

    def resample(self, freq: str):
        """Convert ohlc time span

        Usage: `fx.resample('D')  # 日足に変換`

        * Args:  変更したい期間 M(onth) | W(eek) | D(ay) | H(our) | T(Minute) | S(econd)
        * Return: スパン変更後のデータフレーム
        """
        self.freq = freq
        df = self._init_stock_dataframe.resample(freq).ohlc2().dropna()
        self.stock_dataframe = ss.StockDataFrame(df)
        for indicator in self._indicators.keys():
            self.append(indicator)  # Re-append indicator in dataframe
        return self.stock_dataframe

    def plot(self, bar='candle', start_view=None, end_view=None, periods_view=None, shift=None,
             start_plot=None, end_plot=None, periods_plot=None,
             showgrid=True, validate=False, **kwargs):
        """Retrun plotly candle chart graph

        Usage: `fx.plot()`

        * Args:
            * bar: 'candle', 'c' -> candle_plot / 'heikin', 'h' -> heikin_ashi plot
            * start, end: 最初と最後のdatetime, 'first'でindexの最初、'last'でindexの最後
            * periods: 足の本数
            > **start, end, periods合わせて2つの引数が必要**
            * shift: shiftの本数の足だけ右側に空白
        * Return: グラフデータとレイアウト(plotly.graph_objs.graph_objs.Figure)
        """
        # ---------Set "plot_dataframe"----------
        # Default Args
        if com._count_not_none(start_plot,
                               end_plot, periods_plot) == 0:
            end_plot = 'last'
            periods_plot = 300
        try:
            # first/last
            start_plot = self.stock_dataframe.index[0] if start_plot == 'first' else start_plot
            end_plot = self.stock_dataframe.index[-1] if end_plot == 'last' else end_plot
        except AttributeError:
            raise AttributeError('{} Use `fx.resample(<TimeFrame>)` at first'
                                 .format(type(self.stock_dataframe)))
        # Set "plot_dataframe"
        start_plot, end_plot = set_span(start_plot, end_plot, periods_plot, self.freq)
        if bar in ('candle', 'c'):
            plot_dataframe = self.stock_dataframe.loc[start_plot:end_plot]
            self._fig = FF.create_candlestick(plot_dataframe.open,
                                              plot_dataframe.high,
                                              plot_dataframe.low,
                                              plot_dataframe.close,
                                              dates=plot_dataframe.index)
        elif bar in ('heikin', 'h'):
            self.stock_dataframe.heikin_ashi()
            plot_dataframe = self.stock_dataframe.loc[start_plot:end_plot]
            self._fig = FF.create_candlestick(plot_dataframe.hopen,
                                              plot_dataframe.hhigh,
                                              plot_dataframe.hlow,
                                              plot_dataframe.hclose,
                                              dates=plot_dataframe.index)
        else:
            raise KeyError('Use bar = "[c]andle" or "[h]eikin"')
        # ---------Append indicators----------
        for indicator in self._indicators.keys():
            self._append_graph(indicator, start_plot, end_plot)  # Re-append indicator in graph
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
        """Export file type

        Usage:
            * fx.show()  # Plot in HTML file
            * fx.show('jupyter')  # Plot in Jupyter Notebook
            * fx.show('png', filename='hoge')  # Plot as 'hoge.png' file
        """
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


# ---------Indicator----------
    def append(self, indicator):
        """Add indicator in self._indicators & self.stock_dataframe NOT self._fig.

        Usage:
            `sp.append('close_25_sma')`  # add indicator of 'close 25 sma'
        """
        indicator_value = self.stock_dataframe[indicator]
        self._indicators[indicator] = indicator_value
        return indicator_value

    def _append_graph(self, indicator, start, end):
        """Auxualy functon as plotting indicator.
        This function add indicator in self._fig.

        Usage:
            NONE
            Used in `plot` method
        """
        graph_value = self._indicators[indicator].loc[start:end]
        plotter = go.Scatter(x=graph_value.index, y=graph_value,
                             name=indicator.upper().replace('_', ' '))  # グラフに追加する形式変換
        self._fig['data'].append(plotter)

    def clear(self, hard=False):
        """Remove all indicators.
        Keep self.freq, self.stock_dataframe

        Usage:
            fx.clear()
            """
        self._fig = None  # <-- plotly.graph_objs
        self._indicators = {}
        if hard:
            self.stock_dataframe = None
            self.freq = None  # 足の時間幅
        else:
            self.stock_dataframe = reset_dataframe(self.stock_dataframe)

    def pop(self, indicator):
        """Remove indicator from StockDataFrame & figure

        Usage:
            `fx.remove('close_25_sma')`  # remove indicator named 'close_25_sma'.
        """
        popper = self._indicators.pop(indicator)
        self.stock_dataframe = reset_dataframe(self.stock_dataframe)
        for reindicator in self._indicators.keys():
            self.stock_dataframe.get(reindicator)
        return popper
