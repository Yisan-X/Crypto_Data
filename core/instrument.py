from .utils import nested_get
from .static import INSTRUMENT_DELIMITER, SYMBOL_DELIMITER, apiconfig, main_contract_change_duration
from .exceptions import ConfigNotFoundError, InstrumentNotFoundError
from .exchange import Exchange

import logging
import re 
import datetime
from pytz import timezone
from typing import Tuple
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)


class ContractType:
    Spot = 'spot'
    FutureThisWeek = 'week'
    FutureNextWeek = 'nextweek'
    FutureThisQuarter = 'quarter'
    FutureNextQuarter = 'nextquarter'
    FuturePerp = 'perp'
    FutureIndex = 'index'
    Option = 'option'
    Forex = 'forex'


class InstrumentTypeClass:
    Spot = 'spot'
    ForwardFuture = 'forward_future'
    ReverseFuture = 'reverse_future'
    Quanto = 'quanto'
    CFD = 'cfd'


class Instrument:
    """
    Add an instrument:
    Instrument('Binance_BTC.USD_PERP')
    Instrument('Binance_BTC.USD_quarter')
    Instrument.get_contract_expiration_date('2022-11-16') (perform this step before loading the data)
    """
    FORWARD_FUTURES_EXCHANGES = [Exchange.HuobiPerpUSDT, Exchange.HuobiPerpUSDTCross, Exchange.Bitasset, \
                                Exchange.BinanceUsdMargin, Exchange.NewOkcoinUSDT, Exchange.Ftx]

    def __init__(self, instrumentId:str, trading:bool = True) -> None:
        """
        Expected Instrument id:
        spots: Binance_BTC.USD_spot
        perp: Binance_BTC.USDT_perp
        quarterly: Binance_BTC.USD_quarter 
        """
        self._instrumentId = instrumentId
        self._trading = trading
        self._exchange = None
        self._symbol = None
        self._contract_type = None
        self._expiration_date = None
        self._expiration_dt = None
        self._change_contract_dt = None
        self._base_ccy = None
        self._quote_ccy = None
        self._instrument_type_class = None
        self._future_size_precision = None
        self._settlement_ccy = None
        self._future_contract_usd = None
        self._future_multiplier = None
        self._process()
    
    @property
    def info(self):
        info_dict = {
            'instrumentId': self._instrumentId,
            'status': self._trading,
            'contract_type': self._contract_type,
            'expiration_date': self._expiration_date,
            'change_contract_date': self._change_contract_dt,
            'instrument_type_class': self._instrument_type_class,
            'future_size_precision': self._future_size_precision,
            'settlement_currency': self._settlement_ccy,
            'future_contract_usd': self._future_contract_usd,
            'future_multiplier': self._future_multiplier,
        }
        return info_dict

    def __str__(self) -> str:
        return self._instrumentId
    
    def __repr__(self) -> str:
        return str(self)

    def _process(self) -> None:
        self._instrumentId, flag = Instrument.format_instrument_id(self._instrumentId)
        if flag == False:
            raise InstrumentNotFoundError(f'Instrument::instrument {self._instrumentId} cannot be standardize, please check.')
        self._exchange, self._symbol, self._contract_type = self._instrumentId.split(INSTRUMENT_DELIMITER)
        self._base_ccy, self._quote_ccy = self._symbol.split(SYMBOL_DELIMITER)

        if self._exchange.lower() == "bitmex":
            self._exchange = 'BitMEX'
        
        self._instrument_type_class = Instrument.get_instrument_type_class(self._exchange, self._symbol, self._contract_type)
        tmp_symbol = self._symbol.replace(SYMBOL_DELIMITER, '')
        if self._instrument_type_class != InstrumentTypeClass.Spot:
            self._future_size_precision = nested_get(
                apiconfig, ['Exchanges', self._exchange, 'Future_size_precision', tmp_symbol], 0
            )
            if self._instrument_type_class == InstrumentTypeClass.ReverseFuture:
                self._settlement_ccy = self._base_ccy
                self._future_contract_usd = nested_get(
                    apiconfig, ['Exchanges', self._exchange, 'Future_contract_usd_face', tmp_symbol]
                )
                if self._future_contract_usd is None:
                    raise ConfigNotFoundError(f'Instrument::Missing Future_contract_usd_face for instrumentId = {self._instrumentId}')
            elif self._instrument_type_class == InstrumentTypeClass.ForwardFuture or self._instrument_type_class == InstrumentTypeClass.Quanto:
                self._settlement_ccy = self._quote_ccy if self._instrument_type_class == InstrumentTypeClass.ForwardFuture else 'BTC'
                self._future_multiplier = nested_get(
                    apiconfig, ['Exchanges', self._exchange, 'Future_multiple', tmp_symbol]                    
                )
                if self._future_multiplier is None:
                    raise ConfigNotFoundError(f'Instrument::Missing Future_Multiple for instrumentId = {self._instrumentId}, with symbol {tmp_symbol}')

    def get_contract_expiration_date(self, date:str) -> None:
        expiration_date, expiration_dt = Exchange.get_contract_expiration_date(date, self._exchange)
        next_expiration_date, next_expiration_dt = Exchange.get_contract_next_expiration_date(date, self._exchange)
        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
        if self._contract_type == ContractType.FutureThisQuarter:
            if dt <= ( expiration_dt - main_contract_change_duration ):
                self._expiration_date = expiration_date
                self._expiration_dt = expiration_dt.astimezone(timezone('Asia/Shanghai'))
                self._change_contract_dt = expiration_dt - main_contract_change_duration
            else:
                self._expiration_date = next_expiration_date
                self._expiration_dt = next_expiration_dt.astimezone(timezone('Asia/Shanghai'))
                self._change_contract_dt = expiration_dt - main_contract_change_duration
        elif self._contract_type == ContractType.FutureNextQuarter:
            if dt <= ( expiration_dt - main_contract_change_duration ):
                self._expiration_date = next_expiration_date
                self._expiration_dt = next_expiration_dt.astimezone(timezone('Asia/Shanghai'))
                self._change_contract_dt = expiration_dt - main_contract_change_duration
            else:
                self._expiration_date = expiration_date
                self._expiration_dt = expiration_dt.astimezone(timezone('Asia/Shanghai'))
                self._change_contract_dt = expiration_dt - main_contract_change_duration

    @property
    def instrument_contract(self):
        return INSTRUMENT_DELIMITER.join([self._exchange, self._symbol, self._contract_type])

    @property
    def is_trading_instrument(self):
        return self._trading
        
    @staticmethod
    def format_quarter_contract(contract:str) -> Tuple[str]:
        if re.findall(contract) != []:
            expiration_date = re.findall(r'[0-9]+', contract)[0]
            contract = re.sub(r'[0-9]', '', contract)
            return contract, expiration_date
        else:
            return contract, None

    @staticmethod
    def get_instrument_type_class(exchange, symbol:str, contract_type:str) -> str:
        if contract_type == ContractType.Spot:
            return InstrumentTypeClass.Spot
        elif contract_type == ContractType.FutureLTFX or exchange in Instrument.FORWARD_FUTURES_EXCHANGES:
            return InstrumentTypeClass.ForwardFuture
        elif exchange == Exchange.BitMEX and symbol.endswith('BTC'):
            return InstrumentTypeClass.ForwardFuture
        elif exchange == Exchange.BitMEX and 'BTC' not in symbol:
            return InstrumentTypeClass.Quanto
        elif exchange in [Exchange.Ig, Exchange.Yahoo]:
            return InstrumentTypeClass.CFD
        else:
            return InstrumentTypeClass.ReverseFuture
        
    @staticmethod
    def format_instrument_id(instrumentId:str) -> str:
        exchange, symbol, contract_type = instrumentId.split(INSTRUMENT_DELIMITER)
        find_exchange = False
        for key, value in Exchange.__dict__.items():
            if not key.startswith('__') and value.lower() == exchange.lower():
                exchange = value
                find_exchange  = True
                break
        symbol = symbol.upper()
        find_contract_type = False
        # formatted_contract, expiration_date = Instrument.format_quarter_contract(contract_type)
        for key, value in ContractType.__dict__.items():
            if not key.startswith('__') and value.lower() == contract_type.lower():
                # formatted_contract = value
                contract_type = value
                find_contract_type = True
                break
        if find_exchange == True and find_contract_type == True:
            return INSTRUMENT_DELIMITER.join([exchange, symbol, contract_type]), True
        else:
            logger.warning(f'DataType::standardize instrument_id failed, instrument_id = {instrumentId}, find_contract = {find_contract_type}, find_exchange = {find_exchange}')
            return instrumentId, False
        
    @staticmethod
    def convert_futuresize_into_coin(instrument, price:float, future_size:float) -> float:
        if instrument._instrument_type_class == InstrumentTypeClass.Spot:
            return future_size
        elif instrument._instrument_type_class == InstrumentTypeClass.ReverseFuture:
            return future_size * instrument._future_contract_usd / price
        elif instrument._instrument_type_class == InstrumentTypeClass.ForwardFuture:
            return future_size * instrument._future_multiplier
        elif instrument._instrument_type_class == InstrumentTypeClass.Quanto:
            return future_size * instrument._future_multiplier * price
    
    @staticmethod
    def convert_coin_into_futuresize(instrument, price:float, coin_size:float) -> float:
        if instrument._instrument_type_class == InstrumentTypeClass.Spot:
            return coin_size
        elif instrument._instrument_type_class == InstrumentTypeClass.ReverseFuture:
            return round(coin_size * price / instrument._future_contract_usd, instrument._future_size_precision)
        elif instrument._instrument_type_class == InstrumentTypeClass.ForwardFuture:
            return round(coin_size / instrument._future_multiplier, instrument._future_size_precision)
        elif instrument._instrument_type_class == InstrumentTypeClass.Quanto:
            return round(coin_size / (instrument._future_multiplier * price), instrument._future_size_precision)

