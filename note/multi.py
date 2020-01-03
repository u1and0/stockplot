#!/usr/bin/env python3
import glob
import os
import pandas as pd
import stockplot as sp
FILES = glob.glob('/home/vagrant/Data/*JPY.zip')  # get JPY files
FILE_DICT = {os.path.basename(i)[:-4]: i for i in FILES}


class StockPanel:
    """usage:
        files = glob.glob('/home/vagrant/Data/*JPY.zip')
        sl = StockPanel(files, freq='H', start=None, end=pd.datetime.today())
        """

    def __init__(self,
                 filelist,
                 freq='M',
                 start=pd.Timestamp('2016'),
                 end=None):
        self.freq = freq
        self.start = start
        self.end = end

        self.data = self.file_dict(filelist)
        self.dict = self.hst_to_dict(**self.data)
        self = pd.Panel(self.dict)

    def freq_comp(self, path):
        """read historical data from path
        * resample Daily
        * drop nan data rows
        """
        df = sp.read_hst.read_hst(path).\
            resample(self.freq).\
            ohlc2().\
            loc[self.start:self.end]
        return df

    def file_dict(self, files):
        """make path dict
        {'USDJPY': 'path/to/USDJPY.zip',}
        usage:
            file_dict(glob.glob(~/Data/*JPY,zip))
        """
        return {os.path.basename(f)[:-4]: f for f in files}

    def hst_to_dict(self, **kwargs):
        """filepath to dict of DataFrame
        read multiple historical data's filepath
        then convert to dict of DataFrame

        usage:
            hst_to_dict(USDJPY='path/to/USDJPY.zip',
                        EURJPY='path/to/EURJPY.zip')
        """
        return {k: self.freq_comp(v) for k, v in kwargs.items()}


def hst_multiindex(**kwargs):
    """read multiple columns DataFrame
    usage:
        mdf = hst_multiindex(
            USDJPY=freq_comp('path/to/data/USDJPY.zip').loc[pd.Time('2016'):],
            EURJPY=freq_comp('path/to/data/EURJPY.zip').loc[pd.Time('2016'):]
            )
    """
    s, e = pd.Period(2016).start_time, pd.Period(2017).end_time
    index = pd.date_range(s, e)
    columns = pd.MultiIndex.from_product(
        [kwargs.keys(), ['open', 'high', 'low', 'close', 'volume']],
        names=['currency', 'ohlcv'])
    df = pd.DataFrame(None, index=index, columns=columns)
    for k in kwargs.keys():
        df[k] = kwargs[k]
    return df
