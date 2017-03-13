
# coding: utf-8

# # ドルコスト平均法
# 1. 下がったら買い
# 2. 一定額を買う

# ## ランダムウォークのシリーズを作成

# In[198]:

n = 1000
bullbear = pd.Series(np.random.randint(-1, 2, n))
price = bullbear.cumsum()
price.index.name='DateTime'
price.plot()


# ## 前日より値が低かったら買い、高かったら見過ごし
# ドルコスト平均法の(1)

# In[199]:

position = np.zeros(len(se))  # seと同じ長さの配列を作成
for i in price.index[:-1]:
    if price[i+1] - price[i] < 0:  # 前日の値のほうが小さければ高ければ安くなっているということ
        position[i]=price[i]  # そのときのpriceで買い
position


# In[147]:

fig, ax = plt.subplots()
price.plot(ax=ax)
pd.DataFrame(position).cumsum().plot(ax=ax, secondary_y=True)  # ポジションのcumulative sumをプロット


# ### priceからbullbearの計算

# In[148]:

def p2b(price):
    return price.sub(price.shift(1), fill_value=0)


# In[149]:

np.array_equal(p2b(price), np.array(bullbear))


# `p2b`関数によってbullbearの計算が可能となった。

# ## 効率化
# 前日の値より低かった日の終値だけを収集する関数

# In[150]:

def dob(price):
    pos = np.zeros(len(price))  # priceと同じ長さの配列を作成
    for i in price.index[:-1]:
        if price[i+1]<price[i]:  # 前日の値より安ければ
            pos[i]=price[i]  # 買い
    return pos


# In[151]:

get_ipython().magic('timeit dob(price)')


# 最もシンプル

# In[152]:

get_ipython().magic('timeit [price[i] if price[i+1]<price[i] else 0 for i in price.index[:-1]]')


# 内包表記を用いても時間はあまり変わらない

# In[153]:

def dob2(price):
    pos = np.zeros(len(price))  # priceと同じ長さの配列を作成
    pos = [price[i] if price.sub(price.shift(1), fill_value=0)<0 else 0]  # 下がったら買い
    return pos


# In[154]:

price[np.array(bullbear)<0]  # bullbearが負の値になったところだけのpriceを収集


# In[155]:

def lowprice(price):
    """bullbearが負になったところだけのpriceを収集したpd.Seriesを返す"""
    return price[np.array(p2b(price))<0]


# In[156]:

get_ipython().magic('timeit lowprice(price)')


# pd.Serieesから直接引き出すので高速。10倍速を実現した

# ## 可視化

# In[157]:

price.head()


# In[162]:

low = lowprice(price)
ax = pd.DataFrame([price, low, low.cumsum()]).T.plot(grid=True, style=['-', '^', '.'], secondary_y=[False, False, True])


# In[165]:

low = lowprice(price)
df = pd.DataFrame([price, pd.Series(np.zeros_like(low)+min(price), index=low.index), low.cumsum()]).T
df.plot(grid=True, style=['-', '^', '.'], secondary_y=[False, False, True])


# ## 特定期間で買い
# 毎週毎週購入かけているとお金が大量に必要になってしまう。
# 
# そんなに大量のお給料をもらっていないのである程度制限する。
# 
# ある週に1回でも購入したら、その週は条件が来ても購入を控えようと思う。
# 
# つまり来週になるまで「購入」の行動を無視するわけだね。

# In[ ]:




# In[200]:

def randomwalk(periods, start=pd.datetime.today().date()):
    ts = pd.date_range(start=start, periods=periods)
    bullbear = pd.Series(np.random.randint(-1, 2, n), index=ts, name='DateTime')
    price = bullbear.cumsum()
    return price
price=randomwalk(1000)
price.plot()


# In[193]:

p2b(price)


# In[ ]:




# In[ ]:




# In[ ]:

freq = 5 

