import pandas as pd
from stockplot import to_unix_time


def set_span(sdf, start=None, end=None, periods=None, freq=None, tz=None,
             normalize=False, closed=None, **kwargs):
    """spanの変更
    引数:
        sdf: indexがdatetimeのデータフレーム
        freq: M | W | D | H | T | S <必ず必要>
            * freq入れなくてもここはpassするが、
            * date_rangeのところでNoneだとエラー出る。
            * sdfがすでに指定したいfreqだったときには
            * 無駄なコストなのでchange_freq通さない。
        戻り値: datetime index
    """

    # Args check
    count_not_none = sum(x is not None for x in [start, end, periods])
    if count_not_none != 2:  # Like a pd.date_range Error
        raise ValueError('Must specify two of start, end, or periods')

    source = sdf.copy().change_freq(freq)  # if freq else sdf.copy()
    end = source.index[-1] if end == 'last' else end
    start = source.index[0] if start == 'first' else start

    # start, end, periodsどれかが与えられていない場合
    if not periods:
        time_span = pd.date_range(start=start, end=end, freq=freq, tz=None,
                                  normalize=False, closed=None, **kwargs)
    elif not end:
        time_span = pd.date_range(start=start, periods=periods, freq=freq,
                                  tz=None, normalize=False, closed=None, **kwargs)
    elif not start:
        time_span = pd.date_range(end=end, periods=periods, freq=freq,
                                  tz=None, normalize=False, closed=None, **kwargs)
    return time_span
