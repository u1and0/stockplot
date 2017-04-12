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


class StockPlot:
    """StockDataFrameの可視化ツール

    # なにがしたい

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
    * dfs.add('hoge')
        * dfs.get('hoge')を実行して、グラフに挿入するデータフレームを入手する
            > `indi = dfs.get('hoge')`
        * プロットするための形plotterに変換してやる
            > `plotter = go.Scatter(x=..., y=...) <- indiを使う`
        * plotterをStockPlotのattributeである`fig`に入れてやる
            > `fig['data'].append(plotter)`

    * dfs.candle_plot()
        * `fig = FF.create_candlestick... `でキャンドルチャートを取得できる
        * figに対してadd / remove_inidcatorで指標の追加 / 削除が行われる。

    * dfs.plot()
        * plt.show()に当たるのかな

        ```python
                self._fig['layout'].update(xaxis={'showgrid': True})  # figのレイアウト調整をして
                pyo.plot(self._fig, filename=filename, validate=False)  # plotlyでhtmlとしてプロットする
        ```

    # TODO
    * heikin_plot
    * pop
    * subplot

    """

    def __init__(self, sdf: ss.StockDataFrame):
        self.StockDataFrame = sdf
        self._fig = FF.create_candlestick(self.StockDataFrame.open,
                                         self.StockDataFrame.high,
                                         self.StockDataFrame.low,
                                         self.StockDataFrame.close,
                                         dates=self.StockDataFrame.index)

    def candle_plot(self, filebasename='candlestick_and_trace'):
        """StockDataFrameをキャンドルチャート化する
        引数: dfs: StockDataFrame
        戻り値: plotly plot"""
        self._fig['layout'].update(xaxis={'showgrid': True})
        ax = pyo.iplot(self._fig, filename=filebasename + '.html', validate=False)
        # pyo.plot(self._fig, image='png', image_filename=filebasename, validate=False)
        return ax

    def append(self, indicator):
        indi = self.StockDataFrame.get(indicator)
        plotter = go.Scatter(x=indi.index, y=indi,
                             name=indicator.upper().replace('_', ' '))  # グラフに追加する形式変換
        self._fig['data'].append(plotter)
        return indi

    def remove(self, indicator):
        indi = indicator.lower().replace(' ', '_')
        INDI = indicator.upper().replace('_', ' ')
        rem = self.StockDataFrame.pop(indi)
        for dicc in self._fig['data']:
            if dicc['name'] == INDI:
                self._fig['data'].remove(dicc)
                return rem


if __name__ == '__main__':
    # Make sample data
    np.random.seed(1)
    df = randomwalk(60 * 24 * 90, freq='T', tick=0.01,
                    start=pd.datetime(2017, 3, 20)).resample('B').ohlc() + 115  # 90日分の1分足を日足に直す

    # Convert DataFrame as StockDataFrame
    sdf = ss.StockDataFrame(df)

    # Convert StockDataFrame as StockPlot
    x = StockPlot(sdf)

    # # Add indicator
    for i in range(10, 14):
        x.add('close_{}_sma'.format(i))

    # # Remove indicator
    for i in (10, 12):
        x.remove('close_{}_sma'.format(i))

    # # Plot Candle chart
    x.candle_plot()
