from dotenv import load_dotenv
import logging
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from typing import Generator

class Db:
    """
    Class to handle database operations using SQLAlchemy.

    This class provides the necessary methods to interact with a MySQL databas. It supports working with 
    SQLAlchemy models and performing database transactions.

    Attributes:
        engine (Engine): SQLAlchemy engine connected to the MySQL database.
        SessionLocal (Session): SQLAlchemy session maker to interact with the database.

    Methods:
        __init__: Initializes the database connection using environment variables.
    """
    
    def __init__(self):
        """
        Initializes the service with the database connection settings.

        The method loads environment variables from a `.env` file to configure the database 
        connection and sets up the SQLAlchemy engine and session maker.

        Environment variables required:
            - DB_USER: Username for the MySQL database.
            - DB_PASSWORD: Password for the MySQL database.
            - DB_DIRECTION: Database server address.
            - DB_PORT: Port for connecting to the MySQL server.
            - DB_TO_USE: Name of the database to connect to.
        """
        load_dotenv()  # Load environment variables from the .env file

        # Create the MySQL database connection URL
        url_database = (
            f"mysql+pymysql://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}"
            f"@{getenv('DB_DIRECTION')}:{getenv('DB_PORT')}/{getenv('DB_TO_USE')}"
        )
        
        # Create the SQLAlchemy engine for database interaction
        self.engine = create_engine(url_database)
        
        # Create a session maker to interact with the database
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
