"""
Module for clinical data preprocessing.

This module provides functionalities to preprocess clinical data.
"""

import json
import traceback
import numpy as np
import pandas as pd
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from helper import (load_config, read_data, write_data, nationality_to_country, nationality_to_continent_and_region, construct_path, setup_logging)

CONFIG = load_config("clinical")

def preprocess() -> None:
    """
    Preprocess the clinical data.

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
    df.replace({
        "POMPE": {
            "YES": 1,
            "NO": 0
        }
    }, inplace=True)

    dtype_conversion = CONFIG["parameters"]["dtype_conversion"]
    df = df.astype(dtype_conversion)

    df.drop(columns=["ORDERID", "CLINICALEVENTID", "TASKASSAY"], axis=1, inplace=True)
    df = df[~df.EVENTDATETIME.str.contains("4557")]
    df.EVENTDATETIME = df.EVENTDATETIME.str.strip()
    df.EVENTDATETIME = pd.to_datetime(df.EVENTDATETIME, format=CONFIG["parameters"]["date_format"])
    df.sort_values(by=["EVENTDATETIME"], ascending=False, inplace=True)
    df.replace(["nan", "None", None], np.nan, inplace=True)
    df = df[df.EVENTRESULT.notnull()]
    df.EVENTRESULT = df.EVENTRESULT.str.strip()
    df = df[pd.to_numeric(df.EVENTRESULT, errors='coerce').notnull()]
    df.EVENTNAME = df.EVENTNAME.str.rstrip('.')
    clinical_df_grp = df.groupby(["PERSONID", "EVENTNAME"]).first().reset_index()

    pivot_clinical_df = clinical_df_grp.pivot(index='PERSONID', columns='EVENTNAME', values='EVENTRESULT')
    pivot_clinical_df.reset_index(inplace=True)
    df = pivot_clinical_df.merge(df[['PERSONID', 'POMPE']].drop_duplicates(), on='PERSONID')
    
    # SAVE FILE
    write_data(df, save_path, destination_format, index=False, compression=destination_compression_method)
    print(df.head())
    print(df.shape)

def main():
    setup_logging(CONFIG["name"])
    preprocess()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}\n{traceback.format_exc()}")