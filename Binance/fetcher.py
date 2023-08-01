from .class_types import *
from .download_file import * 
from .static import *
from .utils import * 

from loguru import logger
import pandas as pd 


class DataFetcher(object):
    EXCHANGES = ["Binance", "BinanceUsdMargin", "BinanceCoinMargin"]

    def __init__(self, save_dir) -> None:
        self._save_dir = save_dir
        make_dir(save_dir)
        logger.info(f"save dir: {save_dir} is created")

    @staticmethod
    def format_instrumentId(quote_coin, base_coin, instrumentType: InstrumentType, margin_type = None):
        s = ""
        if instrumentType == InstrumentType.FUTURES:
            if margin_type == FuturesContractType.USD_MARGIN:
                s += "BinanceUsdMargin"
            elif margin_type == FuturesContractType.COIN_MARGIN:
                s += "BinanceCoinMargin"
            else:
                raise ValueError(f"{margin_type} not recognized")
        elif instrumentType == InstrumentType.SPOT:
            s += "Binance"
        elif instrumentType == InstrumentType.OPTIONS:
            s += "BinanceOption"
        s += f"_{quote_coin.upper()}.{base_coin.upper()}"
        return s
        

    @staticmethod
    def format_download_filename(instrumentId, date, data_type: DataType, instrumentType: InstrumentType, freq: DataFrequency = None):
        if data_type in [DataType.KLINE, DataType.INDEX_PRICE_KLINE, DataType.PREMIUM_INDEX_KLINE, DataType.MARK_PRICE_KLINE]:
            return "_".join([instrumentId, freq, data_type, date]) + '.parquet'
        elif data_type == DataType.BOOK_TICKER:
            return "_".join([instrumentId, str(1), data_type, date]) + '.parquet'
        else:
            return "_".join([instrumentId, 'None', data_type, date]) + '.parquet'

    def fetch_binance_date_data(self, quote_coin, base_coin, instrumentType: InstrumentType, date:str, 
                                data_type: DataType, freq: DataFrequency, margin_type: FuturesContractType = None):
        if instrumentType not in InstrumentType:
            raise ValueError(f"Unknown instrument type: {instrumentType}, supported types are {InstrumentType.list()}")
        if data_type not in DataType:
            raise ValueError(f"Unknown data type: {data_type}, supported data types are {DataType.list()}")
        if freq and freq not in DataFrequency:
            raise ValueError(f"Unknown data frequency: {freq}, supported frequencies are {DataFrequency.list()}")
        if margin_type and margin_type not in FuturesContractType:
            raise ValueError(f"Unknown futures margin type: {margin_type}, supported margin types are {FuturesContractType.list()}")
        instrumentId = DataFetcher.format_instrumentId(quote_coin, base_coin, instrumentType, margin_type)
        if instrumentType == InstrumentType.OPTIONS:
            symbol = f"{quote_coin}BVOL{base_coin}"
        else:
            symbol = f"{quote_coin}{base_coin}"
        dest_dir = os.path.join(self._save_dir, date)
        make_dir(dest_dir)
        fn = DataFetcher.format_download_filename(instrumentId, date, data_type, instrumentType, freq)
        dest_dir = os.path.join(dest_dir, fn)
        df = get_daily_data(instrumentType, symbol, data_type, freq, date, dest_dir, instrumentId, margin_type, overwrite = True)
        logger.info(f"BinanceData::{dest_dir} is downloaded")
        return df