# ドルコスト平均法
ドルコスト平均法をシミュレート

1. 下がったら買い
2. 一定額を買う

## ランダムウォークのシリーズを作成
* bullbearはランダムに+1, 0, -1を発生させるリスト
* priceがbullbearのcumsum
* bullbear < 0で買い
* priceはbullbearから発生させているが、実際の日経平均などからはpriceをネット上 のデータとして引っ張ってくるので、 priceの値からbullbearを計算する

```python
n = 1000
bullbear = pd.Series(np.random.randint(-1, 2, n))
price = bullbear.cumsum()
```

![png](randomwalk_files/randomwalk_2_1.png)


## 前日より値が低かったら買い、高かったら見過ごし
ドルコスト平均法の(1)を実現する最もシンプルなpythonスクリプト

```python
position = np.zeros(len(se))  # seと同じ長さの配列を作成
for i in price.index[:-1]:
    if price[i+1] - price[i] < 0:  # 前日の値のほうが小さければ高ければ安くなっているということ
        position[i]=price[i]  # そのときのpriceで買い
position
```

![png](randomwalk_files/randomwalk_5_1.png)



### priceからbullbearの計算

```python
def p2b(price):
    return price.sub(price.shift(1), fill_value=0)
```

`p2b`関数によってbullbearの計算が可能となった。



## 効率化
前日の値より低かった日の終値だけを収集する関数

```python
def lowprice(price):
    """bullbearが負になったところだけのpriceを収集したpd.Seriesを返す"""
    return price[np.array(p2b(price))<0]
```

pd.Serieesから直接引き出すので高速。10倍速を実現した



## 可視化

```python
low = lowprice(price)
pd.DataFrame([price, pd.Series(np.zeros_like(low)+min(price), index=low.index), low.cumsum()]).T.plot\
    (grid=True, style=['-', '^', '.'], secondary_y=[False, False, True])
```

![png](randomwalk_files/randomwalk_24_1.png)

下の三角マークは購入したところをプロット

`pd.Series(np.zeros_like(low)+min(price), index=low.index)`でDateTimeをそのままに値だけpriceの最小値にする。
