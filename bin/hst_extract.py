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
    """Convert binary to pandas DataFrame."""
    if filetype in ('old', 'o'):
        size = OLD_FILE_STRUCTURE_SIZE
        fmt = "<iddddd"
    elif filetype in ('new', 'n'):
        size = NEW_FILE_STRUCTURE_SIZE
        fmt = "<Qddddqiq"
    else:
        raise KeyError(filetype)

    # =================np unpack===================
    # nls = np.asarray([np.array(i) for i in chunked(binary[HEADER_SIZE:], size)])  # ndarray
    # struct_array = np.frompyfunc(struct.unpack, 2, 1)  # 動かない
    # bar = struct.unpack(fmt, nls)  # ndarray全要素に対してunpackをかける 動かない
    # =================unpack_from===================
    bar = []
    for i in range(HEADER_SIZE, len(binary), size):
        try:
            unp = list(struct.unpack_from(fmt, binary, i))
            unp[0] = pd.datetime.utcfromtimestamp(unp[0])
            bar.append(unp)
        except Exception:
            pass
    # ===============to DataFrame=====================
    df = pd.DataFrame(bar, columns=['DateTime', 'open', 'high', 'low', 'close', 'volume'])
    df.index = df.DateTime
    df = pd.DataFrame(df.ix[:, ['open', 'high', 'low', 'close', 'volume']])
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
