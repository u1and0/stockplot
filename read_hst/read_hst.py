
# coding: utf-8

# # ヒストリカルデータの読み込み

# ## ヒストリカルデータの扱い方
# * [FXDD - メタトレーダのヒストリカルデータ](http://www.fxdd.com/bm/jp/forex-resources/forex-trading-tools/metatrader-1-minute-data/)よりzipファイルをダウンロード。
# * 解凍して.hstを取り出す。
# * 以下の`hst_to_df.py`に食べさせると.h5ファイルのうんこを出す。

# In[6]:

get_ipython().magic('run hst_to_df.py  -f data/EURUSD.hst -ty old')


# ## hdfファイル(.h5)の扱い

# In[1]:

df = pd.read_hdf('data/EURUSD.h5', key="main")
df


# ## 日足に圧縮する

# open, high, low, closeだけにして、
# resampleで指定した期間だけデータを丸める
# 
# 休日はbfill()かdropna()でなくす

# In[2]:

dff = df.ix[:, :4].resample('d').agg({'open':'first',
                                      'high':'max',
                                      'low':'min',
                                      'close':'last'}).dropna()
dff


# ## 最新100日、約3か月分のプロット

# In[3]:

dfl = dff[-100:]
dfl.plot()


# # ローソク足のプロット

# In[4]:

import matplotlib.finance as fi


# In[69]:

dfl


# 各列をnp.arrayで取り出すには、ドットで列名綴って、valuesメソッドで取り出す。
# 
# ixなどで列番号を使って取り出す時と比べて、列の入れ替え問題が解消される。

# In[87]:

dfl.open.values


# In[103]:

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
    fi.candlestick2_ohlc(ax, opens=ohlc.open.values, closes=ohlc.close.values,
                         lows=ohlc.low.values, highs=ohlc.high.values,
                         width=width, colorup='r', colordown='b')
    
    # x軸を時間にする
    xdate = dfl.index
    ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))

    fig.autofmt_xdate()
    fig.tight_layout()

    return fig, ax


# In[105]:

candlechart(dfl)


# In[ ]:



