"""
    + utils/utils.py
    + Description:
        This module provides functions for working with CSV files in a monitoring system.
        The functions include detecting CSV files in a folder, loading data from a CSV file,
        and printing the shape of a DataFrame.

        Functions:
            - detect_load_csv_file: Detects CSV files in a specified folder.
            - load_file_data: Loads the content of a CSV file into a DataFrame.
            - print_shape: Prints the shape of a DataFrame and returns it.
            - print_info: Prints a custom message for information logging purposes.
            - drop_row_with_nan: Deletes rows containing any NaN values from the DataFrame.
            - transform_timestamp: Converts the timestamp column to datetime and adds year, 
                semester, trimester, and month columns to the DataFrame.
            - save_df_in_db: Saves data from a pandas DataFrame to the database, handling foreign keys and statistics updates.
            - stats_from_db: Retrieves and returns statistical data from the `FactSales` table, including minimum, maximum, average prices, and the total number of records.
    Dependencies:
        - os: To interact with the file system.
        - pandas: For working with DataFrames.
        - logging: For logging informational and error messages.
        - numpy: For numerical operations (though not directly used in this module).
        - sqlalchemy: For database queries (though not directly used in this module).
        - config.database.Db: For managing the database (though not directly used in this module).
        - config.tables: For accessing related tables (though not directly used in this module).
        - utils.stats_class.StatisticsManager: For statistics (though not directly used in this module).
"""

import datetime
import logging
import numpy as np
import os
import pandas as pd
from sqlalchemy import func, select

from config.database import Db
from config.tables import FactSales, DimUser, DimTime
from utils.stats_class import StatisticsManager

def detect_load_csv_file(path: str):
    """
    Detects CSV files in a specified folder.

    This function checks for the existence of files with the `.csv` extension in a folder and returns a list
    of the found files. If no CSV files are found, a debug message is logged.

    :param path: The folder path to monitor. It should be a valid path in the file system.
    :return: A list of CSV files found in the folder. If no files are found, it returns None.
    """
    try:
        # List files in the folder that end with .csv
        files = [f'{path}/{f}' for f in os.listdir(path) if f.endswith('.csv')]
        
        if not files:
            logging.debug("No CSV files found in the folder.")
            return None
        
        return files
    except Exception as e:
        logging.error(f"Error accessing the folder: {e}")
        return None

def load_file_data(path: str):
    """
    Loads the content of a CSV file into a pandas DataFrame.

    This function reads a CSV file located at the specified path and loads it into a DataFrame for further
    processing and analysis.

    :param path: The path to the CSV file. It should be a valid path in the file system.
    :return: A pandas DataFrame containing the data loaded from the CSV file.
    :raises: Raises an exception if the file cannot be read due to errors in the file or path.
    """
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        logging.error(f"Error loading file: {e}")
        raise

def print_shape(data: pd.DataFrame, msg: str = 'Shape =') -> pd.DataFrame:
    """
    Prints and returns the shape of a DataFrame.

    This method logs the number of rows and columns of the DataFrame, helping to verify
    the size of the loaded or processed data.

    :param data: The DataFrame whose shape is to be printed.
    :param msg: An optional message to accompany the printed shape. Default is 'Shape ='.
    :return: The same DataFrame passed as a parameter.
    """
    logging.info(f'{msg} - {data.shape}')
    return data

def print_info(data: pd.DataFrame, msg: str) -> pd.DataFrame:
    """
    Prints a custom message for information logging purposes.

    This function logs the specified message without modifying the DataFrame. It can be used to
    print any relevant information, such as data processing steps, to help with debugging or
    tracking the flow of the data pipeline.

    :param data: The DataFrame to be passed, but is not modified by the function.
    :param msg: The message to be logged.
    :return: The same DataFrame passed as a parameter, allowing method chaining.
    """
    logging.info(f'{msg}')
    return data

def drop_row_with_nan(data: pd.DataFrame) -> pd.DataFrame:
    """
    Deletes rows containing any NaN values from the DataFrame.

    This function removes any rows in the DataFrame that contain one or more NaN values. It is useful for
    cleaning the data before performing further analysis or processing.

    :param data: The DataFrame from which rows with NaN values will be removed.
    :return: A DataFrame with rows containing NaN values dropped.
    """
    data.dropna(inplace=True, axis=0)
    return data


