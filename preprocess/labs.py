"""
Module for labs data preprocessing.

This module provides functionalities to preprocess labs data.
"""

import json
import traceback
import pandas as pd
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from helper import (load_config, read_data, write_data, nationality_to_country, nationality_to_continent_and_region, construct_path, setup_logging)

CONFIG = load_config("labs")

def preprocess() -> None:
    """
    Preprocess the labs data.

    Args:
    - data (DataFrame or other suitable type): The input data to be preprocessed.

    Returns:
    - DataFrame (or other suitable type): The preprocessed data.
    """

    file_name = CONFIG["name"]
    
    source_path, source_format, source_compression = CONFIG["source"]["path"], CONFIG["source"]["format"], CONFIG["source"]["compression"]
    destination_path, destination_format, destination_compression = CONFIG["destination"]["path"], CONFIG["destination"]["format"], CONFIG["destination"]["compression"]

    source_compression_method = source_compression["method"] if source_compression["enabled"] else None
    destination_compression_method = destination_compression["method"] if destination_compression["enabled"] else None

    file_path = construct_path(source_path, file_name, source_format, compression=source_compression_method)
    save_path = construct_path(destination_path, file_name, destination_format, compression=destination_compression_method)

    # READ UNIQUE IDs
    with open(f'{destination_path}unique_ids.json', 'r') as f:
        unique_ids_list = json.load(f)

    # READ FILE
    df = read_data(file_path, source_format)
    df = df[df["PERSONID"].isin(unique_ids_list)]

    # CLEAN DATA
    dtype_conversion = CONFIG["parameters"]["dtype_conversion"]
    df = df.astype(dtype_conversion)

    df.ORDERDATE = df.ORDERDATE.str.strip()
    df.ORDERDATE = pd.to_datetime(df.ORDERDATE, format=CONFIG['parameters']['date_format'])
    df.sort_values('ORDERDATE', ascending=False, inplace=True)

    df.replace({
        "POMPE": {
            "YES": 1,
            "NO": 0
        }
    }, inplace=True)

    df.drop_duplicates(subset=['PERSONID', 'ORDERCATALOG'], keep='first', inplace=True)
    pivot_labs_df = df.pivot(index='PERSONID', columns='ORDERCATALOG', values='RESULTVALUE')
    pivot_labs_df.reset_index(inplace=True)
    df = pivot_labs_df.merge(df[['PERSONID', 'POMPE']].drop_duplicates(), on='PERSONID')
    
    # SAVE FILE
    write_data(df, save_path, destination_format, index=False, compression=destination_compression_method)
    print(df.head())
    print(df.shape)

def run_cleaning():
    setup_logging(CONFIG["name"])
    preprocess()

if __name__ == "__main__":
    try:
        run_cleaning()
    except Exception as e:
        logging.error(f"An error occurred: {e}\n{traceback.format_exc()}")