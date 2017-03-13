
# coding: utf-8

# # はじめに
# ドルコスト平均法をpython, pandasを使ってシミュレートします。
# 読者はpython, pandasの基礎的な知識を持っているものとします。

# ![pngfile](./randomwalk_files/randomwalk_6_1.png)
# ![pngfile](./randomwalk_files/randomwalk_33_2.png)
# 
# 概要こんな感じ。
# あとで使う画像です。

# ここでは株価や為替の既存のチャートを使用しません。
# トレンド相場、レンジ相場の様々な形の相場でドルコスト平均法を試したいのですが、
# 既存のチャートでトレンドやレンジを調べて切り出してくることに労力がかかるためです。
# 
# そこで、ランダムに生成させた仮のチャートを使用します。
# 見た目がチャートにそっくりなので、これでもざっくりシミュレーションには有効でしょう。
# その動きに対してドルコスト平均法を適用して、この投資法の有効性を判定する目論見です。

# # 金融用語説明
# プログラムするにはルールを知らなければいけませんので記載します。
# リンク先はwikipediaです。

# ## [ドルコスト平均法](https://ja.wikipedia.org/wiki/%E3%83%89%E3%83%AB%E3%83%BB%E3%82%B3%E3%82%B9%E3%83%88%E5%B9%B3%E5%9D%87%E6%B3%95)
# 
# * 投資手法の一つで、高値掴みを避けるように投資額を時間的に分割して均等額ずつ定期的に投資します。
# * 重要なのが投資額を等分する際、**金額分割**を行うこと
#     * 単純な数量分割に比べ平均値の点で有利になると言われています。
#     * ○金額分割: 定額数の株や、変量数の売通貨で定額の買通貨を購入すること
#         * 1000,000円投資を10回に分けて100,000円分ずつの株を購入すること
#         * 100,000円投資を10回に分けて10,000円分ずつのドルを購入すること
#     * ×数量分割: 定量数の株や、定額の売通貨で買通貨を購入すること
#         * 1000株投資を10回に分けて100株ずつ購入すること
#         * 1000ドル投資を10回に分けて、100ドル分ずつのドルを購入すること

# ### ドルコスト平均法のルール
# 1. 定期的に購入します。
# 	* よく本に載っている手法として、毎月この日！と決めた日にちに購入していきます。
# 	* 私の使っている手法として、週の最安値(だと思っているところ)で指値をいれます。
# 1. 一定数ではなく、一定額を買うようにします。
#     * 値段が下がればいっぱい買えます。
#     * 値段が上がれば控えめに買っておきます。

# ## [ランダムウォーク](https://ja.wikipedia.org/wiki/%E3%83%A9%E3%83%B3%E3%83%80%E3%83%A0%E3%83%BB%E3%82%A6%E3%82%A9%E3%83%BC%E3%82%AF%E7%90%86%E8%AB%96)
# * 現れる位置が確率的に無作為（ランダム）に決定される運動のことです。
# * 株価や為替の価格は誰かが買うと上がり、売ると下がります。
# 	* つまり上がるか下がるかの2択
# * 長期的に見ても短期的(ある程度の限度はあるが)に見ても似たような形が出現する、
# 自己相似形([フラクタル](https://ja.wikipedia.org/wiki/%E3%83%95%E3%83%A9%E3%82%AF%E3%82%BF%E3%83%AB#.E3.83.95.E3.83.A9.E3.82.AF.E3.82.BF.E3.83.AB.E3.81.AE.E4.BE.8B))
# の形状をしています。

# ### ランダムウォークのpandas Seriesを作成

# In[7]:

n = 1000
bullbear = pd.Series(np.random.randint(-1, 2, n))  # -1,0,1のどれかを生成するpd.Series
price = bullbear.cumsum()  # 累積和

print(pd.DataFrame({'bullbear': bullbear, 'price': price}).head())
price.plot()


# ### ランダムウォークの関数化

# In[9]:

def randomwalk(periods, start=pd.datetime.today().date(), name=None):
    """periods日分だけランダムウォークを返す"""
    ts = pd.date_range(start=start, periods=periods, freq='B')  # 今日の日付からperiod日分の平日
    bullbear = pd.Series(np.random.randint(-1, 2, periods),
                         index=ts, name=name)  # -1,0,1のどれかを吐き出すSeries
    price = bullbear.cumsum()  # 累積和
    return price
