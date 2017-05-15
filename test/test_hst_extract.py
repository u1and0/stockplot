import sys
import os
home = os.environ['HOME'] + '/python/stockplot'
sys.path.append('{}/bin/'.format(home))
from hst_extract import zip2hst, bin2dict, hst2bin

# =================zip2hst test===================
# file = ('../data/USDJPY.zip')
# d = zip2hst(file)
# print('Now extracting...')

# d == 'data/USDJPY.zip'
# print('Path is exist?: {}'.format(os.path.exists(d)))
# ====================================

# =================struct.unpack test===================
file = '{}/test/test_bin.txt'.format(home)
bi = hst2bin(file)
li = bin2dict(bi, 'old')
print(li)
# ====================================
