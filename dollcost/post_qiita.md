
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
    * ○金額分割: 定額数の株や、定額の売通貨で買通貨を購入すること
        * 1000,000円投資を10回に分けて100,000円分ずつの株を購入すること
        * 100,000円投資を10回に分けて10,000円分ずつのドルを購入すること
    * ×数量分割: 定量数の株や、変量数の売通貨で定額の買通貨を購入すること
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
np.random.seed(1)  # 練習のため常に同じrandom stateリセット
bullbear = pd.Series(np.random.randint(-1, 2, n))  # -1,0,1のどれかを生成するpd.Series
price = bullbear.cumsum()  # 累積和

# 出力
print(pd.DataFrame({'bullbear': bullbear, 'price': price}).head())
price.plot()
```

       bullbear  price
    0         0      0
    1        -1     -1
    2        -1     -2
    3         0     -2
    4         0     -2
    




    <matplotlib.axes._subplots.AxesSubplot at 0x281f6f36b70>




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

np.random.seed(1)  # 練習のため常に同じrandom stateリセット
price=randomwalk(periods=1000) + 115  # 115は初期値
price.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x281f6f4bef0>




![png](post_qiita_files/post_qiita_10_1.png)


一日ごとに

* 1円上がる
* 1円下がる
* 動かない(0円動く)

を模擬したチャートができました。

初期値を115円(2017/3半ば現在これくらいの値)、期間を1000日とすることで、115円から始まる約3年分の仮想ドル円チャートです。

一日1円とか、このチャートがドル円だとすると2016年の上海ショック、ブレグジットショック、米大統領選が毎日続いているかのようなお祭りボラティリティですね。

これにもっともらしい経済用語ちりばめた説明文つけると、なんちゃって経済アナリスト気分。

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




    2017-03-19    113
    2017-03-26    110
    2017-04-02    109
    2017-04-09    110
    2017-04-16    110
    2017-04-23    111
    2017-04-30    111
    2017-05-07    112
    2017-05-14    109
    2017-05-21    109
    Freq: W-SUN, dtype: int32



例えば一行目は、2017年3月19日(日曜)が週末の日付である週に113円で購入できた、という意味です。

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
price[0], ticket, int(ticket)
```




    (115, 86.956521739130437, 86)



インデックス0の期間のチケット数の計算


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
      <th>2017-03-14</th>
      <td>115.0</td>
      <td>86.956522</td>
      <td>86.0</td>
    </tr>
    <tr>
      <th>2017-03-15</th>
      <td>114.0</td>
      <td>87.719298</td>
      <td>87.0</td>
    </tr>
    <tr>
      <th>2017-03-16</th>
      <td>113.0</td>
      <td>88.495575</td>
      <td>88.0</td>
    </tr>
    <tr>
      <th>2017-03-17</th>
      <td>113.0</td>
      <td>88.495575</td>
      <td>88.0</td>
    </tr>
    <tr>
      <th>2017-03-20</th>
      <td>113.0</td>
      <td>88.495575</td>
      <td>88.0</td>
    </tr>
  </tbody>
</table>
</div>



全期間に適用します。

切り捨てすると時は`astype(int)`メソッドを使います。


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

## 利益の計算


