"""
Module for diagnosis data preprocessing.

This module provides functionalities to preprocess diagnosis data.
"""

import json
import traceback
import pandas as pd
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from helper import (load_config, read_data, write_data, nationality_to_country, nationality_to_continent_and_region, construct_path, setup_logging)

CONFIG = load_config("diagnosis")

def preprocess() -> None:
    """
    Preprocess the diagnosis data.

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
    df = df[df['PERSONID'].isin(unique_ids_list)]
    df = df[["PERSONID", "ENCNTRID", "ICDCODE", "ICDDESCRIPTION", "POMPE"]]

    # CLEAN DATA
    dtype_conversion = CONFIG["parameters"]["dtype_conversion"]
    df = df.astype(dtype_conversion)

    df = df.groupby(['PERSONID', 'ENCNTRID', 'ICDCODE']).last().reset_index()

    description_map = df.groupby('ICDCODE')['ICDDESCRIPTION'].first()
    df['ICDDESCRIPTION'] = df['ICDCODE'].map(description_map)
    code_to_description_dict = description_map.to_dict()

    with open(f'{destination_path}icdcodes.json', 'w') as file:
        json.dump(code_to_description_dict, file)

    # TRANSFORM DATA
    df['VALUE'] = 1
    pivot_df = pd.crosstab(df['PERSONID'], df['ICDCODE'])
    pivot_df.reset_index(inplace=True)
    df = df.drop_duplicates(subset='PERSONID')[['PERSONID', 'POMPE']]

    df.replace({
        "POMPE": {"YES": 1, "NO": 0, "UNKNOWN": None}
    }, inplace=True)

    df = pd.merge(pivot_df, df, on='PERSONID', how='left')

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