import numpy as np
import matplotlib.pyplot as plt
import matplotlib.finance as fin
import pandas as pd



def mydate(x,pos):
    try:
        return xdate[int(x)]
    except IndexError:
        return ''


def candlechart(ohlc, width=0.8):
    """入力されたデータフレームに対してローソク足チャートを返す
        引数:
            * ohlc: 
                *データフレーム
                * 列名に'open'", 'close', 'low', 'high'を入れること
                * 順不同"
            * widrh: ローソクの線幅 
        戻り値: ax: subplot"""
    fig, ax = plt.subplots()
    # ローソク足
    fin.candlestick2_ohlc(ax, opens=ohlc.open.values, closes=ohlc.close.values,
                         lows=ohlc.low.values, highs=ohlc.high.values,
                         width=width, colorup='r', colordown='b')
    
    # x軸を時間にする
    xdate = dfl.index
    ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))

    fig.autofmt_xdate()
    fig.tight_layout()

    return fig, ax

def randomwalk(periods, start=pd.datetime.today().date(), index=None, name=None, tick=1, freq='B'):
    """periods日分だけランダムウォークを返す"""
    if not index:
        index = pd.date_range(start=start, periods=periods, freq=freq)  # 今日の日付からperiod日分の平日
    bullbear = pd.Series(tick * np.random.randint(-1, 2, periods),
                         index=index, name=name)  # unit * (-1,0,1のどれか)を吐き出すSeries
    price = bullbear.cumsum()  # 累積和
    return price
