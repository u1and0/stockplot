import sys
sys.path.append('../common/')
import numpy as np
import pandas as pd
import pandas.core.common as com
from randomwalk import randomwalk


def set_span(start=None, end=None, periods=None, freq='D'):
    """ 引数のstart, end, periodsに対して
    startとendの時間を返す。

    * start, end, periods合わせて2つの引数が指定されていなければエラー
    * start, endが指定されていたらそのまま返す
    * start, periodsが指定されていたら、endを計算する
    * end, periodsが指定されていたら、startを計算する
    """
    if com._count_not_none(start, end, periods) != 2:  # Like a pd.date_range Error
        raise ValueError('Must specify two of start, end, or periods')
    start = start if start else (pd.Period(end, freq) - periods).start_time
    end = end if end else (pd.Period(start, freq) + periods).start_time
    return start, end

if __name__ == '__main__':
    # Make sample data
    np.random.seed(1)
    df = randomwalk(60 * 60 * 24 * 90, freq='S', tick=0.01,
                    start=pd.datetime(2017, 3, 20)).resample('T').ohlc() + 115  # 90日分の1分足を日足に直す
    freq = '1D6H39T23S'  # 1日と6時間39分23秒足
    dfs = df.resample(freq).agg({'open': 'first', 'high': 'max',
                                 'low': 'min', 'close': 'last'}).dropna()  # freqの足にコンバート

    # Set span
    ss, ee = set_span(periods=20, end=pd.Timestamp('201706012200'), freq=freq)
    # 2017/6/1 22:00:00から20足分後ろ

    print('starttime, endtime=', ss, ee)
    dfloc = dfs.loc[ss:ee]
    print(dfloc)
