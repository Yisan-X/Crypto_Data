from enum import Enum, EnumMeta
from typing import Any


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True 


class BaseEnum(Enum, metaclass=MetaEnum):
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class InstrumentType(BaseEnum):
    FUTURES = 'futures'
    OPTIONS = 'options'
    SPOT = 'spot'


class FuturesContractType(BaseEnum):
    COIN_MARGIN = 'cm'
    USD_MARGIN = 'um'


class DataSizeType(BaseEnum):
    DAILY = 'daily'
    MONTHLY = 'monthly'


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


class FuturesDataType(BaseEnum):
    AGG_TRADE = DataType.AGG_TRADE
    BOOK_DEPTH = DataType.BOOK_DEPTH
    BOOK_TICKER = DataType.BOOK_TICKER
    INDEX_PRICE_KLINE = DataType.INDEX_PRICE_KLINE
    KLINE = DataType.KLINE
    LIQUIDATION_SNAPSHOT = DataType.LIQUIDATION_SNAPSHOT
    MARK_PRICE_KLINE = DataType.MARK_PRICE_KLINE
    METRICS = DataType.METRICS
    PREMIUM_INDEX_KLINE = DataType.PREMIUM_INDEX_KLINE
    TRADE = DataType.TRADES


class SpotDataType(BaseEnum):
    AGG_TRADE = DataType.AGG_TRADE
    KLINE = DataType.KLINE
    TRADE = DataType.TRADES


class OptionDataType(BaseEnum):
    BVOL_INDEX = DataType.BVOL_INDEX
    EOH_SUMMARY = DataType.EOH_SUMMARY


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


class SpotDataFrequency(BaseEnum):
    HOUR12 = DataFrequency.HOUR12
    MIN15 = DataFrequency.MIN15
    DAY1 = DataFrequency.DAY1
    HOUR1 = DataFrequency.HOUR1
    HOUR2 = DataFrequency.HOUR2
    MIN30 = DataFrequency.MIN30
    MIN1 = DataFrequency.MIN1
    MIN3 = DataFrequency.MIN3
    HOUR4 = DataFrequency.HOUR4
    MIN5 = DataFrequency.MIN5
    HOUR6 = DataFrequency.HOUR6
    HOUR8 = DataFrequency.HOUR8
    SECOND1 = DataFrequency.SECOND1


class FuturesDataFrequency(BaseEnum):
    HOUR12 = DataFrequency.HOUR12
    MIN15 = DataFrequency.MIN15
    DAY1 = DataFrequency.DAY1
    HOUR1 = DataFrequency.HOUR1
    MONTH1 = DataFrequency.MONTH1
    MIN1 = DataFrequency.MIN1
    WEEK1 = DataFrequency.WEEK1
    HOUR2 = DataFrequency.HOUR2
    MIN30 = DataFrequency.MIN30
    DAY3 = DataFrequency.DAY3
    MIN3 = DataFrequency.MIN3
    HOUR4 = DataFrequency.HOUR4
    MIN5 = DataFrequency.MIN5
    HOUR6 = DataFrequency.HOUR6
    HOUR8 = DataFrequency.HOUR8

RETRY_TIMES = 5

COLUMNS = {
    DataType.AGG_TRADE: ['AggregateTradeId', 'Price', 'Quantity', 'FirstTradeId', 'LastTradeId', 'Timestamp', 'IsBuyerMaker', 'BestMatch'],
    DataType.KLINE: ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume', 'NumberOfTrades', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignore'],
    DataType.TRADES: ['TradeId', 'Price', 'Qty', 'QuoteQty', 'Time', 'IsBuyerMaker', 'BestMatch']
}

