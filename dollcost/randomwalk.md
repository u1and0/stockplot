
# ドルコスト平均法
1. 下がったら買い
2. 一定額を買う

## ランダムウォークのシリーズを作成


```python
n = 1000
bullbear = pd.Series(np.random.randint(-1, 2, n))
price = bullbear.cumsum()
price.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1d5b5860fd0>




![png](randomwalk_files/randomwalk_2_1.png)


## 前日より値が低かったら買い、高かったら見過ごし
ドルコスト平均法の(1)


```python
position = np.zeros(len(se))  # seと同じ長さの配列を作成
for i in price.index[:-1]:
    if price[i+1] - price[i] < 0:  # 前日の値のほうが小さければ高ければ安くなっているということ
        position[i]=price[i]  # そのときのpriceで買い
position
```




    array([  0.,   0.,   0.,   0.,   1.,   0.,   1.,   0.,   1.,   0.,   0.,
             0.,   0.,   0.,   0.,   1.,   0.,   0.,   0.,   0.,   1.,   0.,
            -1.,   0.,   0.,   0.,   0.,  -1.,   0.,   0.,   0.,   0.,   0.,
             0.,   2.,   0.,   0.,   0.,   0.,   2.,   0.,   0.,   0.,   4.,
             0.,   4.,   3.,   0.,   0.,   4.,   0.,   0.,   4.,   0.,   3.,
             0.,   3.,   0.,   3.,   0.,   3.,   0.,   0.,   0.,   3.,   0.,
             3.,   2.,   0.,   0.,   0.,   2.,   0.,   0.,   0.,   0.,   4.,
             0.,   0.,   0.,   0.,   0.,   5.,   4.,   0.,   3.,   2.,   1.,
             0.,   0.,   0.,   0.,   0.,   0.,   5.,   4.,   3.,   0.,   0.,
             3.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   5.,   4.,   0.,
             3.,   0.,   3.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   6.,   0.,   0.,   0.,   0.,   0.,
             8.,   7.,   0.,   7.,   0.,   0.,   0.,   0.,   8.,   0.,   0.,
             0.,   0.,  11.,   0.,  10.,   0.,  10.,   0.,  10.,   0.,   0.,
             9.,   0.,   0.,   0.,   0.,  10.,   9.,   8.,   0.,   0.,   7.,
             0.,   6.,   0.,   0.,   0.,   0.,   0.,   0.,   7.,   6.,   0.,
             0.,   5.,   0.,   5.,   4.,   0.,   0.,   4.,   3.,   2.,   1.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   1.,   0.,   0.,   0.,
             0.,   1.,   0.,   0.,   0.,   0.,   0.,   3.,   2.,   1.,   0.,
             1.,   0.,   0.,   0.,   0.,   2.,   0.,   0.,   0.,   0.,   3.,
             0.,   0.,   2.,   0.,   1.,   0.,   0.,   1.,   0.,   0.,   0.,
             2.,   1.,   0.,   0.,   0.,   0.,   2.,   0.,   1.,   0.,   0.,
             0.,  -1.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,  -1.,
            -2.,   0.,   0.,  -2.,   0.,  -3.,   0.,   0.,   0.,   0.,  -2.,
            -3.,   0.,  -4.,   0.,  -4.,  -5.,   0.,  -5.,   0.,   0.,  -4.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
            -1.,  -2.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   2.,   0.,   0.,   0.,   0.,   0.,   3.,   0.,
             2.,   0.,   0.,   3.,   0.,   3.,   0.,   2.,   0.,   0.,   0.,
             0.,   0.,   4.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   5.,
             0.,   4.,   0.,   4.,   3.,   2.,   0.,   0.,   0.,   3.,   0.,
             0.,   0.,   5.,   0.,   5.,   0.,   0.,   0.,   5.,   0.,   0.,
             0.,   0.,   7.,   0.,   0.,   8.,   0.,   8.,   0.,   7.,   6.,
             5.,   0.,   0.,   0.,   6.,   0.,   0.,   0.,   0.,   7.,   6.,
             0.,   0.,   0.,   5.,   0.,   0.,   4.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   8.,   0.,   0.,   0.,   0.,  11.,   0.,  10.,
             0.,   9.,   8.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,  10.,
             9.,   0.,   0.,  10.,   9.,   8.,   7.,   0.,   0.,   0.,   8.,
             0.,   0.,   0.,   9.,   0.,   0.,  10.,   9.,   0.,   0.,   8.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,  10.,   0.,   0.,   0.,
             0.,  10.,   9.,   0.,   0.,   8.,   7.,   6.,   0.,   0.,   0.,
             7.,   0.,   0.,   0.,   8.,   0.,   8.,   7.,   0.,   0.,   0.,
             0.,   8.,   7.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   6.,
             5.,   4.,   0.,   4.,   3.,   0.,   3.,   2.,   0.,   0.,   1.,
             0.,   0.,   0.,   0.,   0.,  -1.,   0.,   0.,   0.,   0.,   0.,
             1.,   0.,   0.,   0.,   1.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   4.,   3.,   2.,   0.,   0.,   2.,   1.,   0.,  -1.,   0.,
            -2.,  -3.,   0.,   0.,  -2.,   0.,   0.,   0.,   0.,   0.,   0.,
            -1.,   0.,   0.,  -1.,   0.,  -1.,   0.,   0.,   0.,  -1.,   0.,
            -2.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             1.,   0.,   0.,   0.,   0.,  -1.,   0.,   0.,   0.,  -2.,   0.,
             0.,   0.,   0.,   0.,   0.,  -1.,  -2.,   0.,  -2.,   0.,   0.,
             0.,   0.,   0.,  -1.,   0.,   0.,   0.,   0.,   0.,   0.,  -1.,
            -2.,   0.,  -2.,   0.,  -2.,   0.,   0.,   0.,  -1.,   0.,  -2.,
             0.,  -2.,   0.,  -3.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   1.,   0.,   0.,   0.,   0.,   3.,   0.,   0.,   3.,   0.,
             3.,   2.,   0.,   0.,   0.,   0.,   3.,   0.,   0.,   0.,   3.,
             2.,   1.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   1.,
             0.,   0.,   0.,   0.,   0.,   2.,   1.,   0.,  -1.,  -2.,  -3.,
             0.,   0.,  -3.,  -4.,  -5.,   0.,  -6.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,  -3.,  -4.,   0.,   0.,   0.,
            -3.,  -4.,   0.,   0.,  -5.,  -6.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,  -2.,   0.,   0.,  -2.,   0.,  -2.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   2.,   0.,   0.,
             0.,   0.,   1.,   0.,   0.,   1.,   0.,   0.,   2.,   0.,   0.,
             0.,   2.,   1.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,  -1.,
             0.,   0.,  -2.,   0.,  -3.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,  -2.,  -3.,   0.,  -3.,  -4.,   0.,   0.,   0.,  -4.,   0.,
             0.,  -5.,  -6.,   0.,   0.,   0.,   0.,   0.,   0.,  -3.,  -4.,
             0.,  -4.,  -5.,   0.,  -6.,   0.,  -6.,  -7.,   0.,  -8.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,
             0.,   0.,   0.,   0.,  -4.,   0.,   0.,   0.,  -4.,  -5.,   0.,
             0.,  -5.,   0.,   0.,   0.,   0.,  -4.,   0.,   0.,   0.,  -3.,
            -4.,  -5.,  -6.,   0.,   0.,  -7.,  -8.,   0.,  -8.,   0.,  -8.,
             0.,   0.,   0.,   0.,   0.,   0.,  -4.,   0.,   0.,   0.,  -2.,
             0.,  -2.,   0.,  -3.,   0.,  -3.,   0.,  -3.,   0.,   0.,  -2.,
            -3.,  -4.,   0.,  -5.,   0.,  -5.,  -6.,   0.,   0.,   0.,  -5.,
             0.,  -6.,   0.,  -6.,  -7.,   0.,   0.,   0.,   0.,   0.,  -5.,
            -6.,   0.,  -6.,   0.,   0.,  -7.,   0.,  -8.,  -9., -10.,   0.,
             0.,   0.,   0.,  -9., -10.,   0., -10.,   0., -10., -11.,   0.,
             0.,   0., -10., -11.,   0.,   0.,   0., -11., -12., -13.,   0.,
             0., -13.,   0.,   0.,   0.,   0.,   0., -12.,   0., -12., -13.,
           -14.,   0.,   0.,   0., -13.,   0.,   0., -13.,   0., -13., -14.,
             0.,   0.,   0.,   0., -12.,   0.,   0.,   0.,   0.,   0.,   0.,
           -11., -12., -13.,   0.,   0.,   0., -13.,   0.,   0., -12., -13.,
             0., -13.,   0.,   0., -12.,   0.,   0.,   0.,   0.,   0., -12.,
             0.,   0.,   0., -11.,   0.,   0.,   0., -10.,   0.,   0.,   0.,
            -9.,   0.,   0.,   0.,  -8.,   0.,   0.,   0.,   0.,  -8.,   0.,
             0.,   0.,   0.,  -7.,   0.,  -7.,   0.,   0.,  -7.,  -8.,   0.,
             0.,   0.,   0.,   0.,   0.,   0.,   0.,  -6.,   0.,  -6.,   0.,
             0.,   0.,   0.,  -5.,   0.,   0.,   0.,   0.,   0.,   0.])




```python
fig, ax = plt.subplots()
price.plot(ax=ax)
pd.DataFrame(position).cumsum().plot(ax=ax, secondary_y=True)  # ポジションのcumulative sumをプロット
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1d5b543b780>




