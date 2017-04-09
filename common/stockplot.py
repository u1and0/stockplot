import numpy as np
import pandas as pd
from randomwalk import *
from plotly.tools import FigureFactory as FF
from plotly import tools
import plotly.offline as pyo
import plotly.graph_objs as go
from stockstats import *
pyo.init_notebook_mode(connected=True)


# fig = tools.make_subplots(rows=2, cols=1, specs=[[{}], [{}]],
#                           shared_xaxes=True, shared_yaxes=True,
#                           vertical_spacing=0.001)
class StockPlot:
    """StockDataFrameの可視化ツール

    # なにがしたい

    * StockDataFrameにプロット能力を持たせたい。
    * プロット能力はStockDataFrameクラスにメソッドを付与してあげる。

    ```python
    df = randomwalk(60 * 24 * 90, freq='T', tick=0.01,
                    start=pd.datetime(2017, 3, 20)).resample('B').ohlc() + 115  # 90日分の1分足を日足に直す
    dfs = stockstats.StockDataFrame(df)
    dfs.add_indicator('hoge'): インジケーターの追加
    dfs.candle_plot(): キャンドルチャートとインジケータの表示
    dfs.remove_indicator('hoge'): インジケーターの削除
    ```

    # メソッド詳細
    * dfs.add_indicator('hoge')
        * dfs.get('hoge')を実行して、グラフに挿入するデータフレームを入手する
            > `indi = dfs.get('hoge')`
        * プロットするための形plotterに変換してやる
            > `plotter = go.Scatter(x=..., y=...) <- indiを使う`
        * plotterをStockPlotのattributeである`fig`に入れてやる
            > `fig['data'].append(plotter)`

    * dfs.candle_plot()
        * `fig = FF.create_candlestick... `でキャンドルチャートを取得できる
        * figに対してadd_indicator / remove_inidcatorで指標の追加 / 削除が行われる。

    * dfs.plot()
        * plt.show()に当たるのかな

        ```python
                self.fig['layout'].update(xaxis={'showgrid': True})  # figのレイアウト調整をして
                pyo.plot(self.fig, filename=filename, validate=False)  # plotlyでhtmlとしてプロットする
        ```

        別にdataframe的な操作は必要ないから、
        StockDataFrameのサブクラスになる必要はないので

        強いていうなら、StockDataFrameにfigという属性持たせて、
        plotlyとつなげたいから
        def __init()__をStockDataFrameにあてがってあげればいいのか
        StockDataFrame.__init__ = __init__
    """

    def __init__(self, df):
        self.StockDataFrame = StockDataFrame(df)
        self.fig = FF.create_candlestick(self.StockDataFrame.open, self.StockDataFrame.high,
                                         self.StockDataFrame.low, self.StockDataFrame.close, dates=self.StockDataFrame.index)

    # def ppplot(dfs, filename='candlestick_and_trace.html'):
    #     # trace1 = FF.create_candlestick(dfs.open, dfs.high,
    #     #                                dfs.low, dfs.close, dates=dfs.index)
    #     trace1 = go.Scatter(x=[0, 1, 2], y=[10, 11, 12])
    #     fig.append_trace(trace1, 1, 1)
    #     pyo.plot(fig, filename=filename, validate=False)

    def candle_plot(self, filename='candlestick_and_trace.html'):
        """StockDataFrameをキャンドルチャート化する
        引数: dfs: StockDataFrame
        戻り値: plotly plot"""
        self.fig['layout'].update(xaxis={'showgrid': True})
        pyo.plot(self.fig, filename=filename, validate=False)

    def add_indicator(self, indicator):
        indi = self.StockDataFrame.get(indicator)
        plotter = go.Scatter(x=indi.index, y=indi,
                             name=indicator.upper().replace('_', ' '))  # グラフに追加する形式変換
        self.fig['data'].append(plotter)
        return indi

    def remove_indicator(self, indicator):
        indi = indicator.lower().replace(' ', '_')
        INDI = indicator.upper().replace('_', ' ')
        self.StockDataFrame.pop(indi)
        for dicc in self.fig['data']:
            if dicc['name'] == INDI:
                self.fig['data'].remove(dicc)
                return dicc



if __name__ == '__main__':
    # Make sample data
    np.random.seed(1)
    df = randomwalk(60 * 24 * 90, freq='T', tick=0.01,
                    start=pd.datetime(2017, 3, 20)).resample('B').ohlc() + 115  # 90日分の1分足を日足に直す

    # Convert DataFrame as StockDataFrame
    dfs = StockPlot(df.copy())

    # Add indicator
    dfs.add_indicator('close_25_sma')
    dfs.add_indicator('close_25_ema')

    # Remove indicator
    dfs.remove_indicator('close_25_ema')

    # Plot Candle chart
    dfs.candle_plot()
