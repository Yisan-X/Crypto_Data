import re 
import json
import os
from dateutil.relativedelta import relativedelta

INSTRUMENT_DELIMITER = '_'
SYMBOL_DELIMITER = '.'
FLOAT_ERROR = 1E-8

def instrument_name_split(instrument_id):
    tmp_lst = instrument_id.split('.')
    exchange = tmp_lst[-1].upper()
    expire_date = re.findall(r'\d+', tmp_lst[1])
    name = ''.join(re.findall('[a-zA-Z]', tmp_lst[1]))
    return exchange, name, expire_date


apiconfig = json.load(
    open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'config', 'apiconfig.json'
            )
        )
)


main_contract_change_duration = relativedelta(days=0)