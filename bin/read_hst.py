#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# 何をするためのスクリプト？
ヒストリカルデータをpythonを使用してpandas DataFrameとして読み出したり、csvやpickleに書き込みを行います。


# インストール
[github - u1and0/stockplot](https://github.com/u1and0/stockplot.git)からpullしてください。
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
2. tickdata()関数にダウンロードしたzipファイルのパス、または解凍したhstファイルのパスを入れます。
3. 結果はpandas DataFrameとして返されます。

```python
import read_hst as h
df = h.tickdata('data/USDJPY.zip')  # zipファイルの相対/絶対パス
# hstファイル以外の拡張子が与えられると、展開したhstファイルは削除されます。

df = h.tickdata('data/USDJPY.hst')  # hstファイルの相対/絶対パス
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
`-o pickle`とすればpickleファイル(拡張子はpkl)としても保存できます。

```shell-session
$ cd ~/python/stockplot
$ bin/read_hst.py -f ~/Data/USDJPY.zip -o csv
$ bin/read_hst.py -h
    usage: read_hst.py [-h] [-f FILENAME] [-o OUTPUT_FILETYPE]

    optional arguments:
        -h, --help            show this help message and exit
        -f FILENAME, --filename FILENAME
        -o OUTPUT_FILETYPE, --output-filetype OUTPUT_FILETYPE
```

# 参考
* numpyを使用して高速にバイナリ→テキスト変換 >> [(´・ω・｀；)ﾋｨｨｯ　すいません - pythonでMT4のヒストリファイルを読み込む](http://fatbald.seesaa.net/article/447016624.html)
* 引数読み込み >> [Converting MT4 binary history files: hst to csv using a python script](http://mechanicalforex.com/2015/12/converting-mt4-binary-history-files-hst-to-csv-using-a-python-script.html)
"""
import argparse
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
    return:
        pandas DataFrame
    """
    hstfile = zip2hst(fullpath)  # Extract zip in current directory.
    print('Extracting {}...'.format(hstfile))
    df = read_hst(hstfile)  # Convert binary to pandas DataFrame.
    if not os.path.splitext(fullpath)[1] == '.hst':  # fullpathにhstファイル以外が与えられた場合、ファイルを消す
        os.remove(hstfile)
    return df


def main():
    """Arg parser

    Usage: read_hst.py [-h] [-f FILENAME] [-o OUTPUT_FILETYPE]

    optional arguments:
        -h, --help            show this help message and exit
        -c, --csv
        -p, --pickle

    `stockplot/bin/read_hst.py -f ~/Data/USDJPY.zip -o csv`
    Reading '~/Data/USDJPY.zip' then save to '~/Data/USDJPY.csv' as csv file.
    """
    description = 'Convering historical file (.hst) to csv or pickle file.'
    parser = argparse.ArgumentParser(prog=__file__, description=description)
    parser.add_argument('filenames', nargs='+')  # 1個以上のファイルネーム
    parser.add_argument('-c', '--csv', action='store_true', help='Convert to csv file')
    parser.add_argument('-p', '--pickle', action='store_true', help='Convert to pickle file')

    args = parser.parse_args()
    filenames = args.filenames
    csv = args.csv
    pickle = args.pickle

    if not filenames:
        print("\nEnter a valid filenames\n")
        raise KeyError
    elif not (csv or pickle):
        print("\nEnter a valid output - filetype 'csv' or 'pickle'.\n")
        raise KeyError
    else:
        for filename in filenames:
            df = tickdata(filename)
            basename = os.path.splitext(filename)[0]
            if csv:
                outfile = basename + '.csv'
                df.to_csv(outfile)
                yield outfile
            if pickle:
                outfile = basename + '.pkl'
                df.to_pickle(outfile)
                yield outfile


if __name__ == '__main__':
    print(list(main()))
