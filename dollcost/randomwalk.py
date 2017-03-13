
# coding: utf-8

# # ドルコスト平均法
# 1. 下がったら買い
# 2. 一定数ではなく、一定額を買う
# > 値段が下がればいっぱい買える。
# > 値段が上がれば控えめに買っておく

# ## ランダムウォークのシリーズを作成

# In[22]:

n = 1000
bullbear = pd.Series(np.random.randint(-1, 2, n))
price = bullbear.cumsum()
price.index.name='DateTime'
price.plot()


# # 前日より値が低かったら買い、高かったら見過ごし
# ドルコスト平均法の(1)

# In[23]:

position = np.zeros(len(price))  # priceと同じ長さの配列を作成
for i in price.index[:-1]:
    if price[i+1] - price[i] < 0:  # 前日の値のほうが小さければ高ければ安くなっているということ
        position[i]=price[i]  # そのときのpriceで買い
position[:60]


# In[24]:

fig, ax = plt.subplots()
price.plot(ax=ax)
pd.DataFrame(position).cumsum().plot(ax=ax, secondary_y=True)  # ポジションのcumulative sumをプロット


# ## priceからbullbearの計算
# priceはbullbearから発生させているが、
# 実際の日経平均などからはpriceをネット上 のデータとして引っ張ってくるので、 
# priceの値からbullbearを計算できるようにする
# 

# In[25]:

def p2b(price):
    return price.sub(price.shift(1), fill_value=0)


# In[26]:

np.array_equal(p2b(price), np.array(bullbear))


# `p2b`関数によってbullbearの計算が可能となった。

# ## 効率化
# 前日の値より低かった日の終値だけを収集する関数

# In[27]:

def dob(price):
    pos = np.zeros(len(price))  # priceと同じ長さの配列を作成
    for i in price.index[:-1]:
        if price[i+1]<price[i]:  # 前日の値より安ければ
            pos[i]=price[i]  # 買い
    return pos


# In[28]:

get_ipython().magic('timeit dob(price)')


# 最もシンプル

# In[29]:

get_ipython().magic('timeit [price[i] if price[i+1]<price[i] else 0 for i in price.index[:-1]]')


# 内包表記を用いても時間はあまり変わらない

# In[30]:

def dob2(price):
    pos = np.zeros(len(price))  # priceと同じ長さの配列を作成
    pos = [price[i] if price.sub(price.shift(1), fill_value=0)<0 else 0]  # 下がったら買い
    return pos


# In[31]:

price[np.array(bullbear)<0]  # bullbearが負の値になったところだけのpriceを収集


# In[54]:

def lowprice(price):
    """bullbearが負になったところだけのpriceを収集したpd.Seriesを返す"""
    return price[np.array(p2b(price))<0]


# In[33]:

get_ipython().magic('timeit lowprice(price)')


# pd.Serieesから直接引き出すので高速。10倍速を実現した

# ## 可視化
# 価格(price)と購入した時の額(low)と合計資産(asset)を描画する

# In[34]:

low = lowprice(price)
ax = pd.DataFrame([price, low, low.cumsum()]).T.plot(grid=True, style=['-', '^', '.'], secondary_y=[False, False, True])


# In[35]:

low = lowprice(price)
df = pd.DataFrame([price, pd.Series(np.zeros_like(low)+min(price), index=low.index), low.cumsum()]).T
df.plot(grid=True, style=['-', '^', '.'], secondary_y=[False, False, True])


# # 一定金額を買い
# ドルコスト平均法の(2)

# ## ランダムウォークの関数化

# In[36]:

def randomwalk(periods, start=pd.datetime.today().date(), name=None):
    """periods日分だけランダムウォークを返す"""
    ts = pd.date_range(start=start, periods=periods, freq='B')
    bullbear = pd.Series(np.random.randint(-1, 2, periods), index=ts, name=name)
    price = bullbear.cumsum()
    return price
price=randomwalk(100) + 100  # 100は初期値
price.plot()


# ## 枚数(ticket)の購入

# ランダムウォークによる価格変動を再定義。
# 関数化してみた。
# 
# * 縦軸が単位[円]だとする
# * 例えば10000円(unit_cost)ずつ買っていくとする
# * ~~口数(ticket)の最小口数は1000円~~

# In[46]:

unit_cost = 10000
# min_cost = 1000
ticket = unit_cost / price[0]
ticket, int(ticket)


