#!/usr/bin/env python3
""" Handle with 3D, 4D OHLC data """

import pandas as pd


def heat_candle(df: pd.DataFrame) -> pd.Series:
    """Downconvert for making heat map
    descriptions:
        close price is...
            * higher than last close price, then 1
            * higher than last high price, then 2
            * lower than last close price, then -1
            * lower than last low price, then -2
            * as same as last close price, then 0
        return pandas series
    usage:
        heat_candle(df)
    """
    sr = pd.Series(index=df.index)
    sr[df.close > df.shift().close] = 1
    sr[df.close > df.shift().high] = 2
    sr[df.close < df.shift().close] = -1
    sr[df.close < df.shift().low] = -2
    sr.fillna(0, inplace=True)
    return sr


    description:


    usage:
    """
