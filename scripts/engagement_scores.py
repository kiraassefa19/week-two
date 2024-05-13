import pandas as pd
import psycopg2

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
    SELECT "MSISDN/Number", "Dur. (ms)", "Total UL (Bytes)", "Total DL (Bytes)"
    FROM public.xdr_data
"""
df = pd.read_sql_query(query, conn)

# Close connection
conn.close()

# Calculate engagement score
# Define weights for each metric
weights = {
    "Dur. (ms)": 0.4,
    "Total UL (Bytes)": 0.3,
    "Total DL (Bytes)": 0.3,
}

# Normalize metrics
for column in df.columns[1:]:
    df[column + "_norm"] = (df[column] - df[column].min()) / (
        df[column].max() - df[column].min()
    )

# Calculate engagement score
df["engagement_score"] = (
    df["Dur. (ms)_norm"] * weights["Dur. (ms)"]
    + df["Total UL (Bytes)_norm"] * weights["Total UL (Bytes)"]
    + df["Total DL (Bytes)_norm"] * weights["Total DL (Bytes)"]
)

# Fill missing values with the mean of the respective columns
df.fillna(df.mean(), inplace=True)

# Save DataFrame to CSV file
df[["MSISDN/Number", "engagement_score"]].to_csv(
    "../data/engagement_scores.csv", index=False
)

# Display the DataFrame with MSISDN/Number and engagement score
print(df[["MSISDN/Number", "engagement_score"]])
