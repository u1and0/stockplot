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


def zip2hst():
    return hst


def hst2bin(filename):
    with open(filename, 'rb') as f:
        binary = f.read()
    return binary


def bin2df(data):


    data = {'openTime': openTime, 'open': openPrice, 'high': highPrice,
            'low': lowPrice, 'close': closePrice, 'volume': volume}

    result = pd.DataFrame.from_dict(data)
    result = result.set_index('openTime')
    result.index = pd.to_datetime(result.index)
    result = result.ix[:, ['open', 'high', 'low', 'close', 'volume']]
    return df


def df2pickle(df, filename):
    return df.to_pickle(filename)


def df2hdf(df, filename):
    return df.to_hdf(filename)


if __name__ == "__main__":
    main()
