import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Root@123",
    host="localhost",
    port="5432",
)

# Execute SQL query to fetch relevant columns from xdr_data table
query = """
    SELECT "MSISDN/Number", "Avg RTT DL (ms)", "Avg RTT UL (ms)",
           "Avg Bearer TP DL (kbps)", "Avg Bearer TP UL (kbps)",
           "TCP DL Retrans. Vol (Bytes)", "TCP UL Retrans. Vol (Bytes)"
    FROM public.xdr_data
"""
df = pd.read_sql_query(query, conn)

# Close connection
conn.close()

# Calculate experience score
# Define weights for each metric
weights = {
    "Avg RTT DL (ms)": 0.25,
    "Avg RTT UL (ms)": 0.25,
    "Avg Bearer TP DL (kbps)": 0.25,
    "Avg Bearer TP UL (kbps)": 0.25,
    "TCP DL Retrans. Vol (Bytes)": -0.25,
    "TCP UL Retrans. Vol (Bytes)": -0.25,
}

# Normalize metrics
for column in df.columns[1:]:
    df[column + "_norm"] = (df[column] - df[column].min()) / (
        df[column].max() - df[column].min()
    )

# Calculate experience score
df["experience_score"] = (
    (df["Avg RTT DL (ms)_norm"] * weights["Avg RTT DL (ms)"])
    + (df["Avg RTT UL (ms)_norm"] * weights["Avg RTT UL (ms)"])
    + (df["Avg Bearer TP DL (kbps)_norm"] * weights["Avg Bearer TP DL (kbps)"])
    + (df["Avg Bearer TP UL (kbps)_norm"] * weights["Avg Bearer TP UL (kbps)"])
    + (df["TCP DL Retrans. Vol (Bytes)_norm"] * weights["TCP DL Retrans. Vol (Bytes)"])
    + (df["TCP UL Retrans. Vol (Bytes)_norm"] * weights["TCP UL Retrans. Vol (Bytes)"])
)

# Fill missing values with the mean of the respective columns
df.fillna(df.mean(), inplace=True)


# Save DataFrame to CSV file
df[["MSISDN/Number", "experience_score"]].to_csv(
    "../data/experience_scores.csv", index=False
)


# Display the DataFrame with MSISDN/Number and experience score
print(df[["MSISDN/Number", "experience_score"]])


# # Execute SQL queries to fetch data
# cur = conn.cursor()
# cur.execute("SELECT * FROM user_data")
# user_data = np.array(cur.fetchall())

# cur.execute("SELECT * FROM engagement_scores")
# engagement_scores = np.array(cur.fetchall())

# cur.execute("SELECT * FROM experience_scores")
# experience_scores = np.array(cur.fetchall())

# cur.execute("SELECT * FROM satisfaction_scores")
# satisfaction_scores = np.array(cur.fetchall())

# # Close cursor and connection
# cur.close()
# conn.close()

# # Create a DataFrame
# data = {
#     "user_id": user_data[:, 0],
#     "engagement_score": engagement_scores[:, 0],
#     "experience_score": experience_scores[:, 0],
#     "satisfaction_score": satisfaction_scores[:, 0],
# }
# df = pd.DataFrame(data)

# # Connect to MySQL database
# engine = create_engine("mysql://root:Root@123@localhost/statics_for_telecom")

# # Export DataFrame to MySQL database
# df.to_sql("customer_scores", con=engine, if_exists="replace", index=False)

# # Close the database connection
# engine.dispose()

# print("Data exported to MySQL database successfully.")
