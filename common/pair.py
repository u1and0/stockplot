
# coding: utf-8

# In[174]:

import candlechart as c


# In[172]:

# 10秒間のtickチャート
c.randomwalk(10, tick=0.01, freq='S')


# In[99]:

# 5日間のtickチャート
time = 60 * 60 * 24 * 30  # 秒数
init_value = 115
tick = c.randomwalk(time, tick=0.001, freq='S') + init_value


# In[102]:

chart = tick.resample('B').ohlc()
chart.head()


# In[173]:

c.candlechart(chart)
# plt.xlim([pd.Timestamp('20170314'), pd.Timestamp('20170414')])


# In[128]:

sma5 = chart.close.rolling(5).mean()
sma5


# In[165]:

fig, ax = c.candlechart(chart)

# fig.plot(sma5)
# ax = plt.gca()
# ax.plot(sma5)
# sma5.plot(ax=ax.append())


# In[167]:




# In[168]:

sma5.plot(xticks=ax.get_xticklabels())


# In[137]:

# c.candlechart(chart)
get_ipython().magic('pinfo ax.get_axes')


# In[149]:

fig


# In[141]:

fig
# sma5.plot()


# In[ ]:



