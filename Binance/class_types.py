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
    AGG_TRADE = DataType.AGG_TRADE.value
    BOOK_DEPTH = DataType.BOOK_DEPTH.value
    BOOK_TICKER = DataType.BOOK_TICKER.value
    INDEX_PRICE_KLINE = DataType.INDEX_PRICE_KLINE.value
    KLINE = DataType.KLINE.value
    LIQUIDATION_SNAPSHOT = DataType.LIQUIDATION_SNAPSHOT.value
    MARK_PRICE_KLINE = DataType.MARK_PRICE_KLINE.value
    METRICS = DataType.METRICS.value
    PREMIUM_INDEX_KLINE = DataType.PREMIUM_INDEX_KLINE.value
    TRADE = DataType.TRADES.value


class SpotDataType(BaseEnum):
    AGG_TRADE = DataType.AGG_TRADE.value
    KLINE = DataType.KLINE.value
    TRADE = DataType.TRADES.value


class OptionDataType(BaseEnum):
    BVOL_INDEX = DataType.BVOL_INDEX.value
    EOH_SUMMARY = DataType.EOH_SUMMARY.value


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
    HOUR12 = DataFrequency.HOUR12.value
    MIN15 = DataFrequency.MIN15.value
    DAY1 = DataFrequency.DAY1.value
    HOUR1 = DataFrequency.HOUR1.value
    HOUR2 = DataFrequency.HOUR2.value
    MIN30 = DataFrequency.MIN30.value
    MIN1 = DataFrequency.MIN1.value
    MIN3 = DataFrequency.MIN3.value
    HOUR4 = DataFrequency.HOUR4.value
    MIN5 = DataFrequency.MIN5.value
    HOUR6 = DataFrequency.HOUR6.value
    HOUR8 = DataFrequency.HOUR8.value
    SECOND1 = DataFrequency.SECOND1.value


class FuturesDataFrequency(BaseEnum):
    HOUR12 = DataFrequency.HOUR12.value
    MIN15 = DataFrequency.MIN15.value
    DAY1 = DataFrequency.DAY1.value
    HOUR1 = DataFrequency.HOUR1.value
    MONTH1 = DataFrequency.MONTH1.value
    MIN1 = DataFrequency.MIN1.value
    WEEK1 = DataFrequency.WEEK1.value
    HOUR2 = DataFrequency.HOUR2.value
    MIN30 = DataFrequency.MIN30.value
    DAY3 = DataFrequency.DAY3.value
    MIN3 = DataFrequency.MIN3.value
    HOUR4 = DataFrequency.HOUR4.value
    MIN5 = DataFrequency.MIN5.value
    HOUR6 = DataFrequency.HOUR6.value
    HOUR8 = DataFrequency.HOUR8.value

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

