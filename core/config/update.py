import os
import json

from datetime import datetime

from binance import BinanceUpdateConfig

if __name__ == '__main__':
    curr_date = datetime.now().date().strftime('%Y-%m-%d')
    config_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'apiconfig_{curr_date}.json')
    binance_update = BinanceUpdateConfig()
    config_dict = binance_update.update_all()
    
    with open(config_dir, 'w') as fp:
        json.dump(config_dict, fp, indent=4)