```python
lowprice = lowweek(price)  # 週の終値
tickets = dollcost(lowprice, unit_cost=10000)  # dollcost関数: 一定額ずつの購入
cost = tickets * lowprice  # 購入ごとにかかった費用
total_cost = cost.cumsum().resample('D').ffill()  # 全費用の合計(ただし手数料やスリッページ、スワップは除く)
value = tickets.cumsum().resample('D').ffill() * price  # 全ポジションの現在価値: 口数の累積和を週から日ごとに直して価格にかける
profit = value - total_cost  # 利益: 現在価値と費用の差

df = pd.DataFrame([lowprice, tickets, cost, total_cost, value, profit],
                  index=['lowprice', 'tickets', 'cost', 'total_cost','value', 'profit']).T
print(df.head(18))
df.plot(style='.', subplots=True, figsize=(4,9))
```

                lowprice  tickets    cost  total_cost    value  profit
    2017-03-14       NaN      NaN     NaN         NaN      NaN     NaN
    2017-03-15       NaN      NaN     NaN         NaN      NaN     NaN
    2017-03-16       NaN      NaN     NaN         NaN      NaN     NaN
    2017-03-17       NaN      NaN     NaN         NaN      NaN     NaN
    2017-03-19     113.0     88.0  9944.0      9944.0      NaN     NaN
    2017-03-20       NaN      NaN     NaN      9944.0   9944.0     0.0
    2017-03-21       NaN      NaN     NaN      9944.0   9856.0   -88.0
    2017-03-22       NaN      NaN     NaN      9944.0   9768.0  -176.0
    2017-03-23       NaN      NaN     NaN      9944.0   9768.0  -176.0
    2017-03-24       NaN      NaN     NaN      9944.0   9680.0  -264.0
    2017-03-25       NaN      NaN     NaN      9944.0      NaN     NaN
    2017-03-26     110.0     90.0  9900.0     19844.0      NaN     NaN
    2017-03-27       NaN      NaN     NaN     19844.0  19580.0  -264.0
    2017-03-28       NaN      NaN     NaN     19844.0  19402.0  -442.0
    2017-03-29       NaN      NaN     NaN     19844.0  19580.0  -264.0
    2017-03-30       NaN      NaN     NaN     19844.0  19580.0  -264.0
    2017-03-31       NaN      NaN     NaN     19844.0  19758.0   -86.0
    2017-04-01       NaN      NaN     NaN     19844.0      NaN     NaN
    




    array([<matplotlib.axes._subplots.AxesSubplot object at 0x00000281FB83B080>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x00000281FB88B6A0>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x00000281FC913BE0>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x00000281FC92E940>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x00000281FC9AB780>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x00000281FC9C4710>], dtype=object)




![png](post_qiita_files/post_qiita_26_2.png)


### 変数の意味

* lowprice: 週の安値
* tickets:  その週に購入した建玉
    * dollcost関数:  第一引数のSeriesを第二引数で割ってintで返す
* cost: 建玉を持つために投資した金額
* total_cost: 投資額の合計(週から日にupsamplingする)
* value: 全ポジションの現在価値
* profit: 利益(現在価値と費用の差)

### グラフの意味

* lowprice: 週の安値にダウンサンプリングされているので、price曲線に似た形で分布がまばら
* tickets:  定数で割っているのでlowpriceと逆相関
* cost: lowpriceを定数で割るとticketsが出てくる(dollcost関数の仕事)が、ticketsに小数がありえないためにlowpriceとticketsをかけても定数に戻らない。最大値の10000円とそこから離れすぎた値になっていないことを確認できれば良い。
* asset: 毎週定額投資をしているので綺麗な線形増加関数にならなければならない
* value: assetとprice両方に相関した関数形。
* profit: assetから浮いているvalueの値


```python
df.ix[:, ['lowprice','total_cost', 'value', 'profit']]\
    .plot(style=['o', '-', '-', '-'], secondary_y=['lowprice'])
```




    <matplotlib.axes._subplots.AxesSubplot at 0x281fcf31208>




![png](post_qiita_files/post_qiita_29_1.png)


購入価格(lowprice)とトータルコスト(total_cost)、資産価値、利益を並べてみました。 
モーサテとかでよく見かけそうなグラフ。

total_cost(黄)から浮いているvalue(緑)の部分がprofit(青)、すなわち利益となります。

ドルコスト平均法の良いところ
* 相場の急変に強い(上がろうが下がろうがvalueがtotal_costに沿う)
* 


```python
price[-1] * tickets.sum() - cost.sum()  # 最終損益
```




    276780



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


```python
df = profitcalc(lowweek, 10000)
df.head(10)
df.plot(subplots=True, style='.', figsize=[4,8])
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-31-359fc5e60db1> in <module>()
    ----> 1 df = profitcalc(lowweek, 10000)
          2 df.head(10)
          3 df.plot(subplots=True, style='.', figsize=[4,8])
    

    NameError: name 'profitcalc' is not defined



```python
df.profit[-1]  # 最終損益
```

## 別のランダムウォークで計算


```python
pr = randomwalk(1000) + 100
df = profitcalc(pr.resample('W').min(), unit_cost=10000)
# df.plot(subplots=True, style='.', figsize=[4,8])
df.ix[:, ['price', 'profit']].plot(secondary_y=['profit'], style='.')
```