# um: USD-Margin; cm: Coin-Margin
FUTURES_COLUMNS = {
    DataType.AGG_TRADE: {
        FuturesContractType.USD_MARGIN: ['AggregateTradeId', 'Price', 'Quantity', 'FirstTradeId', 'LastTradeId', 'Timestamp', 'IsBuyerMaker'],
        FuturesContractType.COIN_MARGIN: ['AggregateTradeId', 'Price', 'Quantity', 'FirstTradeId', 'LastTradeId', 'Timestamp', 'IsBuyerMaker'],
    },
    DataType.KLINE: {
        FuturesContractType.USD_MARGIN: ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume', 'NumberOfTrades', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignore'],
        FuturesContractType.USD_MARGIN: ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime','BaseAssetVolume', 'NumberOfTrades', 'TakerBuyVolume', 'TakerBuyQuoteBaseAssetVolume','Ignore']
    },
    DataType.TRADES: {
        FuturesContractType.USD_MARGIN: ['TradeId', 'Price', 'Qty', 'QuoteQty', 'Time', 'IsBuyerMaker'],
        FuturesContractType.COIN_MARGIN: ['TradeId', 'Price', 'BaseQty', 'Time', 'IsBuyerMaker'],
    },
    DataType.BOOK_TICKER: {
        FuturesContractType.USD_MARGIN: ['UpdateId', 'BestBidPrice', 'BestBidQty', 'BestAskPrice', 'BestAskQty', 'TransactionTime', 'EventTime'],
        FuturesContractType.COIN_MARGIN: ['UpdateId', 'BestBidPrice', 'BestBidQty', 'BestAskPrice', 'BestAskQty', 'TransactionTime', 'EventTime']
    },
    DataType.METRICS: {
        FuturesContractType.USD_MARGIN: ['CreateTime', 'Symbol', 'SumOpenInterest', 'SumOpenInterestValue', 'CountTopTraderLongShortRatio', 'SumTopTraderLongShortRatio', 'CountLongShortRatio', 'SumTakerLongShotVolRatio'],
        FuturesContractType.COIN_MARGIN: ['CreateTime', 'Symbol', 'SumOpenInterest', 'SumOpenInterestValue', 'CountTopTraderLongShotRatio', 'SumTopTraderLongShotRatio', 'CountLongShortRatio', 'SumTakerLongShotVolRatio'],
    },
    DataType.INDEX_PRICE_KLINE: {
        FuturesContractType.USD_MARGIN: ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteVolume', 'Count', 'TakerBuyVolume', 'TakerBuyQuoteVolume', 'Ignore'],
        FuturesContractType.COIN_MARGIN: ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteVolume', 'Count', 'TakerBuyVolume', 'TakerBuyQuoteVolume', 'Ignore'],
    },
    DataType.MARK_PRICE_KLINE: {
        FuturesContractType.USD_MARGIN: ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteVolume', 'Count', 'TakerBuyVolume', 'TakerBuyQuoteVolume', 'Ignore'],
        FuturesContractType.COIN_MARGIN: ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteVolume', 'Count', 'TakerBuyVolume', 'TakerBuyQuoteVolume', 'Ignore'],
    },
    DataType.PREMIUM_INDEX_KLINE: {
        FuturesContractType.USD_MARGIN: ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteVolume', 'Count', 'TakerBuyVolume', 'TakerBuyQuoteVolume', 'Ignore'],
        FuturesContractType.COIN_MARGIN: ['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteVolume', 'Count', 'TakerBuyVolume', 'TakerBuyQuoteVolume', 'Ignore'],
    },
    DataType.LIQUIDATION_SNAPSHOT: {
        FuturesContractType.USD_MARGIN: ['Time', 'Symbol', 'Side', 'OrderType', 'TimeInForce', 'OriginalQuantity', 'Price', 'AveragePrice', 'OrderStatus', 'LastFillQuantity', 'AccumulatedFillQuantity'],
        FuturesContractType.COIN_MARGIN: ['Time', 'Symbol', 'Side', 'OrderType', 'TimeInForce', 'OriginalQuantity', 'Price', 'AveragePrice', 'OrderStatus', 'LastFillQuantity', 'AccumulatedFillQuantity'],
    }
}

OPTIONS_COLUMNS = {
    DataType.BVOL_INDEX: ['CalcTime', 'Symbol', 'BaseAsset', 'QuoteAsset', 'IndexValue']
}

