import numpy as np
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from randomwalk import *
import plotly as py
from plotly.offline import iplot
from plotly.tools import FigureFactory as FF
py.offline.init_notebook_mode(connected=True) 
# init_notebook_mode(connected=True) # Jupyter notebook用設定

def plotly_candle(df):
    """plotly でcandleチャート描く。
    今のところ時間足は日足のみ対応"""
    fig = FF.create_candlestick(df.open, df.high, df.low, df.close)

    xtick0 = (5-df.index[0].weekday())%5 #最初の月曜日のインデックス
    fig['layout'].update({
        'xaxis':{
            'showgrid': True,
            'ticktext': [x.strftime('%Y-%m-%d') for x in df.index][xtick0::5],
            'tickvals': np.arange(xtick0,len(df),5)
        }
    })
    py.offline.plot(fig)


if __name__ == '__main__':
    np.random.seed(1)
    df = randomwalk(60 * 24 * 30, freq='T', tick=0.01).resample('B').ohlc() + 115

    plotly_candle((df))

    """
    # 参考: http://qiita.com/toyolab/items/1b5d11b5d376bd542022

    fig = plt.figure()
    ax = plt.subplot()

    # candle
    ohlc = np.vstack((range(len(df)), df.values.T)).T  # x軸データを整数に
    mpf.candlestick_ohlc(ax, ohlc, width=0.8, colorup='r', colordown='b')

    # sma
    sma = df.close.rolling(5).mean()
    vstack = np.vstack((range(len(sma)), sma.values.T)).T  # x軸データを整数に
    ax.plot(vstack[:, 0], vstack[:, 1])

    xtick0 = (5 - sma.index[0].weekday()) % 5  # 最初の月曜日のインデックス

    plt.xticks(range(xtick0, len(sma), 5), [x.strftime('%Y-%m-%d') for x in sma.index][xtick0::5])
    ax.grid(True)  # グリッド表示
    ax.set_xlim(-1, len(sma))  # x軸の範囲
    fig.autofmt_xdate()  # x軸のオートフォーマット
    plt.show()
    """
