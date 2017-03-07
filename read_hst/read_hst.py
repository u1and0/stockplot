
# coding: utf-8

# # ヒストリカルデータの読み込み
# 

# In[6]:

get_ipython().magic('run hst_to_df.py  -f data/EURUSD.hst -ty old')


# In[1]:

df = pd.read_hdf('data/EURUSD.h5', key="main")
df


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


# In[ ]:

dfl.y


# In[71]:

import matplotlib.ticker as ticker
import datetime

fig, ax = plt.subplots()
fi.candlestick2_ohlc(ax, opens=dfl.values[:,['open']], closes=dfl.values[:,['close']],
                     lows=dfl.values[:,['low']], highs=dfl.values[:,['high']],
                     width=0.8, colorup='r', colordown='b')

xdate = dfl.index
ax.xaxis.set_major_locator(ticker.MaxNLocator(6))

def mydate(x,pos):
    try:
        return xdate[int(x)]
    except IndexError:
        return ''

ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))

fig.autofmt_xdate()
fig.tight_layout()


# In[61]:

ax


# In[49]:

dfl.index.astype(float)


# In[30]:

ax = plt.subplot()
# dfl['close'].plot()
fi.candlestick2_ohlc(ax, opens=dfl.values[:,0], closes=dfl.values[:,1],
                     lows=dfl.values[:,2], highs=dfl.values[:,3],
                     width=0.8, colorup='r', colordown='b')
tfl = dfl.index.values.astype(float)[::5]
plt.xticks(tfl, [x for x in tfl])


# In[41]:

tfl.astype('datetime64[D]')


# In[ ]:



