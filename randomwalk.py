import numpy as np
import pandas as pd


def randomwalk(periods=None, start=None, end=None, freq='B', tz=None,
               normalize=False, name=None, closed=None, tick=1, **kwargs):
    """Returns random up/down pandas Series.

    Usage:
        ```
        import datetime
        randomwalk(100)  # Returns +-1up/down 100days from now.
        randomwalk(100, freq='H')  # Returns +-1up/down 100hours from now.
        randomwalk(100, ,tick=0.1 freq='S')  # Returns +-0.1up/down 100seconds from now.
        randomwalk(100, start=datetime.datetime.today())  # Returns +-1up/down 100days from now.
        randomwalk(100, end=datetime.datetime.today())
            # Returns +-1up/down back to 100 days from now.
        randomwalk(start=datetime.datetime(2000,1,1), end=datetime.datetime.today())
            # Returns +-1up/down from 2000-1-1 to now.
        randomwalk(100, freq='H').resample('D').ohlc()  # random OHLC data
        ```

    Args:
        periods: int
        start: start time (default datetime.now())
        end: end time
        freq: ('M','W','D','B','H','T','S') (default 'B')
        tz: time zone
        tick: up/down unit size (default 1)

    Returns:
        pandas Series with datetime index
    """
    if not start and not end:
        start = pd.datetime.today().date()  # default arg of `start`
    index = pd.DatetimeIndex(start=start, end=end, periods=periods, freq=freq, tz=tz,
                             normalize=normalize, name=name, closed=closed, **kwargs)
    bullbear = pd.Series(tick * np.random.randint(-1, 2, len(index)),
                         index=index, name=name, **kwargs)  # tick * (-1,0,1のどれか)
    price = bullbear.cumsum()  # 累積和
    return price
