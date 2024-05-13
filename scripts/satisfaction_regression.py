import pandas as pd

# Load engagement scores and experience scores from CSV files
engagement_df = pd.read_csv("../data/engagement_scores.csv")
experience_df = pd.read_csv("../data/experience_scores.csv")

# Merge the DataFrames on MSISDN/Number
merged_df = pd.merge(engagement_df, experience_df, on="MSISDN/Number", how="inner")

# Calculate satisfaction score (weighted average)
# Define weights for engagement and experience scores
weights = {"engagement_score": 0.5, "experience_score": 0.5}

# Calculate satisfaction score
merged_df["satisfaction_score"] = (
    merged_df["engagement_score"] * weights["engagement_score"]
) + (merged_df["experience_score"] * weights["experience_score"])

# Sort DataFrame by satisfaction score in descending order
top_satisfied_customers = merged_df.sort_values(
    by="satisfaction_score", ascending=False
).head(10)

# Save DataFrame to CSV file
top_satisfied_customers.to_csv("../data/top_satisfied_customers.csv", index=False)

# Display top satisfied customers
print("Top 10 Satisfied Customers:")
print(top_satisfied_customers)
