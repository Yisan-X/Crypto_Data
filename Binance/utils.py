from argparse import ArgumentTypeError
import os, sys, re, shutil
import json
from pathlib import Path
from datetime import *
from typing import List
import pandas as pd
from .static import *
from .class_types import *


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
        raise ArgumentTypeError(f"Expected date format 'year-month-date', i.e. 2022-01-05, get {arg_value} instead")
    return arg_value


def get_download_url(file_url) -> str:
    return "{}{}".format(BASE_URL, file_url)


def format_monthly_file(symbol:str, data_type:str, freq:str, year:int, month:int) -> str:
    if month < 10:
        month = f'0{month}'
    if data_type not in SpotDataType:
        raise ValueError(f'{data_type} not in the supported data types: {SpotDataType.list()}')
    if data_type == DataType.KLINE:
        return 'data/spot/monthly/{}/{}/{}/{}-{}-{}-{}.zip'.format(data_type, symbol.upper(), freq, symbol.upper(), freq, year, month)
    else:
        return 'data/spot/monthly/{}/{}/{}-{}-{}-{}.zip'.format(data_type, symbol.upper(), symbol.upper(), data_type, year, month)


def format_daily_file(symbol:str, data_type:str, freq:str, year:int, month:int, date:int) -> str:
    if month < 10:
        month = f'0{month}'
    if date < 10:
        date = f'0{date}'
    if data_type not in SpotDataType:
        raise ValueError(f'{data_type} not in the supported data types: {SpotDataType.list()}')
    if data_type == SpotDataType.KLINE:
        if freq not in SpotDataFrequency:
            raise ValueError(f"{freq} not in the supported data frequencies: {SpotDataFrequency.list()}")
        return 'data/spot/daily/{}/{}/{}/{}-{}-{}-{}-{}.zip'.format(data_type, symbol.upper(), freq, symbol.upper(), freq, year, month, date)
    else:
        return 'data/spot/daily/{}/{}/{}-{}-{}-{}-{}.zip'.format(data_type, symbol.upper(), symbol.upper(), data_type, year, month, date)


def format_futures_monthly_file(contract:str, margin_type:str, data_type:str, freq:str, year:int, month:int) -> str:
    if month < 10:
        month = f'0{month}'
    if data_type not in FuturesDataType:
        raise ValueError(f'{data_type} not in the supported data types: {FuturesDataType.list()}')
    if data_type in [FuturesDataType.KLINE, FuturesDataType.INDEX_PRICE_KLINE, 
                     FuturesDataType.MARK_PRICE_KLINE, FuturesDataType.PREMIUM_INDEX_KLINE]:
        if freq not in FuturesDataFrequency:
            raise ValueError(f"{freq} not in the supported data frequencies: {FuturesDataFrequency.list()}")
        return 'data/futures/{}/monthly/{}/{}/{}/{}-{}-{}-{}.zip'.format(margin_type, data_type, contract.upper(), freq, contract.upper(), freq, year, month)
    else:
        return 'data/futures/{}/monthly/{}/{}/{}-{}-{}-{}.zip'.format(margin_type, data_type, contract.upper(), contract.upper(), data_type, year, month)


def format_futures_daily_file(contract:str, margin_type:str, data_type:str, freq:str, year:int, month:int, date:int) -> str:
    if month < 10:
        month = f'0{month}'
    if date < 10:
        date = f'0{date}'
    if data_type not in FuturesDataType:
        raise ValueError(f'{data_type} not in the supported data types: {FuturesDataType.list()}')
    if data_type in [FuturesDataType.KLINE, FuturesDataType.INDEX_PRICE_KLINE, 
                     FuturesDataType.MARK_PRICE_KLINE, FuturesDataType.PREMIUM_INDEX_KLINE]:
        if freq not in FuturesDataFrequency:
            raise ValueError(f"{freq} not in the supported data frequencies: {FuturesDataFrequency.list()}")
        return 'data/futures/{}/daily/{}/{}/{}/{}-{}-{}-{}-{}.zip'.format(margin_type, data_type, contract.upper(), freq, contract.upper(), freq, year, month, date)
    else:
        return 'data/futures/{}/daily/{}/{}/{}-{}-{}-{}-{}.zip'.format(margin_type, data_type, contract.upper(), contract.upper(), data_type, year, month, date)


def format_options_daily_file(symbol:str, data_type:str, freq:str, year:int, month:int, date:int) -> str:
    if month < 10:
        month = f'0{month}'
    if date < 10:
        date = f'0{date}'
    if data_type not in OptionDataType:
        raise ValueError(f'{data_type} not in the supported data types: {OptionDataType.list()}')
    return 'data/option/daily/{}/{}/{}-{}-{}-{}-{}.zip'.format(data_type, symbol.upper(), symbol.upper(), data_type, year, month, date)

def match_date_regex(arg_value:str, pattern = re.compile(r'\d{4}-\d{2}-\d{2}')) -> str:
    if not pattern.match(arg_value):
        raise ArgumentTypeError(f'datetime {arg_value} not match the pattern')
    return arg_value


def read_txt_to_list(txt_dir:str) -> List:
    with open(txt_dir) as file:
        lines = [line.rstrip() for line in file]
    return lines
