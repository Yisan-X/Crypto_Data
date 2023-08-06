import logging
import json
from typing import Dict, List
import urllib.request
import pandas as pd 
from argparse import ArgumentTypeError
import os
from loguru import logger

# def get_all_symbols(type:str):
#     # ctx = ssl.create_default_context()
#     # ctx.check_hostname = False
#     # ctx.verify_mode = ssl.CERT_NONE
#     # headers = {
#     #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
#     # }
#     if type == 'um':
#         # request = urllib.request.Request("https://fapi.binance.com/fapi/v1/exchangeInfo", headers=headers)
#         response = urllib.request.urlopen("https://fapi.binance.com/fapi/v1/exchangeInfo").read()
#     elif type == 'cm':
#         response = urllib.request.urlopen("https://dapi.binance.com/dapi/v1/exchangeInfo").read()
#     elif type == 'spot':
#         response = urllib.request.urlopen("https://api.binance.com/api/v3/exchangeInfo").read()
#     else:
#         raise ArgumentTypeError(f"The available types are 'um'(for USDT based), 'cm'(for USD based), and 'spot', got {type} instead")
#     return list(map(lambda symbol: symbol['symbol'], json.loads(response)['symbols']))


class SymbolConfig(object):
    UM_URL = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    CM_URL = "https://dapi.binance.com/dapi/v1/exchangeInfo"
    SPOT_URL = "https://api.binance.com/api/v3/exchangeInfo"
    OPTIONS_URL = "https://eapi.binance.com/eapi/v1/exchangeInfo"

    def __init__(self, type:str) -> None:
        self._type = type
        if type == 'um':
            self.response = urllib.request.urlopen(self.UM_URL).read()
        elif type == 'cm':
            self.response = urllib.request.urlopen(self.CM_URL).read()
        elif type == 'spots':
            self.response = urllib.request.urlopen(self.SPOT_URL).read()
        elif type == 'options':
            self.response = urllib.request.urlopen(self.OPTIONS_URL).read()
        else:
           raise ArgumentTypeError(f"The available types are 'um'(for USDT based), 'cm'(for USD based), and 'spot', got {type} instead") 
        self.config = None

    def get_all_symbols(self) -> List:
        if self._type == 'options':
            return list(map(lambda symbol: symbol['symbol'], json.loads(self.response)['optionSymbols']))
        return list(map(lambda symbol: symbol['symbol'], json.loads(self.response)['symbols'])) 
    
    def get_all_symbols_config(self) -> Dict:
        if self._type == 'options':
            config_lst = json.loads(self.response)['optionSymbols']
        else:
            config_lst = json.loads(self.response)['symbols']
        self.config = pd.DataFrame(config_lst)
    
    def load_config(self, path:str) -> None:
        self.config = pd.read_csv(path)

    def save_config(self, path:str) -> None:
        if self.config is None:
            raise TypeError('self.config is None, The config has not been loaded')
        if os.path.isfile(path):
            logger.warning(f'{path} exists, it will be overwritted')
        self.config.to_csv(path, index = False)


if __name__ == '__main__':
    save_dir = r'./config/binance'
    spot_config = SymbolConfig('spots')
    spot_config.get_all_symbols_config()
    spot_config.save_config(
        os.path.join(save_dir, 'spots.csv')
    )
    logger.info("binance spot symbols downloaded")
    um_config = SymbolConfig('um')
    um_config.get_all_symbols_config()
    um_config.save_config(
        os.path.join(save_dir, 'um.csv')
    )
    logger.info("binance USD-M futures symbols downloaded")
    cm_config = SymbolConfig('cm')
    cm_config.get_all_symbols_config()
    cm_config.save_config(
        os.path.join(save_dir, 'cm.csv')
    )
    logger.info("binance COIN-M futures symbols downloaded")
    options_config = SymbolConfig('options')
    options_config.get_all_symbols_config()
    options_config.save_config(
        os.path.join(save_dir, 'options.csv')
    )
    logger.info("binance options symbols downloaded")