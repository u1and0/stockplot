import sys
sys.path.append('../bin')
import stockplot as sp

df = sp.datagen(volume=True)
print(df.resample('D').ohlc2().head())

df.columns = (x.upper() for x in df.columns)  # Columns name CAPITAL case
print(df.resample('H').ohlc2().head())
print(df.iloc[:, :4].resample('H').ohlc2().head())  # Drop `volume` column

df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']  # Columns name Capital case
print(df.resample('W').ohlc2().head())

df['Adj Close'] = df.Close * 1.02
print(df.resample('D').ohlc2(close='Adj Close').head())

df.columns = [1, 2, 3, 4, 5, 6]  # Columns name as int
print(df.resample('W').ohlc2(open=1, high=2, low=3, close=6, volume=5).head())

df.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']  # Columns name Capital case
try:
    print(df.drop(['High', 'Volume'], 1).resample('H').ohlc2().head())
    # Drop `High` & `Volume` columns
    # -> raise KeyError: 'Columns not enough high'
except KeyError as e:
    raise KeyError('想定済みエラー{}'.format(e))