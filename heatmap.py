#!/usr/bin/env python3
""" Handle with 3D, 4D OHLC data """

import pandas as pd


def applydict(func=lambda x: x, **kwargs):
    """Apply some function to keyword arguments

    description:
        Unless designate `func`, `func` is identity function

    usage:
        # same as dict() function
        >>> applydict(apple=5, orrange=10)
        {'apple': 5, 'orrange': 10}

        # apply some function to dict
        >>> applydict(func=lambda x**2, apple=5, orrange=10)
        {'apple': 25, 'orrange': 100}

        >>> def pow_plus(x, n):
                return x**2 + n
        >>> applydict(lambda x: powplus(x,2), apple=5, orrange=10)
        {'apple': 27, 'orrange': 102}
    """
    return {k: func(v) for k, v in kwargs.items()}


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


# pd.DataFrame.heat_candle() -> make Series
# pd.Panel.heat_candle() -> make DataFrame
setattr(pd.DataFrame, 'heat_candle', heat_candle)
setattr(pd.Panel, 'heat_candle',
        lambda x: pd.DataFrame(applydict(heat_candle, **x)))


def cross_currency(panel, freq: str, base=None):
    """Panel OHLC resampler
    If base , change base currency from JPY to other.
    If not base, return JPY based panel.

    usage:
        pl = pd.Panel(...)
        pl.cross_currency('W')  # 週足に変換
    ohlc2と呼び出し方が違うので注意

    Convert 1 min panel to another base currency

    description:
        Function for calculating cross USD from cross JPY
        EURUSD = EURJPY / USDJPY so `base='USDJPY'`

    args:
        panel: cross currency panel XJPY
        base: if dorrer base then 'USDJPY'
        freq: resample frequency

    usage:
        >>> pl = pd.read_pickle('~/Data/XJPY1m-2005-2018.pkl')
        >>> cross_currency(panel=xjpy, base='USDJPY', freq='D')

    # USD cross
        EURUSD = EURJPY / USDJPY
        JPYUSD =      1 / USDJPY
        GBPUSD = GBPJPY / USDJPY
        CADUSD = CADJPY / USDJPY
        CHFUSD = CHFJPY / USDJPY
        AUDUSD = AUDJPY / USDJPY
    # EUR cross
        USDEUR = USDJPY / EURJPY
        JPYEUR =      1 / EURJPY
        GBPEUR = GBPJPY / EURJPY
        CADEUR = CADJPY / EURJPY
        CHFEUR = CHFJPY / EURJPY
        AUDEUR = AUDJPY / EURJPY
    # GBP cross
        USDGBP = USDJPY / GBPJPY
        EURGBP = EURJPY / GBPJPY
        JPYGBP =      1 / GBPJPY
        CADGBP = CADJPY / GBPJPY
        CHFGBP = CHFJPY / GBPJPY
        AUDGBP = AUDJPY / GBPJPY
    # CAD cross
        USDCAD = USDJPY / CADJPY
        EURCAD = EURJPY / CADJPY
        JPYCAD =      1 / CADJPY
        GBPCAD = GBPJPY / CADJPY
        CHFCAD = CHFJPY / CADJPY
        AUDCAD = AUDJPY / CADJPY
    # CHF cross
        USDCHF = USDJPY / CHFJPY
        EURCHF = EURJPY / CHFJPY
        JPYCHF =      1 / CHFJPY
        GBPCHF = GBPJPY / CHFJPY
        CADCHF = CADJPY / CHFJPY
        AUDCHF = AUDJPY / CHFJPY
    # AUD cross
        USDAUD = USDJPY / AUDJPY
        EURAUD = EURJPY / AUDJPY
        JPYAUD =      1 / AUDJPY
        GBPAUD = GBPJPY / AUDJPY
        CADAUD = CADJPY / AUDJPY
        CHFAUD = CHFJPY / AUDJPY
    """
    if base:
        cross_panel = {}
        # Add all item/base (AUDUSD = AUDJPY / USDJPY)
        for item in panel.items:
            if not item == base:  # except USDUSD
                cross_close = panel[item, :, 'close'] / panel[base, :, 'close']
                new_name = item[:3] + base[:3]
                cross_panel[new_name] =\
                    cross_close.resample(freq).ohlc(
                ).dropna()  # Add OHLC in panel
        # Add 1/base (JPYUSD = 1 / USDJPY)
        reverse_name = base[3:] + base[:3]
        reverse_close = panel[base].rdiv(1)['close']
        cross_panel[reverse_name] =\
            reverse_close.resample(freq).ohlc().dropna()  # Add OHLC in panel
        return pd.Panel(cross_panel)
    else:
        adict = applydict(lambda x: x.resample(freq).ohlc2(), **panel)
        return pd.Panel(adict)


# USAGE: xjpy.cross_currency('USDJPY', 'D') <- based USD, resample daily
setattr(pd.Panel, 'cross_currency', cross_currency)


class HeatCandle(pd.Panel):
    def __init__(self, freq, base=None, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
