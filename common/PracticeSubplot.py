
# coding: utf-8

# # matplotlib.financeでローソク足

# In[1]:

import matplotlib.finance as mpf


# In[ ]:

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
    xdate = ohlc.index
    ax.xaxis.set_major_locator(ticker.MaxNLocator(6))

    def mydate(x, pos):
        try:
            return xdate[int(x)]
        except IndexError:
            return ''

    # ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')

    fig.autofmt_xdate()
    fig.tight_layout()

    return fig, ax


# In[6]:

from randomwalk import *


# In[27]:

df = randomwalk(60*24*30, freq='T', tick=0.01).resample('B').ohlc() + 115
df.head()


# In[18]:

# 参考: http://qiita.com/toyolab/items/1b5d11b5d376bd542022

fig = plt.figure()
ax = plt.subplot()

ohlc = np.vstack((range(len(df)), df.values.T)).T #x軸データを整数に
mpf.candlestick_ohlc(ax, ohlc, width=0.8, colorup='r', colordown='b')

xtick0 = (5-df.index[0].weekday())%5 #最初の月曜日のインデックス

plt.xticks(range(xtick0,len(df),5), [x.strftime('%Y-%m-%d') for x in df.index][xtick0::5])
ax.grid(True) #グリッド表示
ax.set_xlim(-1, len(df)) #x軸の範囲
fig.autofmt_xdate() #x軸のオートフォーマット


# In[7]:

# 参考: http://qiita.com/toyolab/items/1b5d11b5d376bd542022
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from randomwalk import *


df = randomwalk(60 * 24 * 30, freq='T', tick=0.01).resample('B').ohlc() + 115

fig = plt.figure()
ax = plt.subplot()

# candle
ohlc = np.vstack((range(len(df)), df.values.T)).T  # x軸データを整数に
mpf.candlestick_ohlc(ax, ohlc, width=0.8, colorup='r', colordown='b')

# sma
sma = df.close.rolling(5).mean()
vstack = np.vstack((range(len(sma)), sma.values.T)).T  # x軸データを整数に
ax.plot(vstack[:, 0], vstack[:, 1])

# xticks
xtick0 = (5 - df.index[0].weekday()) % 5  # 最初の月曜日のインデックス
plt.xticks(range(xtick0, len(df), 5), [x.strftime('%Y-%m-%d') for x in df.index][xtick0::5])
ax.grid(True)  # グリッド表示
ax.set_xlim(-1, len(df))  # x軸の範囲
fig.autofmt_xdate()  # x軸のオートフォーマット
plt.show()


# In[17]:

# 参考: http://qiita.com/toyolab/items/1b5d11b5d376bd542022
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from randomwalk import *


def sma(ohlc, period):
    sma = ohlc.close.rolling(period).mean()
    vstack = np.vstack((range(len(sma)), sma.values.T)).T  # x軸データを整数に
    return vstack


df = randomwalk(60 * 24 * 60, freq='T', tick=0.01).resample('B').ohlc() + 115

fig = plt.figure()
ax = plt.subplot()

# candle
ohlc = np.vstack((range(len(df)), df.values.T)).T  # x軸データを整数に
mpf.candlestick_ohlc(ax, ohlc, width=0.8, colorup='r', colordown='b')

# sma
sma5 = sma(df, 5)
sma25 = sma(df, 25)
ax.plot(sma5[:, 0], sma5[:, 1])
ax.plot(sma25[:, 0], sma25[:, 1])


# xticks
xtick0 = (5 - df.index[0].weekday()) % 5  # 最初の月曜日のインデックス
plt.xticks(range(xtick0, len(df), 5), [x.strftime('%Y-%m-%d') for x in df.index][xtick0::5])
ax.grid(True)  # グリッド表示
ax.set_xlim(-1, len(df))  # x軸の範囲
fig.autofmt_xdate()  # x軸のオートフォーマット
plt.show()


# # plotlyでローソク足

# ## plotlyの練習
# 参考: [Qiita - [Python] Plotlyでぐりぐり動かせるグラフを作る
# ](http://qiita.com/inoory/items/12028af62018bf367722)

# In[49]:

import plotly as py
py.offline.init_notebook_mode(connected=False) 


# In[47]:

fo = [[2000,1190547,1.36],
    [2001,1170662,1.33],
    [2002,1153855,1.32],
    [2003,1123610,1.29],
    [2004,1110721,1.29],
    [2005,1062530,1.26],
    [2006,1092674,1.32],
    [2007,1089818,1.34],
    [2008,1091156,1.37],
    [2009,1070035,1.37],
    [2010,1071304,1.39],
    [2011,1050806,1.39],
    [2012,1037101,1.41],
    [2013,1029816,1.43],
    [2014,1003532,1.42],
    [2015,1005656,1.46]]
raw = pd.DataFrame(fo, columns=['year', 'births', 'birth rate'])
raw


# In[50]:

data = [
    py.graph_objs.Scatter(y=raw["births"], name="births"),
]
layout = py.graph_objs.Layout(
    title="title",
    legend={"x":0.8, "y":0.1},
    xaxis={"title":""},
    yaxis={"title":""},
)
fig = py.graph_objs.Figure(data=data, layout=layout)
py.offline.iplot(fig, show_link=False)


# In[48]:

data = [
    py.graph_objs.Bar(x=raw["year"], y=raw["births"], name="Births"),
    py.graph_objs.Scatter(x=raw["year"], y=raw["birth rate"], name="Birth Rate", yaxis="y2")
]
layout = py.graph_objs.Layout(
    title="Births and Birth Rate in Japan",
    legend={"x":0.8, "y":0.1},
    xaxis={"title":"Year"},
    yaxis={"title":"Births"},
    yaxis2={"title":"Birth Rate", "overlaying":"y", "side":"right"},
)
fig = py.graph_objs.Figure(data=data, layout=layout)
py.offline.iplot(fig)
#py.offline.plot(fig)


# ## 為替チャート

# In[55]:

from plotly.offline import init_notebook_mode, iplot
from plotly.tools import FigureFactory as FF
init_notebook_mode(connected=True) # Jupyter notebook用設定


# In[56]:

fig = FF.create_candlestick(df.open, df.high, df.low, df.close)

xtick0 = (5-df.index[0].weekday())%5 #最初の月曜日のインデックス
fig['layout'].update({
    'xaxis':{
        'showgrid': True,
        'ticktext': [x.strftime('%Y-%m-%d') for x in df.index][xtick0::5],
        'tickvals': np.arange(xtick0,len(df),5)
    }
})

py.offline.iplot(fig)


# In[ ]:



