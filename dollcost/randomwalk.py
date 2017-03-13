
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


# ## 一定金額を買い
# ドルコスト平均法の(2)

# In[256]:

def randomwalk(periods, start=pd.datetime.today().date(), name=None):
    """periods日分だけランダムウォークを返す"""
    ts = pd.date_range(start=start, periods=periods, freq='B')
    bullbear = pd.Series(np.random.randint(-1, 2, periods), index=ts, name=name)
    price = bullbear.cumsum()
    return price
price=randomwalk(100) + 100  # 100は初期値
price.plot()


# ランダムウォークによる価格変動を再定義。
# 関数化してみた。

# * 縦軸が単位[円]だとする
# * 例えば10000円ずつ買っていくとする
# * 口数はint型

# In[257]:

unit_cost = 10000
ticket = unit_cost / price[0]
ticket, int(ticket)


# 0インデックス目

# In[263]:

tickets = unit_cost / price
pd.DataFrame([price, tickets, tickets.astype(int)],
             index=['price', 'ticket(float)', 'ticket(int)']).T


# 全期間に適用。
# 
# 切り捨てすると時は`astype(int)`メソッドを使う。

# In[264]:

def dollcost(price, unit_cost):
    """
    引数: 
        price: 価格変動値
        unit_cost: 購入するときの一定金額
    lp: 前日より価格が低い時に買いを行った時の時間と価格のSeries返す
    戻り値:
        tickets: 購入したチケット数
    """
    lp = lowprice(price)
    tickets = unit_cost / lp
    return tickets.astype(int) * price


# In[282]:

df


# In[281]:

price = randomwalk(10)+100
cost = dollcost(price, 10000)
df = pd.DataFrame([price, cost, cost.cumsum()], index=['price', 'cost', 'asset']).T
df.plot(style='.', subplots=True, figsize=(4,9))


# ## 特定期間で買い
# 毎週毎週購入かけているとお金が大量に必要になってしまう。
# 
# そんなに大量のお給料をもらっていないのである程度制限する。
# 
# ある週に1回でも購入したら、その週は条件が来ても購入を控えようと思う。
# 
# つまり来週になるまで「購入」の行動を無視するわけだね。

# In[193]:

p2b(price)


# In[155]:

def lowprice(price):
    """bullbearが負になったところだけのpriceを収集したpd.Seriesを返す
    ただし、1度購入すると次の週になるまで購入できない"""
    return price[np.array(p2b(price))<0]


# In[230]:

ts = pd.date_range('20170312', periods=100)
df = pd.DataFrame(np.random.rand(len(ts)), index=ts)
ps = df.asfreq('W', how='start')
ts.ali


# In[241]:

p = pd.Period('20170312', )
p.asfreq('W','start')
# pd.Period(pd.datetime.today().date(), freq='W')


# In[ ]:

freq = 5 

