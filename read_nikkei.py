#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pandas.core import common as com
import jsm
from .stockplot import set_span


def get_jstock(code, freq='D', start=None, end=None, periods=None):
    """get Japanese stock data using jsm
    Usage:
        `get_jstock(6502)`
        To get TOSHIBA daily from today back to 30days except holiday.

        `get_jstock(6502, 'W', start=pd.Timestamp('2016'), end=pd.Timestamp('2017'))`
        To get TOSHIBA weekly from 2016-01-01 to 2017-01-01.

        `get_jstock(6502, end=pd.Timestamp('20170201'), periods=50)`
        To get TOSHIBA daily from 2017-02-01 back to 50days except holiday.

        `get_jstock(6502, 'M', start='first', end='last')`
        To get TOSHIBA monthly from 2000-01-01 (the date of start recording) to today.
    """
    # Default args
    if com._count_not_none(start, end, periods) == 0:  # All of args is None
        end, periods = 'last', 30

    # Switch frequency Dayly, Weekly or Monthly
    freq_dict = {'D': jsm.DAILY, 'W': jsm.WEEKLY, 'M': jsm.MONTHLY}

    # 'first' means the start of recording date
    if start == 'first':
        data = jsm.Quotes().get_historical_prices(
            code, range_type=freq_dict[freq], all=True)
        start = [i.date for i in data][-1]
    else:
        data = None  # Temporaly defined

    # 'last' means last weekday (or today)
    if end == 'last':
        end = pd.datetime.today()

    # Return "start" and "end"
    start, end = (x.date() if hasattr(x, 'date') else x
                  for x in set_span(start, end, periods, freq))
    print('Get data from {} to {}'.format(start, end))

    data = jsm.Quotes().get_historical_prices(
        code, range_type=freq_dict[freq], start_date=start,
        end_date=end) if not data else data
    df = _convert_dataframe(data)
    return df[start:end]


def _convert_dataframe(target):
    """Convert <jsm.pricebase.PriceData> to <pandas.DataFrame>"""
    date = [_.date for _ in target]
    open = [_.open for _ in target]
    high = [_.high for _ in target]
    low = [_.low for _ in target]
    close = [_.close for _ in target]
    adj_close = [_._adj_close for _ in target]
    volume = [_.volume for _ in target]
    data = {
        'Open': open,
        'High': high,
        'Low': low,
        'Close': close,
        'Adj Close': adj_close,
        'Volume': volume
    }
    columns = *data.keys(),
    df = pd.DataFrame(data, index=date, columns=columns).sort_index()
    df.index.name = 'Date'
    return df
