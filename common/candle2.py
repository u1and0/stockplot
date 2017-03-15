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

xtick0 = (5 - sma.index[0].weekday()) % 5  # 最初の月曜日のインデックス

plt.xticks(range(xtick0, len(sma), 5), [x.strftime('%Y-%m-%d') for x in sma.index][xtick0::5])
ax.grid(True)  # グリッド表示
ax.set_xlim(-1, len(sma))  # x軸の範囲
fig.autofmt_xdate()  # x軸のオートフォーマット
plt.show()