![png](randomwalk_files/randomwalk_5_1.png)


### priceからbullbearの計算


```python
def p2b(price):
    return price.sub(price.shift(1), fill_value=0)
```


```python
np.array_equal(p2b(price), np.array(bullbear))
```




    True



`p2b`関数によってbullbearの計算が可能となった。

## 効率化


```python
def dob(price):
    pos = np.zeros(len(price))  # priceと同じ長さの配列を作成
    for i in price.index[:-1]:
        if price[i+1]<price[i]:  # 前日の値より安ければ
            pos[i]=price[i]  # 買い
    return pos
```


```python
%timeit dob(price)
```

    10 loops, best of 3: 28.1 ms per loop
    


```python
%timeit [price[i] if price[i+1]<price[i] else 0 for i in price.index[:-1]]
```

    10 loops, best of 3: 28.3 ms per loop
    


```python
def dob2(price):
    pos = np.zeros(len(price))  # priceと同じ長さの配列を作成
    pos = [price[i] if price.sub(price.shift(1), fill_value=0)<0 else 0]  # 下がったら買い
    return pos
```


```python
price[np.array(bullbear)<0]
```




    0      -1
    5       0
    7       0
    9       0
    11     -1
    16      0
    17     -1
    21      0
    22     -1
    23     -2
    26     -1
    28     -2
    35      1
    40      1
    44      3
    46      3
    47      2
    50      3
    53      3
    55      2
    57      2
    59      2
    61      2
    65      2
    67      2
    68      1
    72      1
    77      3
    83      4
    84      3
           ..
    899   -13
    901   -13
    902   -14
    903   -15
    907   -14
    910   -14
    912   -14
    913   -15
    918   -13
    925   -12
    926   -13
    927   -14
    931   -14
    934   -13
    935   -14
    937   -14
    940   -13
    946   -13
    950   -12
    954   -11
    958   -10
    962    -9
    967    -9
    972    -8
    974    -8
    977    -8
    978    -9
    987    -7
    989    -7
    994    -6
    dtype: int32




