"""
Module for drugs data preprocessing.

This module provides functionalities to preprocess drugs data.
"""

import json
import traceback
import pandas as pd
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from helper import (load_config, read_data, write_data, nationality_to_country, nationality_to_continent_and_region, construct_path, setup_logging)

CONFIG = load_config("drugs")

def preprocess() -> None:
    """
    Preprocess the drugs data.

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
    df.ORDERDATE = df.ORDERDATE.str.strip()
    df.ORDERDATE = pd.to_datetime(df.ORDERDATE, format=CONFIG['parameters']['date_format'])

    # CLEAN DATA
    df.ORDERMNEMONIC = df.ORDERMNEMONIC.str.strip()
    df.replace({
        "POMPE": {
            "YES": 1,
            "NO": 0
        }
    }, inplace=True)

    df.sort_values('ORDERDATE', ascending=False, inplace=True)
    drugs_grp_by = df.groupby(['PERSONID', 'ENCNTRID', 'ORDERMNEMONIC']).last().reset_index()

    drugs_grp_by['VALUE'] = 1
    pivot_drugs_df = pd.crosstab(drugs_grp_by['PERSONID'], drugs_grp_by['ORDERMNEMONIC'])
    pivot_drugs_df.reset_index(inplace=True)

    pompe_mapping = df.drop_duplicates(subset='PERSONID')[['PERSONID', 'POMPE']]
    df = pivot_drugs_df.merge(pompe_mapping, on='PERSONID', how='left')
    
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