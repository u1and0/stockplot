import pandas as pd
from stockplot import to_unix_time

def set_span(sdf, start=None, end=None, periods=None, freq=None):
    """spanの変更
    引数:
        sdf: indexがdatetimeのデータフレーム
        freq: D | H | T | S <必ず必要>
            * freq入れなくてもここはpassするが、
            * date_rangeのところでNoneだとエラー出る。
            * sdfがすでに指定したいfreqだったときには
            * 無駄なコストなのでchange_freq通さない。
        戻り値: datetime index
    """

    sdf = sdf.copy().change_freq(freq)\
        if freq else sdf.copy()

    # start, end, periodの数は2でなければならない。pd.date_rangeと同じ
    lst = [start, end, periods]
    count_not_none = sum(x is not None for x in lst)
    if count_not_none != 2:  # Like a pd.date_range Error
        raise ValueError('Must specify two of start, end, or periods')

    end = sdf.index[-1] if end is 'last' else end
    start = sdf.index[0] if start is 'first' else start

    # start, end, periodsどれかが与えられていない場合
    if not periods:
        time_span = pd.date_range(start=start, end=end, freq=freq, tz=None,
                                  normalize=False, closed=None)
    elif not end:
        time_span = pd.date_range(start=start, periods=periods, freq=freq,
                                  tz=None, normalize=False, closed=None)
    elif not start:
        time_span = pd.date_range(end=end, periods=periods, freq=freq,
                                  tz=None, normalize=False, closed=None)
    return time_span
