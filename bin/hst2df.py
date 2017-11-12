#!/usr/bin/env python
# Coded by Daniel Fernandez
# mechanicalForex.com, asirikuy.com 2015
# http://mechanicalforex.com/2015/12/converting-mt4-binary-history-files-hst-to-csv-using-a-python-script.html

"""
**USAGE**
@ipython

```
run hst_to_csv.py -f <filename>.hst -ty <new | old>
```

type (-ty) は基本的にold
.hstファイルを.h5(hdf5ファイル)に変換してくれるpythonスクリプト
"""

import zipfile
import struct
import time
import pandas as pd
import argparse
import os

HEADER_SIZE = 148
OLD_FILE_STRUCTURE_SIZE = 44
NEW_FILE_STRUCTURE_SIZE = 60


def main():
    filename, input_filetype, output_filetype = file_args()
    print('--- Convert Start ---')
    # print('`{1}` --> `{2}` ---'.format(filename, filename))
    print('Please wait a moment...\n')
    df = binary(filename, input_filetype)
    # df.to_csv(os.path.splitext(filename)[0] + '.csv', header=False)
    df.to_hdf(os.path.splitext(filename)[0] + '.h5', key='main')
    print('\n---End of Convert---')
    print('Using %s.h5 file, type below...' % os.path.splitext(filename)[0])
    print('`df = pd.read_hdf(\"%s.h5\", key="main")`' % os.path.splitext(filename)[0])


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


def zip_extract(file):
    if zipfile.is_zipfile(file):
        with zipfile.ZipFile(file) as z:
            z.extractall()
    else:
        pass



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
                elif filetype == "new":
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
                elif filetype == "new":
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
    main()
