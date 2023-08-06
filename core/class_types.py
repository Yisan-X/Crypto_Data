from enum import Enum, EnumMeta
from typing import Any

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True 


class BaseEnum(str, Enum, metaclass=MetaEnum):
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class DataFrequency(BaseEnum):
    HOUR12 = '12h'
    MIN15 = '15m'
    DAY1 = '1d'
    MONTH1 = '1mo'
    WEEK1 = '1w'
    HOUR1 = '1h'
    HOUR2 = '2h'
    MIN30 = '30m'
    DAY3 = '3d'
    MIN1 = '1m'
    MIN3 = '3m'
    HOUR4 = '4h'
    MIN5 = '5m'
    HOUR6 = '6h'
    HOUR8 = '8h'
    SECOND1 = '1s'


class DataType(BaseEnum):
    AGG_TRADE = 'aggTrades'
    BOOK_DEPTH = 'bookDepth'
    BOOK_TICKER = 'bookTicker'
    INDEX_PRICE_KLINE = 'indexPriceKlines'
    KLINE = 'klines'
    LIQUIDATION_SNAPSHOT = 'LiquidationSnapshot'
    MARK_PRICE_KLINE = 'markPriceKlines'
    METRICS = 'metrics'
    PREMIUM_INDEX_KLINE = 'premiumIndexKlines'
    TRADES = 'trades'
    BVOL_INDEX = 'BVOLIndex'
    EOH_SUMMARY = 'EOHSummary'


class InstrumentType(BaseEnum):
    FUTURES = 'futures'
    OPTIONS = 'options'
    SPOT = 'spot'


class FuturesContractType(BaseEnum):
    COIN_MARGIN = 'cm'
    USD_MARGIN = 'um'