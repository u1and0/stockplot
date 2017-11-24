
# coding: utf-8

# In[1]:


import sys
sys.path.append('../../bin/')
from stockplot import StockPlot
from read_hst import read_hst


# In[2]:


df = read_hst('/home/u1and0/Data/USDJPY.zip'); df.tail()


# In[3]:


fx = StockPlot(df)
fx.resample('D')


# In[5]:


fx.plot('heikin', start_plot=pd.Timestamp('20170101'), end_plot=pd.Timestamp('20171124'),
       start_view='first', end_view='last')
fx.show('jupyter')


# ![](heikin_files/ForexChart_USDJPY_2017_heikin)

# 微妙に違うのなんでだろう
# 平均足改良の余地あり
