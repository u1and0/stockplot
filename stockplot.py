#!/usr/bin/env python
# -*- coding: utf-8 -*-
import stockstats as ss
import numpy as np
import pandas as pd
from pandas.core import common as com
from pandas.core import resample
from plotly import figure_factory as FF
import plotly.offline as pyo
import plotly.graph_objs as go
from .randomwalk import randomwalk
pyo.init_notebook_mode(connected=True)


def datagen(random_state=1, n=100, volume=False):
    """Generate sample OHLC data"""
    np.random.seed(random_state)
    df = randomwalk(60 * 60 * 24 * n, freq='S', tick=0.01, start=pd.datetime(2017, 1, 1))\
        .resample('T').ohlc() + 115  # 100日分の1分足, 初期値が115
    if volume:
        df['volume'] = np.random.randint(1000, 10000, len(df))
    return df


def cleansing(df):
    """Columns must set OHLC(V)"""
    df.columns = [_.lower() for _ in df.columns]  # columns -> lower case
    co = ['open', 'high', 'low', 'close']
    if not all(i in df.columns for i in co):  # Columns check
        raise KeyError(
            "columns must have {} (, 'volume')], but it has {}".format(
                co, df.columns))
    # Extract OHLC (and Volume)
    df = df.reindex(columns=co + ['volume']).dropna(1)
    return df


def _ohlcv(columns, open=None, high=None, low=None, close=None, volume=None):
    # `auto_dict` is lower case of columns
    auto_dict = {str(v).lower(): v for v in columns}
    # User defined OHLCV
    my_dict = {
        'open': open,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    }
    # Remove `None` values in `my_dict`
    updater = {k: v for k, v in my_dict.items() if v}
    auto_dict.update(updater)
    return auto_dict


def heikin_ashi(self, open=None, high=None, low=None, close=None):
    """Return HEIKIN ASHI columns"""
    df = self.copy()
    auto_dict = _ohlcv(df.columns, open, high, low, close)
    df['hopen'] = (
        df[auto_dict['open']].shift() + df[auto_dict['close']].shift()) / 2
    df['hclose'] = df[[
        auto_dict['open'], auto_dict['high'], auto_dict['low'],
        auto_dict['close']
    ]].mean(1)
    df['hhigh'] = df[[auto_dict['high'], 'hopen', 'hclose']].max(1)
    df['hlow'] = df[[auto_dict['low'], 'hopen', 'hclose']].min(1)
    heikin_df = df[['hopen', 'hhigh', 'hlow', 'hclose']]
    heikin_df.rename(
        {
            'hopen': 'open',
            'hhigh': 'high',
            'hlow': 'low',
            'hclose': 'close'
        },
        axis='columns',
        inplace=True)
    return heikin_df


pd.DataFrame.heikin_ashi = heikin_ashi


def ohlc2(self, open=None, high=None, low=None, close=None, volume=None):
    """`pd.DataFrame.resample(<TimeFrame>).ohlc2()`
    Resample method converting OHLC to OHLC
    """
    auto_dict = _ohlcv(self.mean().columns, open, high, low, close, volume)
    # Make dict as `agdict` for `df.resample(<Time>).agg(<dict>)`
    try:
        agdict = {
            auto_dict['open']: 'first',
            auto_dict['high']: 'max',
            auto_dict['low']: 'min',
            auto_dict['close']: 'last'
        }
    except KeyError as e:
        raise KeyError('Columns not enough {}'.format(*e.args))
    # Add `volume` columns
    if 'volume' in auto_dict:
        agdict[auto_dict['volume']] = 'sum'
    return self.agg(agdict)


# Add instance as `pd.DataFrame.resample('<TimeFrame>').ohlc2()`
resample.DatetimeIndexResampler.ohlc2 = ohlc2


def reset_dataframe(df):
    """Reset dataframe as stockstats"""
    return ss.StockDataFrame(df.loc[:, ['open', 'high', 'low', 'close']])