def transform_timestamp(data: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the 'timestamp' column in the DataFrame to datetime and adds columns for year, semester, 
    trimester, and month based on the timestamp.

    This function transforms the existing 'timestamp' column in the DataFrame from a string to a datetime object
    and then derives additional time-related columns:
        - 'year': Extracts the year from the timestamp.
        - 'semester': Creates a value indicating the semester (1 for the first half of the year, 2 for the second).
        - 'trimester': Indicates the trimester of the year (1-4).
        - 'month': Extracts the month of the year.

    :param data: The DataFrame that contains the 'timestamp' column to be transformed.
    :return: The DataFrame with new columns added: 'year', 'semester', 'trimester', and 'month'.
    """
    # Convert the 'timestamp' column to datetime
    data['timestamp'] = pd.to_datetime(data['timestamp'], format='%m/%d/%Y')

    # Create the new columns
    data['year'] = data['timestamp'].dt.year
    data['semester'] = (data['timestamp'].dt.month > 6).astype(int) + 1
    data['trimester'] = data['timestamp'].dt.quarter
    data['month'] = data['timestamp'].dt.month
    
    return data

def save_df_in_db(data: pd.DataFrame, stats: StatisticsManager) -> pd.DataFrame:
    """
    Saves a DataFrame containing sales data into the database, handling foreign key relationships and updating statistics.

    This function processes each row of the DataFrame and inserts it into the appropriate tables in the database:
        - First, it updates the statistics with the price of the sale.
        - It then checks for existing user data in the `DimUser` table, inserting a new record if the user doesn't exist.
        - The function also checks for existing time data in the `DimTime` table, inserting a new record if necessary.
        - Finally, a new row is inserted into the `FactSales` table, linking the user and time data with a sales price.

    :param data: The DataFrame containing the sales data to be saved.
    :param stats: An instance of the `StatisticsManager` class for updating sales statistics.
    :return: The original DataFrame with sales data after being processed and saved to the database.
    """
    db_connection = Db()
    session = db_connection.SessionLocal()  # Create a new session
    
    for _, row in data.iterrows():
        # Extract values from each row of the DataFrame
        user_key_df = row['user_id']
        price = row['price']
        date = row['timestamp']
        year = row['year']
        semester = row['semester']
        trimester = row['trimester']
        month = row['month']

        # Update statistics
        stats.update_statistics(price)
        logging.debug(f'Add row, New Stats.\n{stats.get_statistics()}')

        # Handle foreign key relations for DimUser and DimTime
        user_data = session.query(DimUser).filter(DimUser.user_key == user_key_df).first()
        if not user_data:
            user_data = DimUser(user_key=user_key_df)
            session.add(user_data)
            session.commit()  # Commit to get the ID of the new row
            session.refresh(user_data)  # Refresh to get the assigned ID

        time_data = session.query(DimTime).filter(DimTime.date == date).first()
        if not time_data:
            time_data = DimTime(date=date,
                                year=year,
                                semester=semester,
                                trimester=trimester,
                                month=month)
            session.add(time_data)
            session.commit()  # Commit to get the ID of the new row
            session.refresh(time_data)  # Refresh to get the assigned ID

        # Insert new row into FactSales
        new_fact = FactSales(
            user_id=user_data.id,
            time_id=time_data.id,
            price=price
        )        
        session.add(new_fact)
        
    session.commit()  # Commit all changes to the database
    return data

def stats_from_db() -> None:
    """
    Retrieves statistical data from the `FactSales` table, including the minimum, maximum, and average price, 
    as well as the total record count.

    The function constructs and executes a SQL query that computes the following statistics:
        - Minimum price (`min`).
        - Maximum price (`max`).
        - Average price (`average`), rounded to two decimal places.
        - The total number of records (`record_count`).

    The results are returned as a pandas DataFrame for easy handling and further processing.

    :return: A pandas DataFrame containing the statistical data (min, max, average, record_count).
    """
    db_connection = Db()
    session = db_connection.SessionLocal()  # Create a new session
    
    # Build the query to calculate statistics
    query = select(
        func.min(FactSales.price).label("min"),
        func.max(FactSales.price).label("max"),
        func.round(func.avg(FactSales.price), 2).label("average"),
        func.count(FactSales.id).label("record_count"),
    ).select_from(FactSales)
    
    # Execute the query and fetch the result
    result = session.execute(query).fetchone()
    
    # Return the result as a pandas DataFrame
    return pd.DataFrame([result._asdict()])