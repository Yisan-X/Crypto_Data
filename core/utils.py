from copy import deepcopy
from pathlib import Path
import re
import os
from datetime import date
import json

from .static import INSTRUMENT_DELIMITER, SYMBOL_DELIMITER

def nested_set(dct, keys, value):
    for k in keys[:-1]:
        dct = dct.setdefault(k, {})
    dct[keys[-1]] = value
    
def nested_get(dct, keys, value = None):
    obj = deepcopy(dct)
    for k in keys:
        obj = obj.get(k)
        if obj is None:
            return value
    return obj


def instrumentId_encode(exchange, base_coin, quote_coin, contract):
    return f"{exchange}_{base_coin.upper()}.{quote_coin.upper()}_{contract}"

def instrumentId_decode(instrumentId: str):
    exchange, symbol, contract = instrumentId.split(INSTRUMENT_DELIMITER)
    base_coin, quote_coin = symbol.split(SYMBOL_DELIMITER)
    return exchange, base_coin, quote_coin, contract
    
def make_dir(target_dir: str):
    if not os.path.isdir(target_dir):
        path = Path(target_dir)
        path.mkdir(parents=True, exist_ok=True)

def convert_str_to_date(date_time:str):
    y,m,d = date_time.split('-')
    date_obj = date(int(y), int(m), int(d))
    return date_obj


def match_date_regrex(arg_value, pattern = re.compile(r'\d{4}-\d{2}-\d{2}')):
    if not pattern.match(arg_value):
        raise Exception(f"Expected date format 'year-month-date', i.e. 2022-01-05, get {arg_value} instead")
    return arg_value


def update_delivery_config(instrumentId, contract, contractType, date, save_dir):
    json_dir = os.path.join(save_dir, 'mapping.json')
    mode = 'r+'
    if os.path.isfile(json_dir) == False:
        save_path = Path(save_dir)
        save_path.mkdir(parents=True, exist_ok=True)
        mode = 'w'
    with open(json_dir, mode) as jFile:
        if mode != 'w':
            data = json.load(jFile)
        else:
            data = {}
        nested_set(data, [date, instrumentId, contractType], contract)
        jFile.seek(0)
        json.dump(data, jFile, indent=4)
        jFile.truncate()