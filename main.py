import logging
import colorlog
import pandas as pd
import datetime
from typing import Tuple, Any

from utils.utils import *
from utils.stats_class import StatisticsManager

def process_data(data: pd.DataFrame, stats: StatisticsManager) -> Tuple[pd.DataFrame, Any]:
    """
    Process raw data into a cleaned and transformed format for model input.

    Args:
        data (pd.DataFrame): The raw input data to be processed.
        stats (StatisticsManager): An instance of StatisticsManager to manage and store statistics.

    Returns:
        Tuple[pd.DataFrame, Any]: A tuple containing the processed DataFrame and any additional processed information.

    Steps:
        1. Log the initial shape of the data.
        2. Remove rows with NaN values.
        3. Transform timestamp fields to a standard format.
        4. Save the processed DataFrame into a database and update statistics.
    """
    process_data = (data
                    .pipe(print_shape, msg='Shape original')  # Log original shape of the data.
                    .pipe(drop_row_with_nan)  # Remove rows containing any NaN values.
                    .pipe(print_shape, msg='Shape after remove row with any NaN value')  # Log shape after NaN removal.
                    .pipe(transform_timestamp)  # Standardize timestamp fields.
                    .pipe(print_shape, msg='Shape after transform timestamp')  # Log shape after timestamp transformation.
                    )
    
    # Save the processed data and update statistics in the database.
    save_df_in_db(process_data, stats)
    
    return process_data

if __name__ == '__main__':
    # Configure logging to provide detailed execution information.
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)
    # Detect and load CSV files from the './data' directory.
    file_list = detect_load_csv_file('./data')
    
    validation_path_file = ''  # Path to the validation file (if any).
    global_stats = None  # Placeholder for global statistics.
    
    stats = StatisticsManager()  # Initialize the statistics manager.
    # Iterate through each file in the detected file list.
    for file_path in file_list:
        if 'validation' in file_path:
            # Identify the validation file.
            validation_path_file = file_path
        else:
            logging.info(f'Working with: {file_path}')  # Log the file being processed.
            
            # Load and process the data from the current file.
            df = load_file_data(path=file_path)
            df = process_data(data=df, stats=stats)
            
            print('-'*60)  # Visual separator for console output.
            
            # Log statistics for the 'price' column in the current file.
            logging.info(f"Statistics for column 'price' in {file_path}:\nmin: {df['price'].min()} - max: {df['price'].max()} - avg: {df['price'].mean()} - rows: {len(df)}")
            
            print('-'*60)  # Visual separator for console output.
            
            # Log global statistics for the 'price' column across files.
            logging.info(f"Global statistics for column 'price':\n{stats.get_statistics()}")
        
        print('#'*60)  # Visual separator for console output.
    # Log and print statistics retrieved from the database.
    logging.info('Stats From DB:')
    stats_db = stats_from_db()
    print(stats_db)

    print('#'*60)  # Visual separator for console output.
    logging.info('Validation File')
    # Process the validation file if available.
    df = load_file_data(path='./data/validation.csv')
    df = process_data(data=df, stats=stats)
    # Log statistics for the 'price' column in the validation file.
    logging.info(f"Statistics for column 'price' in {file_path}:\nmin: {df['price'].min()} - max: {df['price'].max()} - avg: {df['price'].mean()} - rows: {len(df)}")
    # Log and print updated statistics retrieved from the database.
    logging.info('Stats From DB:')
    stats_db = stats_from_db()
    print(stats_db)