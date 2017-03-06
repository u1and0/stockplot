
# coding: utf-8

# In[6]:

get_ipython().magic('run hst_to_df.py  -f EURUSD/EURUSD.hst -ty old')


# In[8]:

df = pd.read_hdf('EURUSD/EURUSD.h5', key="main")


# In[16]:

df.ix[:,['close']].plot()


# In[ ]:



