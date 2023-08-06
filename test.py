from core import DataFetcher
from core import InstrumentType, DataFrequency, DataType
from core import binance

from loguru import logger

save_dir = "./BinanceData"


fetcher = DataFetcher(save_dir)

def future_test():
    date = "2023-07-31"
    instrumentID = 'BinanceUsdMargin_BTC.USDT_perp'
    dataType = DataType.KLINE
    freqType = DataFrequency.MIN1
    df = fetcher.fetch_date(
        instrumentID, date, dataType, freqType
    )
    logger.info(df.head().T)

    dataType = DataType.BOOK_TICKER
    df = fetcher.fetch_date(
        instrumentID, date, dataType, freqType
    )
    logger.info(df.head().T)    

    date = "2023-07-31"
    instrumentID = 'BinanceCoinMargin_BTC.USD_perp'
    dataType = DataType.KLINE
    freqType = DataFrequency.MIN1
    df = fetcher.fetch_date(
        instrumentID, date, dataType, freqType
    )
    logger.info(df.head().T)

    dataType = DataType.BOOK_TICKER
    df = fetcher.fetch_date(
        instrumentID, date, dataType, freqType
    )
    logger.info(df.head().T)    

    date = "2023-07-31"
    instrumentID = 'BinanceCoinMargin_BTC.USD_quarter'
    dataType = DataType.KLINE
    freqType = DataFrequency.MIN1
    df = fetcher.fetch_date(
        instrumentID, date, dataType, freqType
    )
    logger.info(df.head().T)

    dataType = DataType.BOOK_TICKER
    df = fetcher.fetch_date(
        instrumentID, date, dataType, freqType
    )
    logger.info(df.head().T)  

    date = "2023-07-31"
    instrumentID = 'BinanceCoinMargin_BTC.USD_nextquarter'
    dataType = DataType.KLINE
    freqType = DataFrequency.MIN1
    df = fetcher.fetch_date(
        instrumentID, date, dataType, freqType
    )
    logger.info(df.head().T)

    dataType = DataType.BOOK_TICKER
    df = fetcher.fetch_date(
        instrumentID, date, dataType, freqType
    )
    logger.info(df.head().T)  

def spot_test():
    date = "2023-07-31"
    instrumentID = 'Binance_BTC.USDT_spot'
    dataType = DataType.KLINE
    freqType = DataFrequency.MIN1
    df = fetcher.fetch_date(
        instrumentID, date, dataType, freqType
    )
    logger.info(df.head().T)

def option_test():
    date = "2023-07-31"
    instrumentID = 'BinanceOptions_BTC.USDT_option'
    dataType = DataType.BVOL_INDEX
    freqType = DataFrequency.MIN1
    df = fetcher.fetch_date(
        instrumentID, date, dataType, freqType
    )
    logger.info(df.head().T)


if __name__ == '__main__':
    future_test()
    spot_test()
    option_test()