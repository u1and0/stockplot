#!/usr/lib/python
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
    """Decide Filename / Filetype"""
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


def zip2hst(filename):
    zf = zipfile.ZipFile(filename, 'r')
    zf.extractall()


def hst2bin(filename):
    """Convert .hst file to binary."""
    with open(filename, 'rb') as f:
        binary = f.read()
    return binary


def bin2dict(data):
    """Convert binary to pandas DataFrame."""

    if filetype == "old":
        bar = struct.unpack("<iddddd", buf)
    if filetype == "new":
        bar = struct.unpack("<Qddddqiq", buf)

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
