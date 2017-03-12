
# ランダムウォークのシリーズを作成


```python
n = 1000
se = pd.Series(np.random.randint(-1, 2, n)).cumsum()
se.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x25d7820da20>




![png](randomwalk_files/randomwalk_1_1.png)


## 特定期間で買い


```python
freq = 5 
```

## 前日より値が低かったら買い、高かったら見過ごし


```python
position = np.zeros(len(se))  # seと同じ長さの配列を作成
for i in se.index:
    try: 
        if se[i+1] - se[i] > 0:
            position[i]=1
    except:
        
position
```


    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    <ipython-input-7-0a84090b29b1> in <module>()
          1 position = np.zeros(len(se))  # seと同じ長さの配列を作成
          2 for i in se.index:
    ----> 3     if se[i+1] - se[i] > 0:
          4         position[i]=1
          5 position
    

    C:\Anaconda3\lib\site-packages\pandas\core\series.py in __getitem__(self, key)
        601         key = com._apply_if_callable(key, self)
        602         try:
    --> 603             result = self.index.get_value(self, key)
        604 
        605             if not is_scalar(result):
    

    C:\Anaconda3\lib\site-packages\pandas\indexes\base.py in get_value(self, series, key)
       2167         try:
       2168             return self._engine.get_value(s, k,
    -> 2169                                           tz=getattr(series.dtype, 'tz', None))
       2170         except KeyError as e1:
       2171             if len(self) > 0 and self.inferred_type in ['integer', 'boolean']:
    

    pandas\index.pyx in pandas.index.IndexEngine.get_value (pandas\index.c:3557)()
    

    pandas\index.pyx in pandas.index.IndexEngine.get_value (pandas\index.c:3240)()
    

    pandas\index.pyx in pandas.index.IndexEngine.get_loc (pandas\index.c:4279)()
    

    pandas\src\hashtable_class_helper.pxi in pandas.hashtable.Int64HashTable.get_item (pandas\hashtable.c:8564)()
    

    pandas\src\hashtable_class_helper.pxi in pandas.hashtable.Int64HashTable.get_item (pandas\hashtable.c:8508)()
    

    KeyError: 1000



```python

```
