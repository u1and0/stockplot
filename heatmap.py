#!/usr/bin/env python3
""" Handle with 3D, 4D OHLC data """

import pandas as pd
import stockplot as sp


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


def swap_currency(panel: pd.Panel, base: str) -> pd.Panel:
    """
    description:
        panel is XJPY dataframes
        BASE currency vs JPY
        for example
        swap_currency(panel, 'EUR')
        make USDEUR, GBPEUR, AUDEUR, CADEUR, CHFEUR, JPYEUR
    usage:
        ```
        pl = pd.read_pickle('path/to/panel_file.pkl')
        swap_currency(pl, 'CAD').
            to_pickle('/home/vagrant/Data/XCAD-1D-2005-2017.pkl')
        ```
    """
    pl = pd.Panel({
        cur_name[:3]: panel[cur_name] / panel[base + 'JPY']
        for cur_name in panel.drop(base + 'JPY').items
    })
    pl['JPY'] = panel[base + 'JPY'].rdiv(1)
    return pl


def apply_dict(func=lambda x: x, **kwargs):
    """Apply some function to keyword arguments

    description:
        Unless designate `func`, `func` is identity function

    usage:
        apply_dict(
            lambda x: x.resamle('W').ohlc2(),
            USDJPY = read_hst('path/to/USDJPY.zip'),
            EURJPY = read_hst('path/to/EURJPY.zip'),
        )
    """
    return {k: func(v) for k, v in kwargs.items()}
