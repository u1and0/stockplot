#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pandas.core import common as com
import jsm
from stockplot import set_span


# def get_jstock(code, freq='D', start=None, end='last', periods=30)
#     """docstring..."""
#     pass
#     return df


def drange(code, freq='D', start=None, end=None, periods=None):
    freq_dict = {'D': jsm.DAILY, 'W': jsm.WEEKLY, 'M': jsm.MONTHLY}
    # Default args
    if com._count_not_none(start, end, periods) == 0:  # When NO args
        end, periods = 'last', 30

    if com._count_not_none(start, end, periods) != 2:  # Like a pd.date_range Error
        raise ValueError('Must specify two of start, end, or periods')
    if start == 'first':
        data = jsm.Quotes().get_historical_prices(
            code, range_type=freq_dict[freq], all=True)
        start = [i.date for i in data][-1]
    if end == 'last':
        end = pd.datetime.today().date()

    start = start if start else (pd.Period(end, freq) - periods).start_time
    end = end if end else (pd.Period(start, freq) + periods).start_time
    data = jsm.Quotes().get_historical_prices(
            code, range_type=freq_dict[freq], start_date=start, end_date=end)
    df = convert_dataframe(data)
    return df[start:end]


def convert_dataframe(target):
    date = [data.date for data in target]
    open = [data.open for data in target]
    high = [data.high for data in target]
    low = [data.low for data in target]
    close = [data.close for data in target]
    volume = [data.volume for data in target]
    adj_close = [data._adj_close for data in target]
    ar = np.array([open, high, low, close, volume, adj_close])
    df = pd.DataFrame(ar.T, index=date,
                      columns=['open', 'high', 'low', 'close', 'volume', 'adj_close']).sort_index()
    return df


def main():
    df = read_nikkei(9302)
    print(df)


if __name__ == '__main__':
    main()
