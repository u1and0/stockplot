# IPython log file

import stockstats as ss
from randomwalk import randomwalk
df = randomwalk(10000, freq='T').resample('H').ohlc(); df
# random OHLC made END
import basechart as B
x = B.Base(df)
x.plot()
x.sma('close_5_sma')
x.plot()

