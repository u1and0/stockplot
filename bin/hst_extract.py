#!/usr/lib/python
import numpy as np
from more_itertools import chunked
import zipfile
import struct
import time
import pandas as pd
import argparse
import os

HEADER_SIZE = 148
OLD_FILE_STRUCTURE_SIZE = 44
NEW_FILE_STRUCTURE_SIZE = 60


def file_args():
    """Decide Filename / Filetype
    # TODO
    -zh --zip-to-hst
    -zf --zip-to-hdf
    -zp --zip-to-pickle
    -hp --hst-to-pickle
    -hf --hst-to-hdf

    * あとファイル形式からpd.DataFrame, binaryまでに変換する奴
        * 関数を呼ぶだけでいいのか？
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename')
    parser.add_argument('-i', '--input-filetype')
    parser.add_argument('-o', '--output-filetype')
    args = parser.parse_args()

    filename = args.filename
    input_filetype = args.input_filetype
    output_filetype = args.output_filetype if args.output_filetype\
        else 'pickle'  # Default is 'pickle' file

    if not filename:
        print("Enter a valid filename (-f)")
        exit()
    if input_filetype != "new" and input_filetype != "old":
        print("Enter a valid input-filetype (valid options are 'old' or 'new')")
        exit()
    elif output_filetype != "hdf" and output_filetype != "pickle":
        print("Enter a valid output - filetype\
              (valid options are 'pickle' or 'hdf', Default is pickle.)")
        exit()
    return (filename, input_filetype, output_filetype)


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
            assert len(ziplist) == 1,\
                'There are {} files in zipfile. Try again.'.format(len(ziplist))
        pathname = os.path.dirname(fullpath)
        hstfile = ziplist[0]
        return pathname + '/' + hstfile if pathname else hstfile  # フルパスかファイルネームだけを返す
    else:  # zipファイルでなければそのまま返す
        # print('{} is not zip file.'.format(filename))
        return fullpath


def hst2bin(filename):
    """Convert .hst file to binary."""
    with open(filename, 'rb') as f:
        binary = f.read()
    return binary


# def zip2bin(filename):
#     hstfiles = zip2hst(filename)
#     for hstfile in hstfiles:
#         binary = hst2bin(hstfile)
#         os.remove(hstfile)  # remove hst files
#         yield binary


def bin2df(binary, filetype):
    """Convert binary to pandas DataFrame.
    # for文によるループ
    4.78 s ± 74.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

    ```
    %%timeit
    bar=[]
    for i in range(HEADER_SIZE, len(binary), size):
        unp = list(struct.unpack_from(fmt, binary, i))
        unp[0] = pd.datetime.utcfromtimestamp(unp[0])
        bar.append(unp)
    ```

    ```

    # 内包方表記による
    5.14 s ± 17.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

    ```
    %%timeit
    ar = np.asarray([struct.unpack_from(fmt, binary, i)  # numpy.arrayとして返す
           for i in range(HEADER_SIZE, len(binary), size)])  # 内包表記で一挙にbinaryを解凍

    ```

    %timeitによる測定が、内包表記よる方法では止まる
    単純にforループを用いた方法を使おうと思う
    """
    if filetype in ('old', 'o'):
        size = OLD_FILE_STRUCTURE_SIZE
        fmt = "<iddddd"
    elif filetype in ('new', 'n'):
        size = NEW_FILE_STRUCTURE_SIZE
        fmt = "<Qddddqiq"
    else:
        raise KeyError(filetype)
    # =================1. 内包表記によるループ===================
    # ====47.1 s ± 312 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)====
    # ====↓to_datetime消した場合====
    # ====4.98 s ± 13.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) ====
    # ====↓datetime.fromtimestamp使用した場合====
    # ====16.1 s ± 63.4 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)====
    # ar = np.asarray([struct.unpack_from(fmt, binary, i)  # numpy.arrayとして返す
    #                  for i in range(HEADER_SIZE, len(binary), size)])  # 内包表記でbinaryを解凍
    # ar_index = [pd.datetime.fromtimestamp(i) for i in ar[:, 0]]
    # df = pd.DataFrame(ar[:, 1:], index=ar_index,
    #                   columns=['open', 'low', 'high', 'close', 'volume'])  # データフレーム化
    # =================2. for文によるループ===================
    # ====7.76 s ± 440 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)====
    # ====7.44 s ± 107 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) =====
    bar = []
    for i in range(HEADER_SIZE, len(binary), size):
        unp = list(struct.unpack_from(fmt, binary, i))
        unp[0] = pd.datetime.utcfromtimestamp(unp[0])
        bar.append(unp)
    df = pd.DataFrame(bar, columns=['DateTime', 'open', 'high', 'low', 'close', 'volume'])
    df.index = df.DateTime
    df = pd.DataFrame(df.loc[:, ['open', 'high', 'low', 'close', 'volume']])
    # =================3. mapを使う===================
    # ====48.5 s ± 540 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) ====
    # ====↓to_datetime消した場合====
    # ====5.59 s ± 14.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)====
    # ====↓datetime.fromtimestamp使用した場合====
    # ====17 s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)====
    # binary_list = [binary[i:i + size] for i in range(HEADER_SIZE, len(binary), size)]  # binary切り出し
    # binary_map = map(lambda x: struct.unpack(fmt, x), binary_list)  # mapで一気にunpack
    # binary_array = np.asarray(list(binary_map))  # np.array化
    # ar_index = [pd.datetime.fromtimestamp(i) for i in binary_array[:, 0]]
    # df = pd.DataFrame(binary_array[:, 1:], index=ar_index,
    #                   columns=['open', 'low', 'high', 'close', 'volume'])  # データフレーム化
    return df


# def something():
#     openTime.append(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(bar[0])))
#     openPrice.append(bar[1])
#     highPrice.append(bar[2])
#     lowPrice.append(bar[3])
#     closePrice.append(bar[4])
#     volume.append(bar[5])

#     dic = {'open_time': open_time, 'open': openPrice, 'high': highPrice,
#            'low': lowPrice, 'close': closePrice, 'volume': volume}
#     return dic


# def dict2df(dic):
#     df = pd.DataFrame.from_dict(dic)
#     df = df.set_index('open_time')  # open_timeをindexにする
#     df.index = pd.to_datetime(df.index)  # 時間軸へ型変更
#     df = df.ix[:, ['open', 'high', 'low', 'close', 'volume']]
#     return df


def df2pickle(df, filename):
    return df.to_pickle(filename)


def df2hdf(df, filename):
    return df.to_hdf(filename, key='main')


if __name__ == "__main__":
    main()
