# Data Processing and Analytics Project

This project is a data processing and analytics application that integrates with a MySQL database. It processes CSV data, performs statistical calculations, and stores processed data in a database. The main focus is on sales data, which is transformed and stored in a database for further analysis.

## Features

- Load and process CSV files
- Clean and transform data
- Store processed data in a MySQL database
- Perform statistical calculations on the data
- Support for logging and error handling

## Requirements

To run this project, you will need Python and several Python libraries. The required libraries are listed in the `requirements.txt` file.

### Required Python Libraries:

- `sqlalchemy`: For database ORM interactions
- `pandas`: For data manipulation and processing
- `mysql-connector-python`: For connecting to MySQL
- `python-dotenv`: For loading environment variables from a `.env` file
- `numpy`: For numerical operations
- `loguru`: For improved logging management

## Setup

Follow these steps to set up the project:

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/yourproject.git

### Create a Virtual Environment
```bash
python -m venv venv