price=randomwalk(periods=1000) + 100  # 100は初期値
price.plot()


# 一日ごとに
# 
# * 1円上がる
# * 1円下がる
# * 動かない(0円動く)
# 
# を模擬したチャートができました。
# 
# 初期値を100円、期間を1000日とすることで、100円から始まる約3年分の仮想ドル円チャートです。
# 
# 一日1円とか、このチャートがドル円だとすると2016年の上海ショック、ブレグジットショック、米大統領選が毎日続いているかのようなお祭りボラティリティですね。

# # 定期的に購入
# ドルコスト平均法の(1)

# 用語説明に記載した、本に載っている手法ではなく私なりの手法を使います。
# 
# 毎週のここが最安値！と思っているところで指して、約定して、実際それが週の底値だったという、ミラクル理想的な状況で購入できたとします。
# 
# チャートの週の底値は`resample`メソッドで圧縮して、`min`メソッドで最小値を取得します。

# In[29]:

def lowweek(price):
    """毎週の最安値を返す"""
    return price.resample('W').min()
lowweek(price).head(10)


# 例えば一行目は、2017年3月19日(日曜)が週末の日付である週に98円で購入できた、という意味です。

# # 一定金額の購入
# ドルコスト平均法の(1)

# ## 購入口数(ticket)の決定

# * 価格の単位は[円]であるとします
# * 購入額(unit_cost)を最大10000円として買っていくとします
# * ~~購入口数(ticket)の最小口数(min_cost)は1000円~~ 未実装
# * unit_costをある時点での価格(price)で割って、小数を切り落とした値が購入口数となります

# In[30]:

unit_cost = 10000
# min_cost = 1000
ticket = unit_cost / price[0]
ticket, int(ticket)


# インデックス0の期間

# 次に全期間に適用します。
# 
# 切り捨てすると時は`astype(int)`メソッドを使います。

# In[20]:

tickets = unit_cost / price
pd.DataFrame([price, tickets, tickets.astype(int)],
             index=['price', 'ticket(float)', 'ticket(int)']).T.head()


# In[21]:

def dollcost(lowprice, unit_cost):
    """一定額ずつの購入
    引数: 
        price: 購入したときの価格と日付のSeries
        unit_cost: 購入するときの一定金額
    戻り値:
        tickets: 購入口数
    """
    tickets = unit_cost / lowprice
    return tickets.astype(int)


# # ドルコスト平均法シミュレーション

# In[35]:

lowprice = lowweek(price)  # 週の終値
tickets = dollcost(lowprice, unit_cost=10000)  # dollcost関数: 一定額ずつの購入
cost = tickets * lowprice  # 購入ごとにかかった費用
asset = cost.cumsum().resample('D').ffill()  # 費用の合計
value = tickets.cumsum().resample('D').ffill() * price  # 現在価値: 口数の累積和を週から日ごとに直して価格にかける
profit = value - asset  # 現在価値から費用の合計を引いたのが利益(profit)

df = pd.DataFrame([lowprice, tickets, cost, asset, value, profit],
                  index=['lowprice', 'tickets', 'cost', 'asset','value', 'profit']).T
print(df.head(18))
df.plot(style='.', subplots=True, figsize=(4,9))


# In[57]:

price[-1] * tickets.sum() - cost.sum()  # 最終損益


# In[64]:

df = profitcalc(lowweek, 10000)
df.head(10)
df.plot(subplots=True, style='.', figsize=[4,8])


# In[66]:

df.profit[-1]  # 最終損益


# ## ticket, cost, assetの計算関数

# In[87]:

def profitcalc(price, unit_cost): 
    """購入した価格からプロフィットカーブを計算する
        引数:
            price: 購入価格と日付のSeries
            unit_cost: 一定購入額
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


# ## 別のランダムウォークで計算

# In[99]:

pr = randomwalk(1000) + 100
df = profitcalc(pr.resample('W').min(), unit_cost=10000)
# df.plot(subplots=True, style='.', figsize=[4,8])
df.ix[:, ['price', 'profit']].plot(secondary_y=['profit'], style='.')

