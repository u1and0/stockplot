

```python
import candlechart as c
```


```python
# 10秒間のtickチャート
c.randomwalk(10, tick=0.01, freq='S')
```




    2017-03-14 00:00:00   -0.01
    2017-03-14 00:00:01   -0.01
    2017-03-14 00:00:02   -0.01
    2017-03-14 00:00:03   -0.02
    2017-03-14 00:00:04   -0.01
    2017-03-14 00:00:05    0.00
    2017-03-14 00:00:06    0.00
    2017-03-14 00:00:07    0.01
    2017-03-14 00:00:08    0.02
    2017-03-14 00:00:09    0.03
    Freq: S, dtype: float64




```python
c.candlechart
```

    ERROR:root:File `'hst_to_df.py'` not found.
    


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-5-0d3c06f9c46f> in <module>()
    ----> 1 import read_hst.read_hst as r
    

    C:\Users\U1and0\Dropbox\Program\python\fxpy\read_hst\read_hst.py in <module>()
         18 # In[1]:
         19 
    ---> 20 df = pd.read_hdf('data/EURUSD.h5', key="main")
         21 df
         22 
    

    NameError: name 'pd' is not defined



```python

```
