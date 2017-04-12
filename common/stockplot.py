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

    # TODO
    * heikin_plot
    * pop, del
    * clear
    * subplot
    * 拡大縮小(足の数を決める)
    * 時間足の変更メソッド(インスタンス化する前、外で決めたほうが汎用性あるのかな)
    """

    def __init__(self, sdf: ss.StockDataFrame):
        self.StockDataFrame = sdf
        self._fig = FF.create_candlestick(self.StockDataFrame.open,
                                          self.StockDataFrame.high,
                                          self.StockDataFrame.low,
                                          self.StockDataFrame.close,
                                          dates=self.StockDataFrame.index)

    def candle_plot(self, filebasename='candlestick_and_trace', how='jupyter',
                    showgrid=True, validate=False):
        """Draw candle chart
        StockDataFrame must have [open, high, low, close] columns!

        USAGE:
            `sp.candle_plot()`"""
        self._fig['layout'].update(xaxis={'showgrid': showgrid})
        if how == 'jupyter':
            ax = pyo.iplot(self._fig, filename=filebasename + '.html',
                           validate=validate)  # for Jupyter Notebook
        elif how == 'html':
            ax = pyo.plot(self._fig, filename=filebasename + '.html',
                          validate=validate)  # for HTML
        else:  # Using png | jpeg | webp | svg
            ax = pyo.plot(self._fig, image=how, image_filename=filebasename,
                          validate=False)  # for file exporting
        return ax

    def append(self, indicator):
        """Add indicator designated by index (default is last appended one)
        from StockDataFrame & figure

        USAGE:
            `sp.append('close_25_sma')`
            add indicator of 'close 25 sma'
        """
        indi = self.StockDataFrame.get(indicator)
        plotter = go.Scatter(x=indi.index, y=indi,
                             name=indicator.upper().replace('_', ' '))  # グラフに追加する形式変換
        self._fig['data'].append(plotter)
        return indi

    def remove(self, indicator):
        """Remove indicator designated by 'index name'
        from StockDataFrame & figure

        USAGE:
            `sp.remove('close_25_sma')`
            remove indicator named 'close_25_sma'. """
        indi = indicator.lower().replace(' ', '_')
        INDI = indicator.upper().replace('_', ' ')
        rem = self.StockDataFrame.pop(indi)
        for dicc in self._fig['data']:
            if dicc['name'] == INDI:
                self._fig['data'].remove(dicc)
                return rem

    def pop(self, index=-1):
        """Remove indicator designated by 'index' (default is last appended one)
        from StockDataFrame & figure

        USAGE:
            * `sp.pop()`
            > remove indicator last appended.
            * `sp.pop(-2)`
            > remove indicator last 2 before appended.

        ISSUE:
            There are some indicator generate multi columns in StockDataFrame.
            The columns don't remove from StockDataFrame & figure by using pop method.

        SOLLUTION:
            Another attribute can be added for stock the columns key and index.
        """
        rem = self.StockDataFrame.pop(self.StockDataFrame.columns[index])
        self._fig['data'].pop(index)
        return rem


if __name__ == '__main__':
    # Make sample data
    np.random.seed(1)
    df = randomwalk(60 * 24 * 90, freq='T', tick=0.01,
                    start=pd.datetime(2017, 3, 20)).resample('B').ohlc() + 115  # 90日分の1分足を日足に直す

    # Convert DataFrame as StockDataFrame
    sdf = ss.StockDataFrame(df)

    # Convert StockDataFrame as StockPlot
    sp = StockPlot(sdf)

    # Add indicator
    for i in range(10, 17):
        sp.append('close_{}_sma'.format(i))

    # Remove indicator
    for i in [13, 11]:
        sp.remove('close_{}_sma'.format(i))

    # Pop indicator
    sp.pop()

    # # Plot Candle chart
    sp.candle_plot(how='html')