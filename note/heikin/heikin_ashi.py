
# coding: utf-8

# 平均足を算出する
# 
# ```python
# def heikin_ashi(self):
#     """Return HEIKIN ASHI columns"""
#     self['hopen'] = (self.open.shift() + self.close.shift()) / 2
#     self['hclose'] = (self[['open', 'high', 'low', 'close']]).mean(1)
#     self['hhigh'] = self[['high', 'hopen', 'hclose']].max(1)
#     self['hlow'] = self[['low', 'hopen', 'hclose']].min(1)
#     return self[['hopen', 'hhigh', 'hlow', 'hclose']]
# 
# 
# pd.DataFrame.heikin_ashi = heikin_ashi
# ```

# In[19]:


import sys
sys.path.append('../../bin/')
from stockplot import StockPlot
from read_hst import read_hst


# In[20]:


df = read_hst('/home/u1and0/Data/USDJPY.zip'); df.tail()


# In[21]:


fx = StockPlot(df)
fx.resample('D')
fx.stock_dataframe.tail()


# In[22]:


start, end = pd.Timestamp('20170531'), pd.Timestamp('20170818')
fx.plot('heikin', start_plot=start, end_plot=end, start_view='first', end_view='last')
fx.show('jupyter')


# ![image.png](attachment:image.png)

# In[23]:


start, end = pd.Timestamp('20170123'), pd.Timestamp('20170404')
fx.plot('heikin', start_plot=start, end_plot=end, start_view='first', end_view='last')
fx.show('jupyter')


# ![image.png](attachment:image.png)

# 微妙に違うのなんでだろう
# 平均足改良の余地あり

# In[17]:


fx.stock_dataframe.ix[pd.Timestamp('20170214'), ['hopen', 'hhigh', 'hlow', 'hclose']]


# dailyfx.comのデータは
# 
# 2017/2/14
# 
# hopen    113.277
# 
# hhigh    114.501
# 
# hlow     113.274
# 
# hclose   113.933

# In[14]:


start, end = pd.Timestamp('20170123'), pd.Timestamp('20170404')
fx.plot(start_plot=start, end_plot=end, start_view='first', end_view='last')
fx.show('jupyter')


# ![image.png](attachment:image.png)

# In[18]:


fx.stock_dataframe.ix[pd.Timestamp('20170214'), ['open', 'high', 'low', 'close']]


# dailyfx.comのデータは
# 
# 2017/2/14
# 
# open 113.726
# 
# high 114.501
# 
# low 113.247
# 
# close 114.257

# ...スプレッドかな！（諦）
