from . import Binance as binance
from .exchange import Exchange
from .class_types import *

from loguru import logger
import pandas as pd

class DataFetcher:
    EXCHANGES = {
        Exchange.Binance: binance,
        Exchange.BinanceCoinMargin: binance,
        Exchange.BinanceUsdMargin: binance,
        Exchange.BinanceOptions: binance
    }

    def __init__(self, save_dir) -> None:
        self._save_dir = save_dir

    def fetch_date(self, instrumentId: str, date: str, data_type: DataType, freq: DataFrequency) -> pd.DataFrame:
        """
        instrumentId: {Exchange.exchange}_{BaseCoin}.{QuoteCoin}_{contract_type}
        i.e. Binance_BTC.USDT_spot, BinanceUsdMargin_BTC.USDT_perp, BinanceCoinMargin_BTC.USD_quarter
        """
        exchange, symbol, contract_type = instrumentId.split('_')
        if exchange not in self.EXCHANGES:
            raise Exception(f"exchange {exchange} not supported")
        fetcher = self.EXCHANGES[exchange].DataFetcher(self._save_dir)
        data = fetcher.fetch_date_data(
            instrumentId, date, data_type, freq
        )
        return data