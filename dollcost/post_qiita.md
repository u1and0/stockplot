
# はじめに
ドルコスト平均法をpython, pandasを使ってシミュレートします。
読者はpython, pandasの基礎的な知識を持っているものとします。

![pngfile](./randomwalk_files/randomwalk_6_1.png)
![pngfile](./randomwalk_files/randomwalk_33_2.png)

概要こんな感じ。
あとで使う画像です。

ここでは株価や為替の既存のチャートを使用しません。
トレンド相場、レンジ相場の様々な形の相場でドルコスト平均法を試したいのですが、
既存のチャートでトレンドやレンジを調べて切り出してくることに労力がかかるためです。

そこで、ランダムに生成させた仮のチャートを使用します。
見た目がチャートにそっくりなので、これでもざっくりシミュレーションには有効でしょう。
その動きに対してドルコスト平均法を適用して、この投資法の有効性を判定する目論見です。

# 金融用語説明
プログラムするにはルールを知らなければいけませんので記載します。
リンク先はwikipediaです。

## [ドルコスト平均法](https://ja.wikipedia.org/wiki/%E3%83%89%E3%83%AB%E3%83%BB%E3%82%B3%E3%82%B9%E3%83%88%E5%B9%B3%E5%9D%87%E6%B3%95)

* 投資手法の一つで、高値掴みを避けるように投資額を時間的に分割して均等額ずつ定期的に投資します。
* 重要なのが投資額を等分する際、**金額分割**を行うこと
    * 単純な数量分割に比べ平均値の点で有利になると言われています。
    * ○金額分割: 定額数の株や、変量数の売通貨で定額の買通貨を購入すること
        * 1000,000円投資を10回に分けて100,000円分ずつの株を購入すること
        * 100,000円投資を10回に分けて10,000円分ずつのドルを購入すること
    * ×数量分割: 定量数の株や、定額の売通貨で買通貨を購入すること
        * 1000株投資を10回に分けて100株ずつ購入すること
        * 1000ドル投資を10回に分けて、100ドル分ずつのドルを購入すること

### ドルコスト平均法のルール
1. 定期的に購入します。
	* よく本に載っている手法として、毎月この日！と決めた日にちに購入していきます。
	* 私の使っている手法として、週の最安値(だと思っているところ)で指値をいれます。
1. 一定数ではなく、一定額を買うようにします。
    * 値段が下がればいっぱい買えます。
    * 値段が上がれば控えめに買っておきます。

## [ランダムウォーク](https://ja.wikipedia.org/wiki/%E3%83%A9%E3%83%B3%E3%83%80%E3%83%A0%E3%83%BB%E3%82%A6%E3%82%A9%E3%83%BC%E3%82%AF%E7%90%86%E8%AB%96)
* 現れる位置が確率的に無作為（ランダム）に決定される運動のことです。
* 株価や為替の価格は誰かが買うと上がり、売ると下がります。
	* つまり上がるか下がるかの2択
