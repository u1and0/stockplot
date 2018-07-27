#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# 何をするためのスクリプト？
ヒストリカルデータをpythonを使用してpandas DataFrameとして読み出したり、csvやpickleに書き込みを行います。


# インストール
[github - u1and0/stockplot](https://github.com/u1and0/stockplot.git)からcloneしてください。

```shell-session
git clone https://github.com/u1and0/stockplot.git
```

binディレクトリ下のread_hst.pyを使用してください。
その他のファイルは次のページで説明しています。

* [pythonでローソク足(candle chart)の描画](https://qiita.com/u1and0/items/1d9afdb7216c3d2320ef)
* [plotlyでキャンドルチャートプロット](https://qiita.com/u1and0/items/0ebcf097a1d61c636eb9)
* [Plotlyでぐりぐり動かせる為替チャートを作る(1)](https://qiita.com/u1and0/items/e2273bd8e03c670be45a)
* [Plotlyでぐりぐり動かせる為替チャートを作る(2)](https://qiita.com/u1and0/items/b6e1cfba55778d505e7d)


# データのダウンロード
[FXDD Trading](http://www.fxdd.com/bm/jp/forex-resources/forex-trading-tools/metatrader-1-minute-data/) などからヒストリカルデータ(一分足のティックデータ)の圧縮ファイルをダウンロードしてください。

wget, aria2などのコマンドが使える環境にあれば

```
$ wget http://tools.fxdd.com/tools/M1Data/USDJPY.zip
```

などとしてヒストリカルデータの圧縮ファイルをダウンロードできます。 容量は50MB程度です。


# 使用方法

## jupyter notebook や ipython上で使うとき

1. read_hstモジュールをインポートします。
2. read_hst()関数にダウンロードしたzipファイルのパス、または解凍したhstファイルのパスを入れます。
3. 結果はpandas DataFrameとして返されます。

```python
import read_hst as h
df = h.read_hst('data/USDJPY.zip')  # zipファイルの相対/絶対パス
# hstファイル以外の拡張子が与えられると、展開したhstファイルは削除されます。

df = h.read_hst('data/USDJPY.hst')  # hstファイルの相対/絶対パス
# zipを解凍してhstファイルを引数に与えたらファイルを削除しません。

df.tail

                        open     high      low    close  volume
time
2017-11-17 08:32:00  112.573  112.584  112.573  112.581    50.0
2017-11-17 08:33:00  112.581  112.583  112.578  112.580    38.0
2017-11-17 08:34:00  112.580  112.583  112.578  112.580    51.0
2017-11-17 08:35:00  112.580  112.580  112.572  112.572    44.0
2017-11-17 08:36:00  112.572  112.574  112.572  112.572    24.0
```

## bashなどのshell上で使うとき
以下のコマンドは~/Data/USDJPY.zipを~/Data/USDJPY.csvとして保存します。
`-p`とすればpickleファイル(拡張子はpkl)としても保存できます。

```shell-session
$ cd ~/python/stockplot
$ bin/read_hst.py -c ~/Data/USDJPY.zip  # Convert .hst to .csv
$ bin/read_hst.py -h

usage: bin/read_hst.py [-h] [-c] [-p] filenames [filenames ...]

Convering historical file (.hst) to csv or pickle file.

positional arguments:
  filenames

optional arguments:
  -h, --help    show this help message and exit
  -c, --csv     Convert to csv file
  -p, --pickle  Convert to pickle file
```

# 参考
* numpyを使用して高速にバイナリ→テキスト変換 >>
[(´・ω・｀；)ﾋｨｨｯ　すいません - pythonでMT4のヒストリファイルを読み込む](http://fatbald.seesaa.net/article/447016624.html)
* 引数読み込み >>
[Converting MT4 binary history files: hst to csv using a python script](http://mechanicalforex.com/2015/12/converting-mt4-binary-history-files-hst-to-csv-using-a-python-script.html)
"""
import pathlib
import argparse
import zipfile
import numpy as np
import pandas as pd
import stockplot  # for using `ohlc2()`


def zip2hst(fullpath):
    """Extract zip file.

    Usage:
        zip2hst('~/Data/USDJPY.zip')
        > ~/Data/USDJPY.hst
        zip2hst('USDJPY.zip')
        > USDJPY.hst

    args:
        fullpath: Zip filename or path
    return:
        Extract filename or path
    """
    if zipfile.is_zipfile(fullpath):
        with zipfile.ZipFile(fullpath, 'r') as zf:
            zf.extractall()
            ziplist = zf.namelist()
            if not len(ziplist) == 1:
                raise IOError(f'{len(ziplist)} files in zipfile.\
                              Should be 1 file')
            else:
                hstfile = ziplist[0]
        return hstfile  # .hst file name after extracting
    return fullpath  # .hst file name before extracting


def tickdata(filepath):
    """binary to pandas DataFrame using numpy.

    参考: (´・ω・｀；)ﾋｨｨｯ　すいません - pythonでMT4のヒストリファイルを読み込む
    http://fatbald.seesaa.net/article/447016624.html
    """
    with open(filepath, 'rb') as f:
        ver = np.frombuffer(f.read(148)[:4], 'i4')
        if ver == 400:
            dtype = [('time', 'u4'), ('open', 'f8'), ('low', 'f8'),
                     ('high', 'f8'), ('close', 'f8'), ('volume', 'f8')]
            df = pd.DataFrame(np.frombuffer(f.read(), dtype=dtype))
            df = df['time open high low close volume'.split()]
        elif ver == 401:
            dtype = [('time', 'u8'), ('open', 'f8'), ('high', 'f8'),
                     ('low', 'f8'), ('close', 'f8'), ('volume', 'i8'),
                     ('s', 'i4'), ('r', 'i8')]
            df = pd.DataFrame(
                np.frombuffer(f.read(), dtype=dtype).astype(dtype[:-2]))
        df = df.set_index(pd.to_datetime(df['time'], unit='s')).drop(
            'time', axis=1)
        return df


def read_hst(files, freq='T', start=None, end=None):
    """Extracting hst file from zip file.

    usage:
        # one hist file, return pandas DataFrame
        df = read_hst('~/Data/USDJPY.zip')

        # some hist files, return pandas Panel
        panel = read_hst(['~/Data/USDJPY.zip','~/Data/EURJPY.zip'])

    args:
        * hstfiles: historical file path(s), extension is .zip or .hst
        * freq: Resample time frame
        * start: Slice first of time
        * end: Slice last of time

    return:
        pandas DataFrame or Panel
    """
    if isinstance(files, list):
        hst_dict = {
            pathlib.Path(zip_or_hst).stem:  # basename
            read_hst(zip_or_hst, freq=freq, start=start, end=end)  # OHLC
            for zip_or_hst in files
        }  # key is `files` basename, value is OHLC DataFrame
        return pd.Panel(hst_dict)
    else:
        # Extract zip in current directory.
        hstfile = zip2hst(files)
        print('Extracting {}...'.format(hstfile))
        # Convert binary to pandas DataFrame.
        ohlc_data = tickdata(hstfile)
        # Delete unpacked hst file unless extension is ".hst".
        extension = pathlib.Path(files).suffix
        if not extension == '.hst':
            pathlib.Path(hstfile).unlink()  # remove .hst file
        resample_ohlc = ohlc_data.resample(freq).ohlc2().dropna()
        cut_ohlc = resample_ohlc.loc[start:end]
        return cut_ohlc


def main():
    """Arg parser

    usage: bin/read_hst.py [-h] [-c] [-p] filenames [filenames ...]

    Convering historical file (.hst) to csv or pickle file.

    positional arguments:
      filenames

    optional arguments:
      -h, --help    show this help message and exit
      -c, --csv     Convert to csv file
      -p, --pickle  Convert to pickle file


    `stockplot/bin/read_hst.py -cp ~/Data/USDJPY.zip ~/Data/EURUSD.zip`
    Extracting '~/Data/USDJPY.zip' and '~/Data/EURUSD.zip' then save to

    * '~/Data/USDJPY.csv' and '~/Data/EURUSD.csv' as csv file.
    * '~/Data/USDJPY.pkl' and '~/Data/EURUSD.pkl' as pickle file.
    """
    description = 'Convering historical file (.hst) to csv or pickle file.'
    parser = argparse.ArgumentParser(prog=__file__, description=description)
    parser.add_argument('filenames', nargs='+')  # 1個以上のファイルネーム
    parser.add_argument(
        '-c', '--csv', action='store_true', help='Convert to csv file')
    parser.add_argument(
        '-p', '--pickle', action='store_true', help='Convert to pickle file')

    args = parser.parse_args()
    filenames = args.filenames
    csv = args.csv
    pickle = args.pickle

    if not filenames:
        raise KeyError("Enter a valid filenames")
    elif not (csv or pickle):
        raise KeyError(
            "Enter a valid output - filetype '-c'(--csv) or '-p'(--pickle).")
    else:
        for filename in filenames:
            df = read_hst(filename)  # convert historical to pandas Dataframe
            basename = pathlib.Path(filename).stem
            if csv:
                outfile = basename + '.csv'
                df.to_csv(outfile)
                yield outfile
            if pickle:
                outfile = basename + '.pkl'
                df.to_pickle(outfile)
                yield outfile


if __name__ == '__main__':
    for convert_filename in main():
        print(convert_filename)
