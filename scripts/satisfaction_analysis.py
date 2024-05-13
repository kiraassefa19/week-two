import pymysql
from sqlalchemy import create_engine
import pandas as pd
import urllib.parse

# Define the cluster statistics DataFrame
cluster_data = {
    "Cluster": [0, 1],
    "Engagement Satisfaction Score": [4.026023, 2.034945],
    "Engagement Experience Score": [4.026023, 2.034945],
    "Experience Satisfaction Score": [4.026023, 2.034945],
    "Experience Experience Score": [4.026023, 2.034945],
}
df = pd.DataFrame(cluster_data)

# Encode the password
password = urllib.parse.quote_plus("Root@123")

# Connect to MySQL database
conn = pymysql.connect(
    host="localhost",
    user="root",
    password=password,
    database="statics_for_telecom",
)

# Define the SQLAlchemy engine with the correct connection string format
engine = create_engine(
    f"mysql+pymysql://root:{password}@localhost:3306/statics_for_telecom"
)

# Export DataFrame to MySQL
df.to_sql("cluster_statistics", con=engine, if_exists="replace", index=False)

# Close connection
conn.close()