* 長期的に見ても短期的(ある程度の限度はあるが)に見ても似たような形が出現する、
自己相似形([フラクタル](https://ja.wikipedia.org/wiki/%E3%83%95%E3%83%A9%E3%82%AF%E3%82%BF%E3%83%AB#.E3.83.95.E3.83.A9.E3.82.AF.E3.82.BF.E3.83.AB.E3.81.AE.E4.BE.8B))
の形状をしています。

### ランダムウォークのpandas Seriesを作成


```python
n = 1000
bullbear = pd.Series(np.random.randint(-1, 2, n))  # -1,0,1のどれかを生成するpd.Series
price = bullbear.cumsum()  # 累積和

print(pd.DataFrame({'bullbear': bullbear, 'price': price}).head())
price.plot()
```

       bullbear  price
    0         1      1
    1         1      2
    2        -1      1
    3        -1      0
    4         0      0
    




    <matplotlib.axes._subplots.AxesSubplot at 0x22412696048>




![png](post_qiita_files/post_qiita_8_2.png)


### ランダムウォークの関数化


```python
def randomwalk(periods, start=pd.datetime.today().date(), name=None):
    """periods日分だけランダムウォークを返す"""
    ts = pd.date_range(start=start, periods=periods, freq='B')  # 今日の日付からperiod日分の平日
    bullbear = pd.Series(np.random.randint(-1, 2, periods),
                         index=ts, name=name)  # -1,0,1のどれかを吐き出すSeries
    price = bullbear.cumsum()  # 累積和
    return price
price=randomwalk(periods=1000) + 100  # 100は初期値
price.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1f997ab2630>




![png](post_qiita_files/post_qiita_10_1.png)


一日ごとに

* 1円上がる
* 1円下がる
* 動かない(0円動く)

を模擬したチャートができました。

初期値を100円、期間を1000日とすることで、100円から始まる約3年分の仮想ドル円チャートです。

一日1円とか、このチャートがドル円だとすると2016年の上海ショック、ブレグジットショック、米大統領選が毎日続いているかのようなお祭りボラティリティですね。

# 定期的に購入
ドルコスト平均法の(1)

用語説明に記載した、本に載っている手法ではなく私なりの手法を使います。

毎週のここが最安値！と思っているところで指して、約定して、実際それが週の底値だったという、ミラクル理想的な状況で購入できたとします。

チャートの週の底値は`resample`メソッドで圧縮して、`min`メソッドで最小値を取得します。


```python
def lowweek(price):
    """毎週の最安値を返す"""
    return price.resample('W').min()
lowweek(price).head(10)
```




    2017-03-19    98
    2017-03-26    97
    2017-04-02    93
    2017-04-09    91
    2017-04-16    90
    2017-04-23    89
    2017-04-30    90
    2017-05-07    91
    2017-05-14    93
    2017-05-21    93
    Freq: W-SUN, dtype: int32



例えば一行目は、2017年3月19日(日曜)が週末の日付である週に98円で購入できた、という意味です。

# 一定金額の購入
ドルコスト平均法の(1)

## 購入口数(ticket)の決定

* 価格の単位は[円]であるとします
* 購入額(unit_cost)を最大10000円として買っていくとします
* ~~購入口数(ticket)の最小口数(min_cost)は1000円~~ 未実装
* unit_costをある時点での価格(price)で割って、小数を切り落とした値が購入口数となります


```python
unit_cost = 10000
# min_cost = 1000
ticket = unit_cost / price[0]
ticket, int(ticket)
```




    (101.01010101010101, 101)



インデックス0の期間

次に全期間に適用します。

切り捨てすると時は`astype(int)`メソッドを使います。


```python
tickets = unit_cost / price
pd.DataFrame([price, tickets, tickets.astype(int)],
             index=['price', 'ticket(float)', 'ticket(int)']).T.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>price</th>
      <th>ticket(float)</th>
      <th>ticket(int)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-03-13</th>
      <td>99.0</td>
      <td>101.010101</td>
      <td>101.0</td>
    </tr>
    <tr>
      <th>2017-03-14</th>
      <td>98.0</td>
      <td>102.040816</td>
      <td>102.0</td>
    </tr>
    <tr>
      <th>2017-03-15</th>
      <td>98.0</td>
      <td>102.040816</td>
      <td>102.0</td>
    </tr>
    <tr>
      <th>2017-03-16</th>
      <td>99.0</td>
      <td>101.010101</td>
      <td>101.0</td>
    </tr>
    <tr>
      <th>2017-03-17</th>
      <td>99.0</td>
      <td>101.010101</td>
      <td>101.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
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
```

# ドルコスト平均法シミュレーション


```python
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
```

                lowprice  tickets    cost    asset    value  profit
    2017-03-13       NaN      NaN     NaN      NaN      NaN     NaN
    2017-03-14       NaN      NaN     NaN      NaN      NaN     NaN
    2017-03-15       NaN      NaN     NaN      NaN      NaN     NaN
    2017-03-16       NaN      NaN     NaN      NaN      NaN     NaN
    2017-03-17       NaN      NaN     NaN      NaN      NaN     NaN
    2017-03-19      98.0    102.0  9996.0   9996.0      NaN     NaN
    2017-03-20       NaN      NaN     NaN   9996.0  10200.0   204.0
    2017-03-21       NaN      NaN     NaN   9996.0  10098.0   102.0
    2017-03-22       NaN      NaN     NaN   9996.0   9996.0     0.0
    2017-03-23       NaN      NaN     NaN   9996.0   9996.0     0.0
    2017-03-24       NaN      NaN     NaN   9996.0   9894.0  -102.0
    2017-03-25       NaN      NaN     NaN   9996.0      NaN     NaN
    2017-03-26      97.0    103.0  9991.0  19987.0      NaN     NaN
    2017-03-27       NaN      NaN     NaN  19987.0  19680.0  -307.0
    2017-03-28       NaN      NaN     NaN  19987.0  19475.0  -512.0
    2017-03-29       NaN      NaN     NaN  19987.0  19475.0  -512.0
    2017-03-30       NaN      NaN     NaN  19987.0  19270.0  -717.0
    2017-03-31       NaN      NaN     NaN  19987.0  19065.0  -922.0
    




    array([<matplotlib.axes._subplots.AxesSubplot object at 0x000001F99B31A828>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x000001F99B368400>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x000001F99B3AE400>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x000001F99B400A58>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x000001F99B443A58>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x000001F99B49A940>], dtype=object)




![png](post_qiita_files/post_qiita_25_2.png)



```python
price[-1] * tickets.sum() - cost.sum()  # 最終損益
```




    -8561.0




```python
df = profitcalc(lowweek, 10000)
df.head(10)
df.plot(subplots=True, style='.', figsize=[4,8])
```




    array([<matplotlib.axes._subplots.AxesSubplot object at 0x000001C0DDCED908>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x000001C0DF1C8F98>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x000001C0DF03C198>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x000001C0DF07AA58>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x000001C0DF0D04A8>], dtype=object)




![png](post_qiita_files/post_qiita_27_1.png)



```python
df.profit[-1]  # 最終損益
```




    -4433



## ticket, cost, assetの計算関数


```python
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
```

## 別のランダムウォークで計算


```python
pr = randomwalk(1000) + 100
df = profitcalc(pr.resample('W').min(), unit_cost=10000)
# df.plot(subplots=True, style='.', figsize=[4,8])
df.ix[:, ['price', 'profit']].plot(secondary_y=['profit'], style='.')
```

    Final Asset: 1993341
    Final Profit: -609801
    




    <matplotlib.axes._subplots.AxesSubplot at 0x1c0e7022f28>




![png](post_qiita_files/post_qiita_32_2.png)

