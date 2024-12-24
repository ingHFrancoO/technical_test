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
```
### 2. Create a Virtual Environment
```bash
python -m venv venv
```
Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux
```bash
source venv/bin/activate
```

### 3. Install Dependencies
After activating the virtual environment, install the required dependencies:
```bash
pip install -r requirements.txt
```
### 4. Set up environment variables
Create a `.env` file in the project root directory and add your database credentials and other configuration settings. Example `.env`:
```bash
DB_USER=root
DB_PASSWORD=yourpassword
DB_DIRECTION=localhost
DB_PORT=3306
DB_TO_USE=PragmaTest
```
### 5. Run the Application
Once the dependencies are installed and your environment is configured, you can run the application. Ensure your MySQL server is running, and execute the script that processes the CSV data and stores it in the database.
```bash
python your_script.py
```

## Project Structure
```bash
The project has the following structure:
│
├── config/                    # Configuration files for database and environment
│   ├── database.py            # Database connection setup
│   └── tables.py              # SQLAlchemy models for the database
│
├── data/                      # CSV files and processed data
│
├── utils/                     # Helper scripts for various utilities
│   ├── utils.py               # Script for processing data and saving to the database
│   └── stats_class.py         # Script for calculating statistics
│
├── requirements.txt           # List of dependencies for the project
├── README.md                  # Project documentation
├── main.py             # Main entry point for the application
└── .env                       # Environment variables for database credentials
```