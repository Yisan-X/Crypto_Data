from distutils.command.config import config
import json
import os, sys
from typing import Dict
import pandas as pd 

from .symbol_config import SymbolConfig
# from ...utils import nested_set


def nested_set(dct, keys, value):
    for k in keys[:-1]:
        dct = dct.setdefault(k, {})
    dct[keys[-1]] = value

class BinanceUpdateConfig(object):
    Future_leverage_Options = [1,3,5,10,20]
    fee_config = {
        'maker_fee':{
            'spot': 0.001,
            'um': 0.0002,
            'cm': 0.0001,
        },
        'taker_fee':{
            'spot': 0.001,
            'um': 0.0004,
            'cm': 0.0005,
        }
    }

    def __init__(self) -> None:
        pass

    def load_config_file(self, contract_type) -> pd.DataFrame:
        config_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'{contract_type}.csv')
        if not os.path.isfile(config_dir):
            config = SymbolConfig(contract_type)
            config.get_all_symbols_config()
            config.save_config(config_dir)
        config_df = pd.read_csv(config_dir)
        return config_df

    def update_spots_config(self, usdtOnly:bool = True) -> Dict:
        """
        We only trade the spots whose quote asset is USDT currently
        """
        config_df = self.load_config_file('spots')
        if usdtOnly == True:
            config_df = config_df.loc[config_df['quoteAsset'] == 'USDT']
        dct = {'Binance':dict()}
        nested_set(dct, ['Binance', 'Fees', 'maker_fee'], self.fee_config['maker_fee']['spot'])
        nested_set(dct, ['Binance', 'Fees', 'taker_fee'], self.fee_config['taker_fee']['spot'])
        status = config_df[['symbol', 'status']].set_index('symbol').to_dict()['status']
        nested_set(dct, ['Binance', 'trading_status'], status)
        return dct
    
    def update_coinMargin_config(self) -> Dict:
        config_df = self.load_config_file('cm')
        config_df = config_df.loc[config_df['contractType'] == 'PERPETUAL']
        dct = {'BinanceCoinMargin':dict()}
        nested_set(dct, ['BinanceCoinMargin', 'Fees', 'maker_fee'], self.fee_config['maker_fee']['cm'])
        nested_set(dct, ['BinanceCoinMargin', 'Fees', 'taker_fee'], self.fee_config['taker_fee']['cm'])
        future_multiplier = config_df[['pair', 'contractSize']].set_index('pair').to_dict()['contractSize']
        nested_set(dct, ['BinanceCoinMargin', 'Future_contract_usd_face'], future_multiplier) # reversed futures
        future_size_precision = config_df[['pair', 'quantityPrecision']].set_index('pair').to_dict()['quantityPrecision']
        nested_set(dct, ['BinanceCoinMargin', 'Future_size_precision'], future_size_precision)
        future_leverage_options = dict(
            zip(
                list(config_df['pair']), [self.Future_leverage_Options] * len(config_df)
            )
        )
        nested_set(dct, ['BinanceCoinMargin', 'Future_leverage_options'], future_leverage_options)
        nested_set(dct, ['BinanceCoinMargin', 'Future_contract_types'], ['perp', 'quarter', 'next_quarter'])
        nested_set(dct, ['BinanceCoinMargin', 'abnormal_expiration_date'], dict())
        return dct

    def update_usdMargin_config(self) -> Dict:
        config_df = self.load_config_file('um')
        config_df = config_df.loc[config_df['contractType'] == 'PERPETUAL']
        dct = {'BinanceUsdMargin': dict()}
        nested_set(dct, ['BinanceUsdMargin', 'Fees', 'maker_fee'], self.fee_config['maker_fee']['um'])
        nested_set(dct, ['BinanceUsdMargin', 'Fees', 'taker_fee'], self.fee_config['taker_fee']['um'])
        future_multiplier = dict(
            zip(config_df['pair'], [1.0] * len(config_df))
        )
        nested_set(dct, ['BinanceUsdMargin', 'Future_multiple'], future_multiplier)
        future_size_precision = config_df[['pair', 'quantityPrecision']].set_index('pair').to_dict()['quantityPrecision']
        nested_set(dct, ['BinanceUsdMargin', 'Future_size_precision'], future_size_precision)
        future_leverage_options = dict(
            zip(
                list(config_df['pair']), [self.Future_leverage_Options] * len(config_df)
            )
        )
        nested_set(dct, ['BinanceUsdMargin', 'Future_leverage_options'], future_leverage_options)
        nested_set(dct, ['BinanceUsdMargin', 'Future_contract_types'], ['perp'])
        return dct
    
    def update_all(self, config_dict:Dict = None) -> Dict:
        if config_dict is None:
            config_dict = {
                "Exchanges" : dict()
            }
        spot_dct = self.update_spots_config()
        nested_set(config_dict, ['Exchanges', 'Binance'], spot_dct['Binance'])
        um_dct = self.update_usdMargin_config()
        nested_set(config_dict, ['Exchanges', 'BinanceUsdMargin'], um_dct['BinanceUsdMargin'])
        cm_dct = self.update_coinMargin_config()
        nested_set(config_dict, ['Exchanges', 'BinanceCoinMargin'], cm_dct['BinanceCoinMargin'])
        return config_dict
