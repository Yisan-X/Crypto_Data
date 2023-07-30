from datetime import *
from tkinter.messagebox import RETRY

YEARS = ['2017', '2018', '2019', '2020', '2021', '2022']
INTERVALS = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1mo"]
DAILY_INTERVALS = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d"]
TRADING_TYPE = ["spot", "um", "cm"]
MONTHS = list(range(1,13))
PERIOD_START_DATE = '2020-01-01'
BASE_URL = 'https://data.binance.vision/'
START_DATE = date(int(YEARS[0]), MONTHS[0], 1)
END_DATE = datetime.date(datetime.now())
UM_FUTURES_SYMBOLS_DIR = '/Users/lingxiao/Desktop/binance-data/binance_data/configs/um-futures-symbol.txt'
CM_FUTURES_SYMBOLS_DIR = '/Users/lingxiao/Desktop/binance-data/binance_data/configs/cm-futures-symbols.txt'
SPOTS_SYMBOLS_DIR = '/Users/lingxiao/Desktop/binance-data/binance_data/configs/spot-symbols.txt'