def set_span(start=None, end=None, periods=None, freq=None):
    """ 引数のstart, end, periodsに対して
    startとendの時間を返す。

    * start, end, periods合わせて2つの引数が指定されていなければエラー
    * start, endが指定されていたらそのまま返す
    * start, periodsが指定されていたら、endを計算する
    * end, periodsが指定されていたら、startを計算する
    """
    if com._count_not_none(start, end,
                           periods) != 2:  # Like a pd.date_range Error
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
    # 90日分の1分足を日足に直す
    df = randomwalk(60 * 24 * 90, freq='T', tick=0.01,
                    start=pd.datetime(2017, 3, 20)).resample('B').ohlc() + 115
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
            * list.removeは使えない。
            * なぜなら、長い長いデータフレームのような辞書形式をリストに格納している
            * だから、実用的には打ち込めない。
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
        self._init_data = ss.StockDataFrame(sdf)  # スパン変更前のデータフレーム
        self.freq = freq  # 足の時間幅
        self._indicators = {}  # Plotするときに使う指標
        self.data = self.resample(freq)  # スパン変更後、インジケータ追加後のデータフレーム
        self._fig = None  # <-- plotly.graph_objs

    def resample(self, freq: str):
        """Convert ohlc time span

        Usage: `fx.resample('D')  # 日足に変換`

        Args:  変更したい期間
            M(onth) | W(eek) | D(ay) | H(our) | T(Minute) | S(econd)

        Return: スパン変更後のデータフレーム
        """
        self.freq = freq
        df = self._init_data.resample(freq).ohlc2().dropna()
        self.data = ss.StockDataFrame(df)
        for indicator in self._indicators.keys():
            self.append(indicator)  # Re-append indicator in dataframe
        return self.data

    def plot(self,
             bar='candle',
             start_view=None,
             end_view=None,
             periods_view=None,
             shift=None,
             start_plot=None,
             end_plot=None,
             periods_plot=None,
             showgrid=True,
             validate=False,
             how='note',
             filebasename='candlestick_and_trace',
             **kwargs):
        """Retrun plotly candle chart graph
        Usage:
            * fx.plot(how='note')  # Plot in Jupyter Notebook (default)
            * fx.plot(how='html')  # Plot in HTML file
            * fx.plot(how='png', filename='hoge')  # Plot as 'hoge.png' file
        * Args:
            * bar:
                'candle', 'c' -> candle_plot
                'heikin', 'h' -> heikin_ashi plot
            * start, end: 最初と最後のdatetime, 'first'でindexの最初、'last'でindexの最後
            * periods: 足の本数
            > **start, end, periods合わせて2つの引数が必要**
            * shift: shiftの本数の足だけ右側に空白
            * how: jupyter notebook, html, png形式などを選択
        * Return: グラフデータとレイアウト(plotly.graph_objs.graph_objs.Figure)
        """
        # ---------Set "plot_dataframe"----------
        # Default Args
        if com._count_not_none(start_plot, end_plot, periods_plot) == 0:
            end_plot = 'last'
            periods_plot = 300
        try:
            # first/last
            start_plot = self.data.index[
                0] if start_plot == 'first' else start_plot
            end_plot = self.data.index[-1] if end_plot == 'last' else end_plot
        except AttributeError:
            raise AttributeError('{} Use `fx.resample(<TimeFrame>)` at first'
                                 .format(type(self.data)))
        # Set "plot_dataframe"
        start_plot, end_plot = set_span(start_plot, end_plot, periods_plot,
                                        self.freq)
        if bar in ('candle', 'c'):
            plot_dataframe = self.data.loc[start_plot:end_plot]
            self._fig = FF.create_candlestick(
                plot_dataframe.open,
                plot_dataframe.high,
                plot_dataframe.low,
                plot_dataframe.close,
                dates=plot_dataframe.index)
        elif bar in ('heikin', 'h'):
            self.data.heikin_ashi()
            plot_dataframe = self.data.loc[start_plot:end_plot]
            self._fig = FF.create_candlestick(
                plot_dataframe.hopen,
                plot_dataframe.hhigh,
                plot_dataframe.hlow,
                plot_dataframe.hclose,
                dates=plot_dataframe.index)
        else:
            raise KeyError('Use bar = "[c]andle" or "[h]eikin"')
        # ---------Append indicators----------
        # Re-append indicator in graph
        for indicator in self._indicators.keys():
            self._append_graph(indicator, start_plot, end_plot)
        # ---------Set "view"----------
        # Default Args
        if com._count_not_none(start_view, end_view, periods_view) == 0:
            end_view = 'last'
            periods_view = 50
        # first/last
        start_view = plot_dataframe.index[
            0] if start_view == 'first' else start_view
        end_view = plot_dataframe.index[-1] if end_view == 'last' else end_view
        # Set "view"
        start_view, end_view = set_span(start_view, end_view, periods_view,
                                        self.freq)
        end_view = set_span(
            start=end_view, periods=shift,
            freq=self.freq)[-1] if shift else end_view
        view = list(to_unix_time(start_view, end_view))
        # ---------Plot graph----------
        self._fig['layout'].update(
            xaxis={
                'showgrid': showgrid,
                'range': view
            },
            yaxis={"autorange": True})
        # ---------Select graph type----------
        if how == 'note':
            pyo.iplot(
                self._fig, filename=filebasename + '.html',
                validate=False)  # for Jupyter Notebook
        elif how == 'html':
            ax = pyo.plot(
                self._fig, filename=filebasename + '.html',
                validate=False)  # for HTML
        elif how in ('png', 'jpeg', 'webp', 'svg'):
            ax = pyo.plot(
                self._fig,
                image=how,
                image_filename=filebasename,
                validate=False)  # for file exporting
        else:
            raise KeyError(how)
        return ax


# ---------Indicator----------

    def append(self, indicator):
        """Add indicator in self._indicators & self.data NOT self._fig.

        Usage:
            `sp.append('close_25_sma')`  # add indicator of 'close 25 sma'
        """
        indicator_value = self.data[indicator]
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
        plotter = go.Scatter(
            x=graph_value.index,
            y=graph_value,
            name=indicator.upper().replace('_', ' '))  # グラフに追加する形式変換
        self._fig['data'].append(plotter)

    def clear(self, hard=False):
        """Remove all indicators.
        Keep self.freq, self.data

        Usage:
            fx.clear()
        """
        self._fig = None  # <-- plotly.graph_objs
        self._indicators = {}
        if hard:
            self.data = None
            self.freq = None  # 足の時間幅
        else:
            self.data = reset_dataframe(self.data)

    def pop(self, indicator):
        """Remove indicator from StockDataFrame & figure

        Usage:
            # remove indicator named 'close_25_sma'
            `fx.remove('close_25_sma')`
        """
        popper = self._indicators.pop(indicator)
        self.data = reset_dataframe(self.data)
        for reindicator in self._indicators.keys():
            self.data.get(reindicator)
        return popper
