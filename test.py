from Binance import DataFetcher
from Binance.class_types import *

from loguru import logger

save_dir = "/Volumes/LIngxiao's Disk/BinanceData"


fetcher = DataFetcher(save_dir)

def future_test():
    quote_coin = "BTC"
    base_coin = "USDT"
    date = "2023-07-31"
    instrumentType = InstrumentType.FUTURES
    dataType = DataType.KLINE
    freqType = FuturesDataFrequency.MIN1
    marginType = FuturesContractType.USD_MARGIN
    df = fetcher.fetch_binance_date_data(
        quote_coin=quote_coin,
        base_coin=base_coin,
        instrumentType=instrumentType,
        date=date,
        data_type=dataType,
        freq=freqType,
        margin_type=marginType
    )
    logger.info(df.head().T)

    dataType = DataType.BOOK_TICKER
    df = fetcher.fetch_binance_date_data(
        quote_coin=quote_coin,
        base_coin=base_coin,
        instrumentType=instrumentType,
        date=date,
        data_type=dataType,
        freq=freqType,
        margin_type=marginType
    )
    logger.info(df.head().T)    

def spot_test():
    quote_coin = "BTC"
    base_coin = "USDT"
    date = "2023-07-31"
    instrumentType = InstrumentType.SPOT
    dataType = DataType.KLINE
    freqType = FuturesDataFrequency.MIN1
    df = fetcher.fetch_binance_date_data(
        quote_coin=quote_coin,
        base_coin=base_coin,
        instrumentType=instrumentType,
        date=date,
        data_type=dataType,
        freq=freqType,
    )
    logger.info(df.head().T)

def option_test():
    quote_coin = "BTC"
    base_coin = "USDT"
    date = "2023-07-31"
    instrumentType = InstrumentType.OPTIONS
    dataType = DataType.BVOL_INDEX
    freqType = FuturesDataFrequency.MIN1
    df = fetcher.fetch_binance_date_data(
        quote_coin=quote_coin,
        base_coin=base_coin,
        instrumentType=instrumentType,
        date=date,
        data_type=dataType,
        freq=freqType,
    )
    logger.info(df.head().T)


if __name__ == '__main__':
    # future_test()
    # spot_test()
    option_test()