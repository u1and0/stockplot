import sys
sys.path.append('./bin/')
import stockplot_quickset
fx = stockplot_quickset.fx  # Set instance

# Resample as Day
fx.resample('D')

# Add indicator
# fx.append('close_10_sma')
# fx.plot()
# for i in range(25, 76, 25):
#     fx.append('close_{}_sma'.format(i))
#     fx.plot()

# Remove indicator
# for i in [13, 11]:
#     fx.remove('close_{}_sma'.format(i))

# # Pop indicator
# fx.pop()
