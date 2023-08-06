from ..exchange import Exchange

import os
from pathlib import Path
import pandas as pd 

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('start_date', type = str)
parser.add_argument('end_date', type = str)


def gen_um_mapping():
    pass