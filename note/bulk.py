# Modules import
import pandas as pd
from plotly.tools import FigureFactory as FF
from plotly import tools
import plotly.offline as pyo
import plotly.graph_objs as go
pyo.init_notebook_mode(connected=True)

# Make sample data
from randomwalk import randomwalk

# Convert df as StockDataFrame
from stockstats import StockDataFrame

# StockPlot(sdf).candle_plot()はうまくいく
# StockPlot(sdf).add_indicator('hogehoge')はself.figが見当たらないって怒られる
# だってinitしてないんだもん
# initするとまた怒られる。詳細は以下


class StockPlot(StockDataFrame):

    # init持たせるとうまくいかない
    # hoge(self, sdf)で
    # エラーいっぱい
    # hoge(self)で
    # 一つしかいらないはずの変数が二つ与えらてますよ！
    # ってエラー出る
    # def __init__(self):
    #     self.fig = self.hoge()

    def hoge(self):
        return FF.create_candlestick(self.open, self.high, self.low, self.close, dates=self.index)

    def candle_plot(self):
        fig = self.hoge()
        fig.layout.update(xaxis={'showgrid': True})
        pyo.plot(fig, validate=False)
        return fig

    def add_indicator(self, indicator):
        indi = self.get(indicator)
        plotter = go.Scatter(x=indi.index, y=indi, name=indicator.upper().replace('_', ' '))
        self.fig['data'].append(plotter)
        # figを格納する場所が見当たらないんだよなぁ
        return indi

    # @staticmethod
    # def retype(value, index_column=None):
    #     """ if the input is a `DataFrame`, convert it to this class.
    #     :param index_column: the column that will be used as index,
    #                          default to `date`
    #     :param value: value to convert
    #     :return: this extended class
    #     """
    #     if index_column is None:
    #         index_column = 'date'

    #     if isinstance(value, StockDataFrame):
    #         # use all lower case for column name
    #         value.columns = map(lambda c: c.lower(), value.columns)

    #         if index_column in value.columns:
    #             value.set_index(index_column, inplace=True)
    #         value = StockDataFrame(value)
    #     return value


if __name__ == '__main__':
    df = randomwalk(60 * 24 * 90, freq='T', tick=0.01, start=pd.datetime(2017, 3, 20)
                    ).resample('B').ohlc() + 115  # 90日分の1分足を日足に直す
    dfs = StockDataFrame(df.copy())

    x = StockPlot(dfs)