```python
dob2(price)
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-60-9f8c61e6813e> in <module>()
    ----> 1 dob2(price)
    

    <ipython-input-58-f604979e7d4c> in dob2(price)
          1 def dob2(price):
          2     pos = np.zeros(len(price))  # priceと同じ長さの配列を作成
    ----> 3     pos = [price[i] if price.sub(price.shift(1), fill_value=0)<0 else 0]  # 下がったら買い
          4     return pos
    

    C:\Anaconda3\lib\site-packages\pandas\core\generic.py in __nonzero__(self)
        915         raise ValueError("The truth value of a {0} is ambiguous. "
        916                          "Use a.empty, a.bool(), a.item(), a.any() or a.all()."
    --> 917                          .format(self.__class__.__name__))
        918 
        919     __bool__ = __nonzero__
    

    ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().



```python
pd.DataFrame([se.shift(1), se, se.sub(se.shift(1), fill_value=0), bullbear]).T
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2.0</td>
      <td>1.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2.0</td>
      <td>1.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2.0</td>
      <td>3.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>3.0</td>
      <td>4.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>4.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>4.0</td>
      <td>5.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>5.0</td>
      <td>6.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>6.0</td>
      <td>6.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>6.0</td>
      <td>6.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>6.0</td>
      <td>6.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>17</th>
      <td>6.0</td>
      <td>7.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>7.0</td>
      <td>7.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>7.0</td>
      <td>6.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>20</th>
      <td>6.0</td>
      <td>5.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>21</th>
      <td>5.0</td>
      <td>5.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>22</th>
      <td>5.0</td>
      <td>6.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>23</th>
      <td>6.0</td>
      <td>7.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>24</th>
      <td>7.0</td>
      <td>6.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>25</th>
      <td>6.0</td>
      <td>6.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>26</th>
      <td>6.0</td>
      <td>5.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>27</th>
      <td>5.0</td>
      <td>5.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>28</th>
      <td>5.0</td>
      <td>6.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>29</th>
      <td>6.0</td>
      <td>5.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>970</th>
      <td>32.0</td>
      <td>33.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>971</th>
      <td>33.0</td>
      <td>32.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>972</th>
      <td>32.0</td>
      <td>32.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>973</th>
      <td>32.0</td>
      <td>32.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>974</th>
      <td>32.0</td>
      <td>31.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>975</th>
      <td>31.0</td>
      <td>32.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>976</th>
      <td>32.0</td>
      <td>32.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>977</th>
      <td>32.0</td>
      <td>32.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>978</th>
      <td>32.0</td>
      <td>31.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>979</th>
      <td>31.0</td>
      <td>30.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>980</th>
      <td>30.0</td>
      <td>30.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>981</th>
      <td>30.0</td>
      <td>29.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>982</th>
      <td>29.0</td>
      <td>28.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>983</th>
      <td>28.0</td>
      <td>27.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>984</th>
      <td>27.0</td>
      <td>26.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>985</th>
      <td>26.0</td>
      <td>27.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>986</th>
      <td>27.0</td>
      <td>27.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>987</th>
      <td>27.0</td>
      <td>27.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>988</th>
      <td>27.0</td>
      <td>26.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>989</th>
      <td>26.0</td>
      <td>26.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>990</th>
      <td>26.0</td>
      <td>27.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>991</th>
      <td>27.0</td>
      <td>28.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>992</th>
      <td>28.0</td>
      <td>27.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>993</th>
      <td>27.0</td>
      <td>27.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>994</th>
      <td>27.0</td>
      <td>26.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>995</th>
      <td>26.0</td>
      <td>25.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>996</th>
      <td>25.0</td>
      <td>24.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>997</th>
      <td>24.0</td>
      <td>23.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>998</th>
      <td>23.0</td>
      <td>24.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>999</th>
      <td>24.0</td>
      <td>24.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>1000 rows × 4 columns</p>
