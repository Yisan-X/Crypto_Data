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

    @staticmethod
    def format_download_filename(instrumentId, date, data_type: DataType, freq: DataFrequency = None):
        if data_type in [DataType.KLINE, DataType.INDEX_PRICE_KLINE, DataType.PREMIUM_INDEX_KLINE, DataType.MARK_PRICE_KLINE]:
            return "_".join([instrumentId, freq, data_type, date]) + '.parquet'
        elif data_type == DataType.BOOK_TICKER:
            return "_".join([instrumentId, str(1), data_type, date]) + '.parquet'
        else:
            return "_".join([instrumentId, 'None', data_type, date]) + '.parquet'

    def fetch_binance_date_data(self, instrumentId, instrumentType: InstrumentType, date:str, 
                                data_type: DataType, freq: DataFrequency, margin_type: FuturesContractType = None):
        if instrumentType not in InstrumentType:
            raise ValueError(f"Unknown instrument type: {instrumentType}, supported types are {InstrumentType.list()}")
        if data_type not in DataType:
            raise ValueError(f"Unknown data type: {data_type}, supported data types are {DataType.list()}")
        if freq and freq not in DataFrequency:
            raise ValueError(f"Unknown data frequency: {freq}, supported frequencies are {DataFrequency.list()}")
        if margin_type and margin_type not in FuturesContractType:
            raise ValueError(f"Unknown futures margin type: {margin_type}, supported margin types are {FuturesContractType.list()}")
        dest_dir = os.path.join(self._save_dir, date)
        make_dir(dest_dir)
        fn = DataFetcher.format_download_filename(instrumentId, date, data_type, freq)
        dest_dir = os.path.join(dest_dir, fn)
        df = get_daily_data(InstrumentType, instrumentId, data_type, freq, date, dest_dir, margin_type, overwrite = True)
        logger.info(f"BinanceData::{dest_dir} is downloaded")
        return df