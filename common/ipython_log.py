# IPython log file

from randomwalk import randomwalk
df = randomwalk(10000, freq='T').resample('H').ohlc(); df
# random OHLC made END
import basechart
x = basechart.Base(df)
x.plot()
x.add('close_5_sma')
x.plot()

