# Considering shorting is forbidden in China market, change backtest to long_only:
import tushare as ts
import numpy as np
import pandas as pd
import talib
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
 
data = ts.get_k_data(code='hs300', start = '2018-01-01', end = '2023-11-18', ktype = 'D')
data = data.set_index('date')
data.index = pd.to_datetime(data.index)
data = data[['open','close','high','low']]
data['pct'] = data['close'].shift(-1)/data['close']-1

data['fast'] = talib.SMA(data['close'].values, timeperiod = 3)
data['slow'] = talib.WMA(data['close'].values, timeperiod = 50)
data['diff'] = data['fast']-data['slow']
data['rumi'] = talib.SMA(data['diff'].values, timeperiod = 30)
data = data.dropna()

data['strategy_pct']=data.apply(lambda x: x.pct if x.rumi > 0 else 0, axis=1)
data['strategy'] = (1.0 + data['strategy_pct']).cumprod()
data['benchmark'] = (1.0 + data['pct']).cumprod()
annual_return = 100 * (pow(data['strategy'].iloc[-1], 250/data.shape[0]) - 1.0)
print('Annual return for HS300 with RUMI is：%.2f%%' %annual_return)
ax = data[['strategy','benchmark']].plot(title='Selection of HS300 using RUMI')
plt.show()
