import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import urllib.parse

# Database Configuration
DB_USERNAME = "root"
DB_PASSWORD = "Root@123"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "statics_for_telecom"

csv_file_path = "../data/final.csv"

# Encode username and password
encoded_username = urllib.parse.quote_plus(DB_USERNAME)
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

# MySQL connection URL without 'useSSL' parameter
DB_URL = f"mysql://{encoded_username}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(DB_URL)

# Create Session
Session = sessionmaker(bind=engine)
session = Session()

# Now you can use 'session' to interact with the database
# Read CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file_path)

# Export DataFrame to MySQL database
try:
    df.to_sql("final_table", con=engine, if_exists="replace", index=False)
    print("Data successfully exported to MySQL database.")
except Exception as e:
    print("An error occurred while exporting data to MySQL database:", e)
