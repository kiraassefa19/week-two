import pandas as pd

# Load the CSV files
engagement_df = pd.read_csv("../data/engagement_scores.csv")
experience_df = pd.read_csv("../data/experience_scores.csv")
satisfied_customers_df = pd.read_csv("../data/top_satisfied_customers.csv")
user_interaction_df = pd.read_csv("../data/user_interaction_with_scores.csv")

# Identify unique MSISDN/Number values in each DataFrame
unique_msisdn_engagement = engagement_df["MSISDN/Number"].unique()
unique_msisdn_experience = experience_df["MSISDN/Number"].unique()
unique_msisdn_satisfied = satisfied_customers_df["MSISDN/Number"].unique()
unique_msisdn_interaction = user_interaction_df["MSISDN/Number"].unique()

# Find the intersection of unique MSISDN/Number values across all DataFrames
common_msisdn = set(unique_msisdn_engagement).intersection(
    unique_msisdn_experience, unique_msisdn_satisfied, unique_msisdn_interaction
)

# Filter DataFrames to include only common MSISDN/Number values
engagement_df = engagement_df[engagement_df["MSISDN/Number"].isin(common_msisdn)]
experience_df = experience_df[experience_df["MSISDN/Number"].isin(common_msisdn)]
satisfied_customers_df = satisfied_customers_df[
    satisfied_customers_df["MSISDN/Number"].isin(common_msisdn)
]
user_interaction_df = user_interaction_df[
    user_interaction_df["MSISDN/Number"].isin(common_msisdn)
]

# Merge the DataFrames
final_df = pd.merge(engagement_df, experience_df, on="MSISDN/Number", how="outer")
final_df = pd.merge(final_df, satisfied_customers_df, on="MSISDN/Number", how="outer")
final_df = pd.merge(final_df, user_interaction_df, on="MSISDN/Number", how="outer")

# Save the final DataFrame to a CSV file
final_df.to_csv("../data/final.csv", index=False)
