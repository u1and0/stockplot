import sys
import os
sys.path.append('../bin/')
from hst_extract import zip2hst, bin2py, hst2bin

# =================zip2hst test===================
# file = ('../data/USDJPY.zip')
# d = zip2hst(file)
# print('Now extracting...')

# d == 'data/USDJPY.zip'
# print('Path is exist?: {}'.format(os.path.exists(d)))
# ====================================

# =================struct.unpack test===================
file = 'test_bin.txt'
bi = hst2bin(file)
li = bin2py(bi, 'old')
print(li)
# ====================================
