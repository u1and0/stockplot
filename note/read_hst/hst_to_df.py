#!/usr/bin/python
# Coded by Daniel Fernandez
# mechanicalForex.com, asirikuy.com 2015
# http://mechanicalforex.com/2015/12/converting-mt4-binary-history-files-hst-to-csv-using-a-python-script.html

"""
**USAGE**
@ipython

```
run hst_to_csv.py -f <filename>.hst -ty <new | old>
type (-ty) は基本的にold
.hstファイルを.h5(hdf5ファイル)に変換してくれるpythonスクリプト
```
"""


import struct
import time
import pandas as pd
import argparse
import os

HEADER_SIZE = 148
OLD_FILE_STRUCTURE_SIZE = 44
NEW_FILE_STRUCTURE_SIZE = 60


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename')
    parser.add_argument('-ty', '--filetype')
    args = parser.parse_args()

    filename = args.filename
    filetype = args.filetype

    if not filename:
        print("Enter a valid filename (-f)")
        exit()

    if filetype != "new" and filetype != "old":
        print("Enter a valid filetype (valid options are old and new)")
        exit()
    return (filename, filetype)


def binary(filename, filetype):
    read = 0
    openTime = []
    openPrice = []
    lowPrice = []
    highPrice = []
    closePrice = []
    volume = []

    with open(filename, 'rb') as f:
        while True:

            if read >= HEADER_SIZE:

                if filetype == "old":
                    buf = f.read(OLD_FILE_STRUCTURE_SIZE)
                    read += OLD_FILE_STRUCTURE_SIZE

                if filetype == "new":
                    buf = f.read(NEW_FILE_STRUCTURE_SIZE)
                    read += NEW_FILE_STRUCTURE_SIZE

                if not buf:
                    break

                if filetype == "old":
                    bar = struct.unpack("<iddddd", buf)
                    openTime.append(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(bar[0])))
                    openPrice.append(bar[1])
                    highPrice.append(bar[3])
                    lowPrice.append(bar[2])
                    closePrice.append(bar[4])
                    volume.append(bar[5])
                if filetype == "new":
                    bar = struct.unpack("<Qddddqiq", buf)
                    openTime.append(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(bar[0])))
                    openPrice.append(bar[1])
                    highPrice.append(bar[2])
                    lowPrice.append(bar[3])
                    closePrice.append(bar[4])
                    volume.append(bar[5])

            else:
                buf = f.read(HEADER_SIZE)
                read += HEADER_SIZE

    data = {'openTime': openTime, 'open': openPrice, 'high': highPrice,
            'low': lowPrice, 'close': closePrice, 'volume': volume}

    result = pd.DataFrame.from_dict(data)
    result = result.set_index('openTime')
    result.index = pd.to_datetime(result.index)
    result = result.ix[:, ['open', 'high', 'low', 'close', 'volume']]
    print(result)
    return result


if __name__ == "__main__":
    filename, filetype = main()
    print('--- Convert Start ---')
    print('`%s` --> `%s.h5` ---' % (filename, os.path.splitext(filename)[0]))
    print('Please wait a moment...\n')
    df = binary(filename, filetype)
    # df.to_csv(os.path.splitext(filename)[0] + '.csv', header=False)
    df.to_hdf(os.path.splitext(filename)[0] + '.h5', key='main')
    print('\n---End of Convert---')
    print('Using %s.h5 file, type below...' % os.path.splitext(filename)[0])
    print('`df = pd.read_hdf(\"%s.h5\", key="main")`' % os.path.splitext(filename)[0])
