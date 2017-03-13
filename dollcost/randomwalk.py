
# coding: utf-8

# # ドルコスト平均法
# 1. 下がったら買い
# 2. 一定額を買う

# ## ランダムウォークのシリーズを作成

# In[46]:

n = 1000
bullbear = pd.Series(np.random.randint(-1, 2, n))
price = bullbear.cumsum()
price.plot()


# ## 前日より値が低かったら買い、高かったら見過ごし
# ドルコスト平均法の(1)

# In[48]:

position = np.zeros(len(se))  # seと同じ長さの配列を作成
for i in price.index[:-1]:
    if price[i+1] - price[i] < 0:  # 前日の値のほうが小さければ高ければ安くなっているということ
        position[i]=price[i]  # そのときのpriceで買い
position


# In[50]:

fig, ax = plt.subplots()
price.plot(ax=ax)
pd.DataFrame(position).cumsum().plot(ax=ax, secondary_y=True)  # ポジションのcumulative sumをプロット


# ### priceからbullbearの計算

# In[80]:

def p2b(price):
    return price.sub(price.shift(1), fill_value=0)


# In[81]:

np.array_equal(p2b(price), np.array(bullbear))


# `p2b`関数によってbullbearの計算が可能となった。

# ## 効率化

# In[51]:

def dob(price):
    pos = np.zeros(len(price))  # priceと同じ長さの配列を作成
    for i in price.index[:-1]:
        if price[i+1]<price[i]:  # 前日の値より安ければ
            pos[i]=price[i]  # 買い
    return pos


# In[53]:

get_ipython().magic('timeit dob(price)')


# In[55]:

get_ipython().magic('timeit [price[i] if price[i+1]<price[i] else 0 for i in price.index[:-1]]')


# In[58]:

def dob2(price):
    pos = np.zeros(len(price))  # priceと同じ長さの配列を作成
    pos = [price[i] if price.sub(price.shift(1), fill_value=0)<0 else 0]  # 下がったら買い
    return pos


# In[88]:

price[np.array(bullbear)<0]


# In[60]:

dob2(price)


# In[41]:

pd.DataFrame([se.shift(1), se, se.sub(se.shift(1), fill_value=0), bullbear]).T


# In[27]:

se.shift(1).sub(se, fill_value=0)


# In[26]:

[se[i] if se.shift(1).sub(se, fill_value=0)>0 else 0 for i in se]


# In[12]:

pd.DataFrame([se.shift(1), se]).T


# ## 特定期間で買い

# In[9]:

freq = 5 

