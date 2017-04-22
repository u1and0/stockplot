#!/bin/bash
import numpy as np
import pandas as pd


def randomwalk(periods, start=pd.datetime.today().date(), index=None, name=None, tick=1, freq='B'):
    """periods日分だけランダムウォークを返す"""
    if not index:
        index = pd.date_range(start=start, periods=periods, freq=freq)  # 今日の日付からperiod日分の平日
    bullbear = pd.Series(tick * np.random.randint(-1, 2, periods),
                         index=index, name=name)  # unit * (-1,0,1のどれか)を吐き出すSeries
    price = bullbear.cumsum()  # 累積和
    return price
