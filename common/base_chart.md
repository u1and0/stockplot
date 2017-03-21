

```python
import numpy as np
import pandas as pd
from datetime import datetime
from randomwalk import *
from plotly.tools import FigureFactory as FF
import plotly.offline as pyo
import plotly.graph_objs as pyg
pyo.init_notebook_mode(connected=True)


class base:
    """candlec chartとその指標を描くクラス
    入力: ohlcデータフレーム
    出力: plrtolyファイル(htmlファイル)"""

    def __init__(self, df):
        self.df = df
        self.add_line = []
        # self.dt = dt
        self.fig = self.fig()

    # ----------DATA MAKE----------

    # resampleは中でやったほうがいいのか外でやったほうがいいのか
    # def resamp(self, ashi):
    #     return df.ix[:, :4].resample(ashi).agg({'open':'first',
    #                                          'high':'max', 'low':'min', 'close':'last'}).dropna()

    def sma(self, window, columns='close'):
        # adding = pyg.Scatter(x=self.df.index, y=ro, name='SMA5', line=pyg.Line(color='r'))
        # self.add_line.extend(list(adding))
        self.df['sma%d'% window] = self.df[columns].rolling(window).mean()
        return self.df

    # ---------PLOT----------
    def fig(self):
        return FF.create_candlestick(self.df.open, self.df.high,
                                     self.df.low, self.df.close, dates=self.df.index)
    def indicator(self):
        add_line = [pyg.Scatter(x=self.df.index, y=self.df.ix[:, 4:].value, name='SMA', line=pyg.Line(color='r'))]
        self.fig['data'].extend(add_line)

    def plot(self, filename='candlestick_and_trace.html'):
        self.indicator()
        self.fig['layout'].update(xaxis={'showgrid': True})
        pyo.iplot(self.fig, filename=filename, validate=False)

if __name__ == '__main__':
    np.random.seed(1)
    df = randomwalk(60 * 24 * 90, freq='T', tick=0.01,
                    start=pd.datetime(2017, 3, 20)).resample('B').ohlc() + 115
    x = base(df)  # ohlcをbaseに渡す
    k = x.sma(5)
    print(k.head(5))
    x.plot()

```


<script>requirejs.config({paths: { 'plotly': ['https://cdn.plot.ly/plotly-latest.min']},});if(!window.Plotly) {{require(['plotly'],function(plotly) {window.Plotly=plotly;});}}</script>


                  open    high     low   close     sma5
    2017-03-20  115.00  115.38  114.76  115.36      NaN
    2017-03-21  115.37  115.49  115.03  115.15      NaN
    2017-03-22  115.14  115.69  115.07  115.65      NaN
    2017-03-23  115.66  116.22  115.64  116.21      NaN
    2017-03-24  116.20  116.53  115.90  116.31  115.736
    


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-1-4616dc8a5cd3> in <module>()
         53     k = x.sma(5)
         54     print(k.head(5))
    ---> 55     x.plot()
    

    <ipython-input-1-4616dc8a5cd3> in plot(self, filename)
         42 
         43     def plot(self, filename='candlestick_and_trace.html'):
    ---> 44         self.indicator()
         45         self.fig['layout'].update(xaxis={'showgrid': True})
         46         pyo.iplot(self.fig, filename=filename, validate=False)
    

    <ipython-input-1-4616dc8a5cd3> in indicator(self)
         38                                      self.df.low, self.df.close, dates=self.df.index)
         39     def indicator(self):
    ---> 40         add_line = [pyg.Scatter(x=self.df.index, y=self.df.ix[:, 4:].value, name='SMA', line=pyg.Line(color='r'))]
         41         self.fig['data'].extend(add_line)
         42 
    

    C:\Anaconda3\lib\site-packages\pandas\core\generic.py in __getattr__(self, name)
       2742             if name in self._info_axis:
       2743                 return self[name]
    -> 2744             return object.__getattribute__(self, name)
       2745 
       2746     def __setattr__(self, name, value):
    

    AttributeError: 'DataFrame' object has no attribute 'value'



```python
np.array(df.ix[:, 4:])
```




    array([[     nan],
           [     nan],
           [     nan],
           [     nan],
           [ 115.736],
           [ 115.858],
           [ 116.044],
           [ 116.118],
           [ 116.076],
           [ 116.078],
           [ 116.206],
           [ 116.288],
           [ 116.4  ],
           [ 116.498],
           [ 116.446],
           [ 116.318],
           [ 116.072],
           [ 115.856],
           [ 115.684],
           [ 115.642],
           [ 115.502],
           [ 115.512],
           [ 115.438],
           [ 115.268],
           [ 115.056],
           [ 115.03 ],
           [ 115.018],
           [ 115.05 ],
           [ 115.198],
           [ 115.226],
           [ 115.118],
           [ 115.03 ],
           [ 114.986],
           [ 114.81 ],
           [ 114.602],
           [ 114.394],
           [ 114.066],
           [ 113.732],
           [ 113.474],
           [ 113.28 ],
           [ 113.138],
           [ 113.108],
           [ 113.158],
           [ 113.332],
           [ 113.716],
           [ 114.106],
           [ 114.36 ],
           [ 114.474],
           [ 114.494],
           [ 114.398],
           [ 114.414],
           [ 114.458],
           [ 114.438],
           [ 114.428],
           [ 114.482],
           [ 114.418],
           [ 114.552],
           [ 114.654],
           [ 114.742],
           [ 114.678],
           [ 114.652],
           [ 114.53 ],
           [ 114.458],
           [ 114.34 ],
           [ 114.308]])




```python
df.close.rolling(25).mean()
```




    2017-03-20         NaN
    2017-03-21         NaN
    2017-03-22         NaN
    2017-03-23         NaN
    2017-03-24         NaN
    2017-03-27         NaN
    2017-03-28         NaN
    2017-03-29         NaN
    2017-03-30         NaN
    2017-03-31         NaN
    2017-04-03         NaN
    2017-04-04         NaN
    2017-04-05         NaN
    2017-04-06         NaN
    2017-04-07         NaN
    2017-04-10         NaN
    2017-04-11         NaN
    2017-04-12         NaN
    2017-04-13         NaN
    2017-04-14         NaN
    2017-04-17         NaN
    2017-04-18         NaN
    2017-04-19         NaN
    2017-04-20         NaN
    2017-04-21    115.7916
    2017-04-24    115.7828
    2017-04-25    115.7868
    2017-04-26    115.7724
    2017-04-27    115.7448
    2017-04-28    115.6896
                    ...   
    2017-05-08    115.2724
    2017-05-09    115.1396
    2017-05-10    115.0124
    2017-05-11    114.8868
    2017-05-12    114.7612
    2017-05-15    114.6364
    2017-05-16    114.5468
    2017-05-17    114.4728
    2017-05-18    114.4164
    2017-05-19    114.3760
    2017-05-22    114.3572
    2017-05-23    114.3164
    2017-05-24    114.2800
    2017-05-25    114.2616
    2017-05-26    114.2444
    2017-05-29    114.2340
    2017-05-30    114.2044
    2017-05-31    114.1576
    2017-06-01    114.1076
    2017-06-02    114.0956
    2017-06-05    114.0940
    2017-06-06    114.1088
    2017-06-07    114.0912
    2017-06-08    114.0940
    2017-06-09    114.1108
    2017-06-12    114.1456
    2017-06-13    114.2016
    2017-06-14    114.2364
    2017-06-15    114.2672
    2017-06-16    114.3164
    Freq: B, Name: close, dtype: float64




```python

```
