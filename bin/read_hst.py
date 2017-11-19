#!/usr/bin/env python
"""
# 何をするためのスクリプト？

ヒストリカルデータをpython上で扱いやすい形式へ読み出したり、書き込みを行います。


# データのダウンロード
[FXDD Trading](http://www.fxdd.com/bm/jp/forex-resources/forex-trading-tools/metatrader-1-minute-data/) というサイトなどからヒストリカルデータ(一分足のティックデータ)の圧縮ファイルをダウンロードしてください。

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
df = h.tickdata('data/USDJPY.hst')  # hstファイルの相対/絶対パス。ただし、hstファイルは削除されます。
```
"""
import zipfile
import struct
import pandas as pd
import os

HEADER_SIZE = 148
OLD_FILE_STRUCTURE_SIZE = 44
NEW_FILE_STRUCTURE_SIZE = 60


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


def bin2df(binary, filetype, utc):
    """Convert binary to pandas DataFrame.

    args:
        binary: readed hst file as binary
        filetype: 'old' or 'new' default 'old'
        utc: boolen defalt False
    return:
        pandas DataFrame
    """
    if filetype in ('old', 'o'):
        size = OLD_FILE_STRUCTURE_SIZE
        fmt = "<iddddd"
    elif filetype in ('new', 'n'):
        size = NEW_FILE_STRUCTURE_SIZE
        fmt = "<Qddddqiq"
    else:
        raise KeyError(filetype)
    bar = []
    for i in range(HEADER_SIZE, len(binary), size):
        unp = list(struct.unpack_from(fmt, binary, i))
        unp[0] = pd.datetime.utcfromtimestamp(unp[0]) if utc else pd.datetime.fromtimestamp(unp[0])
        bar.append(unp)
    df = pd.DataFrame(bar, columns=['DateTime', 'open', 'high', 'low', 'close', 'volume'])
    df.index = df.DateTime
    df = pd.DataFrame(df.loc[:, ['open', 'high', 'low', 'close', 'volume']])
    return df


def tickdata(fullpath, filetype='old', utc=False):
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
    with open(hstfile, 'rb') as f:
        binary = f.read()
        df = bin2df(binary, filetype, utc)  # Convert binary to pandas DataFrame.
    os.remove(hstfile)
    return df
