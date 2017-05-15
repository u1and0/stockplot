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


def zip2hst(filename, path=None):
    """Extract zip file.
    args:
        filename: zip filename
        path: Extraction directory
    return: Extract filename
    """
    zf = zipfile.ZipFile(filename, 'r')
    path = path if path else os.path.dirname(filename)
    zf.extractall(path=path)
    return path + '/' + zf.namelist()[0]


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


def bin2py(binary, filetype):
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
    # ray = []
    # # for i in chunked(binary, size):
    #     # ray.append(''.join(i))  # 10文字ずつばらばらのbinaryを繋げる
    #     # str(i)
    # bls = [i for i in chunked(binary, size)]
    # nls = np.array(bls)
    # # buf = np.array(ray).T
    # bar = struct.unpack(fmt, buf)

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


def something():
    openTime.append(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(bar[0])))
    openPrice.append(bar[1])
    highPrice.append(bar[2])
    lowPrice.append(bar[3])
    closePrice.append(bar[4])
    volume.append(bar[5])

    dic = {'open_time': open_time, 'open': openPrice, 'high': highPrice,
           'low': lowPrice, 'close': closePrice, 'volume': volume}
    return dic


def dict2df(dic):
    df = pd.DataFrame.from_dict(dic)
    df = df.set_index('open_time')  # open_timeをindexにする
    df.index = pd.to_datetime(df.index)  # 時間軸へ型変更
    df = df.ix[:, ['open', 'high', 'low', 'close', 'volume']]
    return df


def df2pickle(df, filename):
    return df.to_pickle(filename)


def df2hdf(df, filename):
    return df.to_hdf(filename)


if __name__ == "__main__":
    main()
