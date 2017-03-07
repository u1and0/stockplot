
# coding: utf-8

# In[6]:

get_ipython().magic('run hst_to_df.py  -f EURUSD/EURUSD.hst -ty old')


# In[46]:

df = pd.read_hdf('EURUSD/EURUSD.h5', key="main")
df


# open, high, low, closeだけにして、
# resampleで指定した期間だけデータを丸める
# 
# 休日はbfill()かdropna()でなくす

# In[63]:

dff = df.ix[:, :4].resample('d').agg({'open':'first',
                                      'high':'max',
                                      'low':'min',
                                      'close':'last'}).dropna()
dff


# 最新100日、約3か月分のプロット

# In[64]:

dfl = dff[-100:]
dfl.plot()


# In[65]:

import matplotlib.finance as fi


# In[85]:

ax = plt.subplot()
fi.candlestick2_ohlc(ax, opens=dfl.values[:,0], closes=dfl.values[:,1],
                     lows=dfl.values[:,2], highs=dfl.values[:,3],
                     width=0.8, colorup='r', colordown='b')


# In[ ]:



