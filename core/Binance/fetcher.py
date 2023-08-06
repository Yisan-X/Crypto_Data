from .class_types import *
from .download_file import * 
from .static import *
from .utils import * 

from ..exchange import Exchange
from ..instrument import ContractType
from ..static import INSTRUMENT_DELIMITER, SYMBOL_DELIMITER
from ..utils import update_delivery_config

from loguru import logger
import pandas as pd 


class DataFetcher(object):
    EXCHANGES = [Exchange.Binance, Exchange.BinanceUsdMargin, 
                 Exchange.BinanceCoinMargin, Exchange.BinanceOptions]

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
    def format_download_filename(instrumentId, date, data_type: DataType, freq: DataFrequency = None):
        if data_type in [DataType.KLINE, DataType.INDEX_PRICE_KLINE, DataType.PREMIUM_INDEX_KLINE, DataType.MARK_PRICE_KLINE]:
            return "_".join([instrumentId, freq, data_type, date]) + '.parquet'
        elif data_type == DataType.BOOK_TICKER:
            return "_".join([instrumentId, str(1), data_type, date]) + '.parquet'
        else:
            return "_".join([instrumentId, 'None', data_type, date]) + '.parquet'

    def _fetch_binance_date_data(self, quote_coin, base_coin, instrumentType: InstrumentType, date:str, 
                                data_type: DataType, freq: DataFrequency, user_instrumentId: str, 
                                margin_type: FuturesContractType = None, expire_date: str = None):
        if instrumentType not in InstrumentType:
            raise ValueError(f"Unknown instrument type: {instrumentType}, supported types are {InstrumentType.list()}")
        if data_type not in DataType:
            raise ValueError(f"Unknown data type: {data_type}, supported data types are {DataType.list()}")
        if freq and freq not in DataFrequency:
            raise ValueError(f"Unknown data frequency: {freq}, supported frequencies are {DataFrequency.list()}")
        if margin_type and margin_type not in FuturesContractType:
            raise ValueError(f"Unknown futures margin type: {margin_type}, supported margin types are {FuturesContractType.list()}")
        instrumentId = user_instrumentId
        if instrumentType == InstrumentType.OPTIONS:
            symbol = f"{quote_coin}BVOL{base_coin}"
        else:
            symbol = f"{quote_coin}{base_coin}"
            if expire_date:
                symbol += f'_{expire_date}'
            elif margin_type == FuturesContractType.COIN_MARGIN:
                symbol += f'_PERP'
        dest_dir = os.path.join(self._save_dir, date)
        make_dir(dest_dir)
        fn = DataFetcher.format_download_filename(instrumentId, date, data_type, freq)
        dest_dir = os.path.join(dest_dir, fn)
        df = get_daily_data(instrumentType, symbol, data_type, freq, date, dest_dir, instrumentId, margin_type, overwrite = True)
        if df is None:
            logger.warning(f"BinanceData::{dest_dir} download failed")
        else:
            logger.info(f"BinanceData::{dest_dir} is downloaded")
        return df
    
    def fetch_date_data(self, instrumentId: str, date: str, data_type: DataType,
                                freq: DataFrequency):
        exchange, quote_coin, base_coin, contractType = instrumentId_decode(instrumentId)
        if contractType == ContractType.FutureThisQuarter:
            expire_date,_ = Exchange.get_binance_expiration_date(date)
        elif contractType == ContractType.FutureNextQuarter:
            expire_date,_ = Exchange.get_binance_next_expiration_date(date)
        else:
            expire_date = None

        margin_type = None
        if exchange == Exchange.Binance:
            instrumentType = InstrumentType.SPOT
        elif exchange == Exchange.BinanceUsdMargin:
            instrumentType = InstrumentType.FUTURES
            margin_type = FuturesContractType.USD_MARGIN
        elif exchange == Exchange.BinanceCoinMargin:
            instrumentType = InstrumentType.FUTURES
            margin_type = FuturesContractType.COIN_MARGIN
        elif exchange == Exchange.BinanceOptions:
            instrumentType = InstrumentType.OPTIONS

        
        data = self._fetch_binance_date_data(
            quote_coin=quote_coin, base_coin=base_coin,
            instrumentType=instrumentType, date=date,
            data_type=data_type, freq=freq, user_instrumentId=instrumentId,
            margin_type=margin_type, expire_date=expire_date
        )

        if data is not None and contractType in [ContractType.FutureThisQuarter, ContractType.FutureNextQuarter]:
            update_delivery_config(
                f"{exchange}_{quote_coin}.{base_coin}", f"{quote_coin}{base_coin}_{expire_date}", 
                contractType, date, self._save_dir
            )
            logger.info(f"The config of the delivery contract {instrumentId} on date {date} has been saved/updated")

        return data

