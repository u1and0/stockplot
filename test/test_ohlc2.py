import sys
sys.path.append('../bin')
import stockplot as sp

df = sp.datagen(volume=True)
print(df.resample('D').ohlc2())
df.columns = list(map(lambda x: x.upper(), df.columns))  # Columns name CAPITAL case
print(df.resample('H').ohlc2())
print(df.iloc[:, :4].resample('H').ohlc2())  # Drop `volume` column
df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']  # Columns name Capital case
print(df.resample('W').ohlc2())
print(df.iloc[:, [0, 2, 3]].resample('H').ohlc2())  # Drop `High` columns
    # -> raise KeyError: 'Columns not enough high'
