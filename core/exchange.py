from .static import apiconfig
from .utils import nested_get

import datetime
from dateutil.relativedelta import FR, relativedelta
from typing import Tuple

class Exchange:
    Ok = "OKcoin"
    Bitfinex = "Bitfinex"
    Huobi = "Huobi"
    HuobiMargin = "HuobiMargin"
    Binance = "Binance"
    BinanceCoinMargin = "BinanceCoinMargin"
    BinanceUsdMargin = "BinanceUsdMargin"
    BinanceOptions = "BinanceOptions"
    Bitasset = "Bitasset"
    BitMEX = "BitMEX"
    Bitstamp = "Bitstamp"
    Bitflyer = "Bitflyer"
    Bithumb = "Bithumb"
    Deribit = "Deribit"
    NewOkcoin = "NewOKcoin"
    NewOkcoinUSDT = "NewOKcoinUSDT"
    Luno = "Luno"
    Kraken = "Kraken"
    HuobiFuture = "HuobiFuture"
    Bybit = "Bybit"
    Ig = "Ig"
    Coinbase = "Coinbase"
    Ftx= "Ftx"
    HuobiFuturePerp = "HuobiFuturePerp"
    HuobiPerpUSDT = "HuobiPerpUSDT"
    HuobiPerpUSDTCross = "HuobiPerpUSDTCross"
    Yahoo = "Yahoo"

    @staticmethod
    def get_binance_expiration_date(date:str) -> Tuple[str, datetime.date]:
        year, month, date = date.split('-')
        year, month, date = int(year), int(month), int(date)
        dt = datetime.datetime(year, month, date)
        expire_date_1 = datetime.datetime(year-1, 12, 31) + relativedelta(months=3, weekday=FR(-1))
        expire_date_2 = datetime.datetime(year, 3, 31) + relativedelta(months=3, weekday=FR(-1))
        expire_date_3 = datetime.datetime(year, 6, 30) + relativedelta(months=3, weekday=FR(-1))
        expire_date_4 = datetime.datetime(year, 10, 1) + relativedelta(months=3, weekday=FR(-1))
        expire_date_5 = datetime.datetime(year, 12, 31) + relativedelta(months=3, weekday=FR(-1))
        
        if dt <= expire_date_1:
            expire_date = expire_date_1
        elif dt <= expire_date_2: 
            expire_date = expire_date_2 
        elif dt <= expire_date_3: 
            expire_date = expire_date_3 
        elif dt <= expire_date_4: 
            expire_date = expire_date_4
        else: 
            expire_date = expire_date_5

        expire_date_str = expire_date.date().strftime('%Y%m%d')[2:]
        abnormal_date = nested_get(
            apiconfig,
            ['Exchanges', 'BinanceCoinMargin', 'abnormal_expiration_date', expire_date_str]
        )
        if abnormal_date is not None:
            expire_date_str = abnormal_date
        return expire_date_str, expire_date


    @staticmethod
    def get_contract_expiration_date(date:str, exchange:str) -> Tuple[str, datetime.date]:
        if exchange == Exchange.BinanceCoinMargin or exchange == Exchange.BinanceUsdMargin:
            return Exchange.get_binance_expiration_date(date)
        else:
            raise Exception(f'Exchange::{exchange} not supported, the valid options are [{Exchange.BinanceCoinMargin}, {Exchange.BinanceUsdMargin}]')

    @staticmethod
    def get_binance_next_expiration_date(date:str) -> Tuple[str, datetime.date]:
        year, month, date = date.split('-')
        year, month, date = int(year), int(month), int(date)

        dt = datetime.datetime(year, month, date)
        expire_date_0 = datetime.datetime(year-1, 12, 31) + relativedelta(months=3, weekday=FR(-1))
        expire_date_1 = datetime.datetime(year, 3, 31) + relativedelta(months=3, weekday=FR(-1))
        expire_date_2 = datetime.datetime(year, 6, 30) + relativedelta(months=3, weekday=FR(-1))
        expire_date_3 = datetime.datetime(year, 10, 1) + relativedelta(months=3, weekday=FR(-1))
        expire_date_4 = datetime.datetime(year, 12, 31) + relativedelta(months=3, weekday=FR(-1))
        expire_date_5 = datetime.datetime(year+1, 3, 31) + relativedelta(months=3, weekday=FR(-1)) 

        if dt <= expire_date_0:
            expire_date = expire_date_1 
        elif dt <= expire_date_1: 
            expire_date = expire_date_2 
        elif dt <= expire_date_2:
            expire_date = expire_date_3 
        elif dt <= expire_date_3: 
            expire_date = expire_date_4
        else:
            expire_date = expire_date_5

        expire_date_str = expire_date.date().strftime('%Y%m%d')[2:]
        abnormal_date = nested_get(
            apiconfig,
            ['Exchanges', 'BinanceCoinMargin', 'abnormal_expiration_date', expire_date_str]
        )
        if abnormal_date is not None:
            expire_date_str = abnormal_date
        return expire_date_str, expire_date

    @staticmethod
    def get_contract_next_expiration_date(date:str, exchange:str) -> Tuple[str, datetime.date]:
        if exchange == Exchange.BinanceCoinMargin or exchange == Exchange.BinanceUsdMargin:
            return Exchange.get_binance_next_expiration_date(date)
        else:
            raise Exception(f'Exchange::{exchange} not supported, the valid options are [{Exchange.BinanceCoinMargin}, {Exchange.BinanceUsdMargin}]')
