import logging
import json
from typing import Dict, List
import urllib.request
import pandas as pd 
from argparse import ArgumentTypeError
import os

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

logger = logging.getLogger(__name__)

class SymbolConfig(object):
    UM_URL = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    CM_URL = "https://dapi.binance.com/dapi/v1/exchangeInfo"
    SPOT_URL = "https://api.binance.com/api/v3/exchangeInfo"

    def __init__(self, type:str) -> None:
        self._type = type
        if type == 'um':
            self.response = urllib.request.urlopen(self.UM_URL).read()
        elif type == 'cm':
            self.response = urllib.request.urlopen(self.CM_URL).read()
        elif type == 'spots':
            self.response = urllib.request.urlopen(self.SPOT_URL).read()
        else:
           raise ArgumentTypeError(f"The available types are 'um'(for USDT based), 'cm'(for USD based), and 'spot', got {type} instead") 
        self.config = None

    def get_all_symbols(self) -> List:
        return list(map(lambda symbol: symbol['symbol'], json.loads(self.response)['symbols'])) 
    
    def get_all_symbols_config(self) -> Dict:
        config_lst = json.loads(self.response)['symbols']
        self.config = pd.DataFrame(config_lst)
    
    def load_config(self, path:str) -> None:
        self.config = pd.read_csv(path)

    def save_config(self, path:str) -> None:
        if self.config is None:
            raise TypeError('self.config is None, The config has not been loaded')
        if os.path.isfile(path):
            logger.warn(f'{path} exists, it will be overwritted')
        self.config.to_csv(path, index = False)


if __name__ == '__main__':
    save_dir = r'/Users/lingxiao/Desktop/crypto_backtest/backtest/backtest/config/binance'
    spot_config = SymbolConfig('spots')
    spot_config.get_all_symbols_config()
    spot_config.save_config(
        os.path.join(save_dir, 'spots.csv')
    )
    um_config = SymbolConfig('um')
    um_config.get_all_symbols_config()
    um_config.save_config(
        os.path.join(save_dir, 'um.csv')
    )
    cm_config = SymbolConfig('cm')
    cm_config.get_all_symbols_config()
    cm_config.save_config(
        os.path.join(save_dir, 'cm.csv')
    )