</div>




```python
se.shift(1).sub(se, fill_value=0)
```




    0      0.0
    1      0.0
    2     -1.0
    3      1.0
    4      0.0
    5     -1.0
    6      1.0
    7     -1.0
    8      1.0
    9      0.0
    10     1.0
    11     1.0
    12     0.0
    13    -1.0
    14     1.0
    15     1.0
    16    -1.0
    17     1.0
    18     1.0
    19     0.0
    20     0.0
    21     1.0
    22     1.0
    23     1.0
    24     1.0
    25     1.0
    26     0.0
    27     1.0
    28     1.0
    29     0.0
          ... 
    970    1.0
    971   -1.0
    972    1.0
    973    1.0
    974    0.0
    975    0.0
    976    0.0
    977    0.0
    978    1.0
    979    0.0
    980    1.0
    981   -1.0
    982    0.0
    983    1.0
    984    1.0
    985    0.0
    986    1.0
    987   -1.0
    988    0.0
    989    1.0
    990    1.0
    991    1.0
    992   -1.0
    993    0.0
    994   -1.0
    995    1.0
    996    1.0
    997    0.0
    998    1.0
    999    0.0
    dtype: float64




```python
[se[i] if se.shift(1).sub(se, fill_value=0)>0 else 0 for i in se]

```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-26-bf9892ea1036> in <module>()
    ----> 1 [se[i] if pd.sub(se.shift(1), se, fill_value=0)>0 else 0 for i in se]
    

    <ipython-input-26-bf9892ea1036> in <listcomp>(.0)
    ----> 1 [se[i] if pd.sub(se.shift(1), se, fill_value=0)>0 else 0 for i in se]
    

    AttributeError: module 'pandas' has no attribute 'sub'



