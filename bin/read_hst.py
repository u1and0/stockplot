#!/usr/bin/env python
"""
# 何をするためのスクリプト？

ヒストリカルデータをpython上で扱いやすい形式へ読み出したり、書き込みを行います。


# データのダウンロード
[FXDD Trading](http://www.fxdd.com/bm/jp/forex-resources/forex-trading-tools/metatrader-1-minute-data/)
というサイトなどからヒストリカルデータ(一分足のティックデータ)の圧縮ファイルをダウンロードしてください。

wget, curl, aria2などのコマンドが使える環境にあれば

```
$ wget http://tools.fxdd.com/tools/M1Data/USDJPY.zip
```

などとしてヒストリカルデータの圧縮ファイルをダウンロードできます。 容量は50MB程度です。


# データの読み出し
zipを解凍すると'.hst'拡張子のヒストリカルデータが得られます。 容量は200MB程度です。
tickdata()関数はこのファイル内のその他の関数をラップしている関数です。

1. zipファイル内のhstファイルをカレントディレクトリに展開
2. hstをバイナリとして読み出す
3. バイナリをpandas DataFrameとして返す


# 使用方法
```
import hst_extract as h
df = h.tickdata('data/USDJPY.zip')  # zipファイルの相対/絶対パス
# hstファイル以外の拡張子が与えられると展開したhstファイルは削除します。

df = h.tickdata('data/USDJPY.hst')  # hstファイルの相対/絶対パス
# hstファイルが直接与えられたらファイルは削除されません。
```
"""
import zipfile
import pandas as pd
import os
import numpy as np


def zip2hst(fullpath):
    """Extract zip file.

    Usage:
        zip2hst('~/data/USDJPY.zip')
        > ~/data/USDJPY.hst
        zip2hst('USDJPY.zip')
        > USDJPY.hst

    args:
        fullpath: Zip filename or path
    return:
        Extract filename or path
    """
    if zipfile.is_zipfile(fullpath):
        with zipfile.ZipFile(fullpath, 'r') as zf:
            zf.extractall()  # zip展開
            ziplist = zf.namelist()
            if not len(ziplist) == 1:
                print('There are {} files in zipfile. Try again.'.format(len(ziplist)))
                raise IOError
        hstfile = ziplist[0]
        return hstfile  # フルパスかファイルネームだけを返す
    else:  # zipファイルでなければそのまま返す
        return fullpath


def read_hst(filepath):
    """numpy使ってbinaryをpandas DataFrame化
    参考: (´・ω・｀；)ﾋｨｨｯ　すいません - pythonでMT4のヒストリファイルを読み込む
    http://fatbald.seesaa.net/article/447016624.html)"""
    with open(filepath, 'rb') as f:
        ver = np.frombuffer(f.read(148)[:4], 'i4')
        if ver == 400:
            dtype = [('time', 'u4'), ('open', 'f8'), ('low', 'f8'),
                     ('high', 'f8'), ('close', 'f8'), ('volume', 'f8')]
            df = pd.DataFrame(np.frombuffer(f.read(), dtype=dtype))
            df = df['time open high low close volume'.split()]
        elif ver == 401:
            dtype = [('time', 'u8'), ('open', 'f8'), ('high', 'f8'), ('low', 'f8'),
                     ('close', 'f8'), ('volume', 'i8'), ('s', 'i4'), ('r', 'i8')]
            df = pd.DataFrame(np.frombuffer(f.read(), dtype=dtype).astype(dtype[:-2]))
        df = df.set_index(pd.to_datetime(df['time'], unit='s')).drop('time', axis=1)
        return df


def tickdata(fullpath):
    """Extracting hst file from zip file.

    Usage:
    import hst_extract as h
    df = h.tickdata('data/USDJPY.zip')

    args:
        fullpath: zip / hst file path
        filetype: 'old' or 'new' default 'old'
        utc: boolen defalt False
    return:
        pandas DataFrame
    """
    hstfile = zip2hst(fullpath)  # Extract zip in current directory.
    print('Extracting {}...'.format(hstfile))
    df = read_hst(hstfile)  # Convert binary to pandas DataFrame.
    if not os.path.splitext(fullpath)[1] == '.hst':  # fullpathにhstファイル以外が与えられた場合、ファイルを消す
        os.remove(hstfile)
    return df