# 0インデックス目

# In[38]:

tickets = unit_cost / price
pd.DataFrame([price, tickets, tickets.astype(int)],
             index=['price', 'ticket(float)', 'ticket(int)']).T.head()


# 全期間に適用。
# 
# 切り捨てすると時は`astype(int)`メソッドを使う。

# ## 一定額ずつ購入していったあとの資産の計算

# In[55]:

def dollcost(lowprice, unit_cost):
    """一定額ずつの購入
    引数: 
        price: 購入したときの価格と日付のSeries
        unit_cost: 購入するときの一定金額
    戻り値:
        tickets: 購入したチケット数
    """
    tickets = unit_cost / lowprice
    return tickets.astype(int)


# In[56]:

# lowprice関数: 前日より価格が低い時に買いを行った時の時間と価格のSeries返す
# dollcost関数: 一定額ずつの購入
tickets = dollcost(lowprice(price), 10000)
cost = tickets * price
asset = cost.cumsum()
profit = tickets.cumsum() * price - asset

df = pd.DataFrame([price, tickets, cost, asset, profit],
                  index=['price', 'tickets', 'cost', 'asset', 'profit']).T
print(df.head())
df.plot(style='.', subplots=True, figsize=(4,9))


# In[57]:

price[-1] * tickets.sum() - cost.sum()  # 最終損益


# ## 特定期間で買い
# 毎週毎週購入かけているとお金が大量に必要になってしまう。
# そんなに大量のお給料をもらっていないのである程度制限する。
# ある週に1回でも購入したら、その週は条件が来ても購入を控えようと思う。

# 仮に、理想的に毎週の底値で購入できたとする

# In[59]:

lowweek = price.resample('W').min()
lowweek[:10]


# ## ticket, cost, assetの計算関数

# In[87]:

def profitcalc(price, unit_cost): 
    """購入した価格からプロフィットカーブを計算する
        引数:
            price: 購入価格と日付のSeries
            unit_cost: 購入一定額
        戻り値: price, tickets, cost, asset, profitを入れたdataframe"""
    tickets = dollcost(price, unit_cost)  # dollcost関数: 一定額ずつの購入
    cost = tickets * price
    asset = cost.cumsum()
    profit = tickets.cumsum() * price - asset
    df = pd.DataFrame([price, tickets, cost, asset, profit],
            index=['price', 'tickets', 'cost', 'asset', 'profit']).T
    print('Final Asset: %d'% df.asset[-1])
    print('Final Profit: %d'% df.profit[-1])
    return df


# In[64]:

df = profitcalc(lowweek, 10000)
df.head(10)
df.plot(subplots=True, style='.', figsize=[4,8])


# In[66]:

df.profit[-1]  # 最終損益


# ## 別のランダムウォークで計算

# In[99]:

pr = randomwalk(1000) + 100
df = profitcalc(pr.resample('W').min(), unit_cost=10000)
# df.plot(subplots=True, style='.', figsize=[4,8])
df.ix[:, ['price', 'profit']].plot(secondary_y=['profit'])


# # 開発中

# In[42]:

pd.Period('20170312', 'W')


# 一定期間としてみなすようにコンバートするにはpandas.Periodクラスを使う。
# 
# 2017/3/12は2017-03-06/2017-03-12の週の間に存在することがわかる。

# In[43]:

ts = pd.date_range('20170312', periods=100)
df = pd.DataFrame(np.random.rand(len(ts)), index=ts)
ps = df.asfreq('W', how='end')
ps.head()


# 週の最後の日の見つけ方がわかった
# 
# whileでこの日まで回して、購入行動を行ったらbreakでwhileから抜けるようにする。

# In[44]:

def lowprice(price):
    """bullbearが負になったところだけのpriceを収集したpd.Seriesを返す
    ただし、1度購入すると次の週になるまで購入できない"""
    pos = np.zeros_like(price)
    for end in price.index.asfreq('W', how='end'):
        for i in date_range():
            for i in price.index[:-1]:
                if price[i+1] - price[i] < 0:  # 前日の値のほうが小さければ高ければ安くなっているということ
                    position[i]=price[i]  # そのときのpriceで買い
    return price[np.array(p2b(price))<0]


# In[45]:

[i for i in price.index.asfreq('W', )]


# In[ ]:

p = pd.Period('20170312', 'W')
p.week


# In[ ]:



