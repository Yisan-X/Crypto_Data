import os, sys, re, shutil
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile
from pathlib import Path
from datetime import *
from typing import Callable, List
import contextlib
import urllib.request
import urllib.error
from loguru import logger
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

from .static import *
from .utils import *
from .class_types import *

def download_file(
    symbol: str,
    file_name:str,
    dest_dir:str,
    user_instrumentId:str,
    overwrite:bool = False,
    retry_times:int = RETRY_TIMES,
    error_callbacks:Callable = None,
    column_names:List = None,
    progress_bar:bool = False,
) -> pd.DataFrame:
    download_path = get_download_url(file_name)

    if os.path.exists(dest_dir):
        logger.warning(f'{dest_dir} already exists! overwrite = {overwrite}')
        if overwrite == False:
            return

    num_try = 0
    while num_try < retry_times:
        try:
            with contextlib.closing(urllib.request.urlopen(download_path)) as dl_file:
                dl_file = urllib.request.urlopen(download_path)
                length = dl_file.getheader('content-length')
                if length:
                    length = int(length)
                    blocksize = max(4096, length // 100)
                raw_data = None
                dl_process = 0
                while True:
                    buf = dl_file.read(blocksize)
                    dl_process += len(buf)
                    if not buf:
                        if raw_data is None:
                            raise ValueError(f'File fetched from {download_path} is empty')
                        break
                    if raw_data is None:
                        raw_data = buf
                    else:
                        raw_data = raw_data + buf
                    done = int(50*dl_process / length)
                    if progress_bar:
                        sys.stdout.write('\r[%s%s]' % ('#' * done, '.'*(50-done)))
                        sys.stdout.flush()
                zipped = ZipFile(BytesIO(raw_data))
                fn = os.path.split(file_name)[-1]
                fn = os.path.splitext(fn)[0] + '.csv'
                data = TextIOWrapper(zipped.open(fn), encoding='utf-8')
                if column_names is None:
                    try:
                        data = pd.read_csv(data, encoding='ISO-8859-1')
                    except:
                        data = pd.read_csv(data, header=None)
                else:
                    data = pd.read_csv(data, header = None, names=column_names)
                    if isinstance(data.iloc[0][0], str):
                        data = data.drop(0)
                data['qualified_instrument_id'] = symbol
                data['user_instrument_id'] = user_instrumentId
                if 'UpdateId' in data.columns:
                    data['UpdateId'] = data['UpdateId'].astype(int)
                if 'BestBidPrice' in data.columns:
                    data['BestBidPrice'] = data['BestBidPrice'].astype(float)
                if 'BestAskPrice' in data.columns:
                    data['BestAskPrice'] = data['BestAskPrice'].astype(float)
                if 'BestAskQty' in data.columns:
                    data['BestAskQty'] = data['BestAskQty'].astype(float)
                if 'BestBidQty' in data.columns:
                    data['BestBidQty'] = data['BestBidQty'].astype(float)
                if 'TransactionTime' in data.columns:
                    data['TransactionTime'] = data['TransactionTime'].astype(int)
                if 'EventTime' in data.columns:
                    data['EventTime'] = data['EventTime'].astype(int)
                data.to_parquet(dest_dir)
                return data
        except urllib.error.HTTPError:
            logger.warning(f'Failed to reach url {download_path}, retry time = {num_try}/{retry_times}')

        num_try += 1

    if num_try == retry_times and error_callbacks is not None:
        error_callbacks(file_name, dest_dir)

    return None


def get_monthly_data(
    instrument_type:str,
    symbol:str,
    data_type:str,
    freq:str,
    year:int,
    month:int,
    dest_dir:str,
    user_instrumentId: str,
    margin_type:str = None,
    checksum:bool = False,
    *args,
    **kwargs,
) -> None:
    current_date = convert_str_to_date('{}-{}-01'.format(year, month))
    if instrument_type == InstrumentType.FUTURES and margin_type == None:
        raise ArgumentTypeError('For futures data, the margin_type argument must be set')
    if freq not in INTERVALS:
        raise ArgumentTypeError(f'freq {freq} not supported, available freqs are {INTERVALS}')
    if current_date >= START_DATE and current_date <= END_DATE:
        if instrument_type == InstrumentType.SPOT or instrument_type == InstrumentType.OPTIONS:
            file_url = format_monthly_file(
                symbol, data_type, freq, year, month,
            )
            column_names = COLUMNS[data_type]
        elif instrument_type == 'futures':
            file_url = format_futures_monthly_file(
                symbol, margin_type, data_type, freq, year, month,
            )
            # column_names = FUTURES_COLUMNS[data_type]
            column_names = None
        data = download_file(symbol, file_url, dest_dir, user_instrumentId, column_names=column_names, *args, **kwargs)

        if checksum == True:
            checksum_path = file_url + '.CHECKSUM'
            save_folder, save_fn = os.path.split(dest_dir)
            save_fn = os.path.splitext(save_fn)[0] + '.zip.CHECKSUM'
            checksum_dest_dir = os.path.join(save_folder, save_fn)
            _ = download_file(symbol, checksum_path, checksum_dest_dir, user_instrumentId, *args, **kwargs)
        
        return data


def get_daily_data(
    instrument_type:str,
    symbol:str,
    data_type:str,
    freq:str,
    date_time:str,
    dest_dir:str,
    user_instrumentId: str, 
    margin_type:str = None,
    checksum:bool = False,
    *args,
    **kwargs,
) -> None:
    current_date = convert_str_to_date(date_time)
    year, month, date = date_time.split('-')
    year, month, date = int(year), int(month), int(date)
    if instrument_type == InstrumentType.FUTURES and margin_type == None:
        raise ArgumentTypeError('For futures data, the margin_type argument must be set')
    if freq not in DAILY_INTERVALS:
        raise ArgumentTypeError(f'freq {freq} not supported, available freqs are {DAILY_INTERVALS}')
    if current_date >= START_DATE and current_date <= END_DATE:
        if instrument_type == InstrumentType.SPOT:
            file_url = format_daily_file(
                symbol, data_type, freq, year, month, date,
            )
            column_names = COLUMNS[data_type]
        elif instrument_type == InstrumentType.FUTURES:
            file_url = format_futures_daily_file(
                symbol, margin_type, data_type, freq, year, month, date
            )
            column_names = FUTURES_COLUMNS[data_type][margin_type]
        elif instrument_type == InstrumentType.OPTIONS:
            file_url = format_options_daily_file(symbol, data_type, freq, year, month, date)
            column_names = OPTIONS_COLUMNS[data_type]
        else:
            raise ValueError(f'{instrument_type} not supported')
        logger.info(f'{file_url} in progress')
        data = download_file(symbol, file_url, dest_dir, user_instrumentId, column_names=column_names, *args, **kwargs)
        logger.info(f'{file_url} downloaded')

        if checksum == True:
            checksum_path = file_url + '.CHECKSUM'
            save_folder, save_fn = os.path.split(dest_dir)
            save_fn = os.path.splitext(save_fn)[0] + '.zip.CHECKSUM'
            checksum_dest_dir = os.path.join(save_folder, save_fn)
            _ = download_file(symbol, checksum_path, checksum_dest_dir, user_instrumentId, *args, **kwargs)

        return data