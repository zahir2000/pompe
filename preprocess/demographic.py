"""
Module for demographic data preprocessing.

This module provides functionalities to preprocess demographic data.
"""

import json
import traceback
import pandas as pd
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from helper import (load_config, read_data, write_data, nationality_to_country, nationality_to_continent_and_region, construct_path, setup_logging)

CONFIG = load_config("demographic")

def preprocess() -> None:
    """
    Preprocess the demographic data.

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

    # READ FILE
    df = read_data(file_path, source_format)
    df['DOB'] = pd.to_datetime(df['DOB'].str.strip(), format='%d/%b/%Y')
    df['DOE'] = pd.to_datetime(df['DOE'].str.strip(), format='%d/%b/%Y')

    # CLEAN DATA
    total_duplicates = df.duplicated(subset=['PERSONID', 'GENDER', 'NATIONALITY']).sum()
    if total_duplicates > 0:
        logging.info(f"There were {df.duplicated(subset=['PERSONID', 'GENDER', 'NATIONALITY']).sum()} duplicated rows.")
        df.drop_duplicates(subset=['PERSONID', 'GENDER', 'NATIONALITY'], inplace=True)
        logging.info(f"Dropped {total_duplicates} duplicated rows.")

    age_date, age_date_format = CONFIG["parameters"]["age_date"]["date"], CONFIG["parameters"]["age_date"]["format"]
    age_date = datetime.strptime(age_date, age_date_format)
    df["AGE"] = df['DOB'].apply(lambda x: relativedelta(age_date, x).years if pd.notnull(x) else None)
    df.loc[df['AGE'] < 0, 'AGE'] = None

    df['DEATH'] = df['DOE'].notnull().astype('int8')

    df.replace({
        "POMPE": {"YES": 1, "NO": 0, "UNKNOWN": None},
        "GENDER": {"Male": 1, "Female": 2, "Unknown": None}
    }, inplace=True)
    
    dtype_conversion = CONFIG["parameters"]["dtype_conversion"]
    for col, dtype in dtype_conversion.items():
        df[col] = df[col].astype(dtype)

    df["COUNTRY"] = df["NATIONALITY"].map(lambda x: nationality_to_country.get(x, None))
    df['CONTINENT'] = df['NATIONALITY'].map(lambda x: nationality_to_continent_and_region.get(x, {}).get('continent'))
    df['REGION'] = df['NATIONALITY'].map(lambda x: nationality_to_continent_and_region.get(x, {}).get('region'))

    # SAVE FILE
    write_data(df, save_path, destination_format, index=False, compression=destination_compression_method)
    print(df.head())

    # SAVE UNIQUE PATIENT IDs
    unique_patient_ids = df['PERSONID'].unique().tolist()
    with open(f'{destination_path}unique_ids.json', 'w') as f:
        json.dump(unique_patient_ids, f)

def run_cleaning():
    setup_logging(CONFIG["name"])
    preprocess()

if __name__ == "__main__":
    try:
        run_cleaning()
    except Exception as e:
        logging.error(f"An error occurred: {e}\n{traceback.format_exc()}")