```python
pd.DataFrame([se.shift(1), se]).T
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>-1.0</td>
      <td>-2.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>-2.0</td>
      <td>-2.0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>-2.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>-1.0</td>
      <td>-2.0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>-2.0</td>
      <td>-3.0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>-3.0</td>
      <td>-2.0</td>
    </tr>
    <tr>
      <th>17</th>
      <td>-2.0</td>
      <td>-3.0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>-3.0</td>
      <td>-4.0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>-4.0</td>
      <td>-4.0</td>
    </tr>
    <tr>
      <th>20</th>
      <td>-4.0</td>
      <td>-4.0</td>
    </tr>
    <tr>
      <th>21</th>
      <td>-4.0</td>
      <td>-5.0</td>
    </tr>
    <tr>
      <th>22</th>
      <td>-5.0</td>
      <td>-6.0</td>
    </tr>
    <tr>
      <th>23</th>
      <td>-6.0</td>
      <td>-7.0</td>
    </tr>
    <tr>
      <th>24</th>
      <td>-7.0</td>
      <td>-8.0</td>
    </tr>
    <tr>
      <th>25</th>
      <td>-8.0</td>
      <td>-9.0</td>
    </tr>
    <tr>
      <th>26</th>
      <td>-9.0</td>
      <td>-9.0</td>
    </tr>
    <tr>
      <th>27</th>
      <td>-9.0</td>
      <td>-10.0</td>
    </tr>
    <tr>
      <th>28</th>
      <td>-10.0</td>
      <td>-11.0</td>
    </tr>
    <tr>
      <th>29</th>
      <td>-11.0</td>
      <td>-11.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>970</th>
      <td>-21.0</td>
      <td>-22.0</td>
    </tr>
    <tr>
      <th>971</th>
      <td>-22.0</td>
      <td>-21.0</td>
    </tr>
    <tr>
      <th>972</th>
      <td>-21.0</td>
      <td>-22.0</td>
    </tr>
    <tr>
      <th>973</th>
      <td>-22.0</td>
      <td>-23.0</td>
    </tr>
    <tr>
      <th>974</th>
      <td>-23.0</td>
      <td>-23.0</td>
    </tr>
    <tr>
      <th>975</th>
      <td>-23.0</td>
      <td>-23.0</td>
    </tr>
    <tr>
      <th>976</th>
      <td>-23.0</td>
      <td>-23.0</td>
    </tr>
    <tr>
      <th>977</th>
      <td>-23.0</td>
      <td>-23.0</td>
    </tr>
    <tr>
      <th>978</th>
      <td>-23.0</td>
      <td>-24.0</td>
    </tr>
    <tr>
      <th>979</th>
      <td>-24.0</td>
      <td>-24.0</td>
    </tr>
    <tr>
      <th>980</th>
      <td>-24.0</td>
      <td>-25.0</td>
    </tr>
    <tr>
      <th>981</th>
      <td>-25.0</td>
      <td>-24.0</td>
    </tr>
    <tr>
      <th>982</th>
      <td>-24.0</td>
      <td>-24.0</td>
    </tr>
    <tr>
      <th>983</th>
      <td>-24.0</td>
      <td>-25.0</td>
    </tr>
    <tr>
      <th>984</th>
      <td>-25.0</td>
      <td>-26.0</td>
    </tr>
    <tr>
      <th>985</th>
      <td>-26.0</td>
      <td>-26.0</td>
    </tr>
    <tr>
      <th>986</th>
      <td>-26.0</td>
      <td>-27.0</td>
    </tr>
    <tr>
      <th>987</th>
      <td>-27.0</td>
      <td>-26.0</td>
    </tr>
    <tr>
      <th>988</th>
      <td>-26.0</td>
      <td>-26.0</td>
    </tr>
    <tr>
      <th>989</th>
      <td>-26.0</td>
      <td>-27.0</td>
    </tr>
    <tr>
      <th>990</th>
      <td>-27.0</td>
      <td>-28.0</td>
    </tr>
    <tr>
      <th>991</th>
      <td>-28.0</td>
      <td>-29.0</td>
    </tr>
    <tr>
      <th>992</th>
      <td>-29.0</td>
      <td>-28.0</td>
    </tr>
    <tr>
      <th>993</th>
      <td>-28.0</td>
      <td>-28.0</td>
    </tr>
    <tr>
      <th>994</th>
      <td>-28.0</td>
      <td>-27.0</td>
    </tr>
    <tr>
      <th>995</th>
      <td>-27.0</td>
      <td>-28.0</td>
    </tr>
    <tr>
      <th>996</th>
      <td>-28.0</td>
      <td>-29.0</td>
    </tr>
    <tr>
      <th>997</th>
      <td>-29.0</td>
      <td>-29.0</td>
    </tr>
    <tr>
      <th>998</th>
      <td>-29.0</td>
      <td>-30.0</td>
    </tr>
    <tr>
      <th>999</th>
      <td>-30.0</td>
      <td>-30.0</td>
    </tr>
  </tbody>
</table>
<p>1000 rows × 2 columns</p>
</div>



## 特定期間で買い


```python
freq = 5 
```
