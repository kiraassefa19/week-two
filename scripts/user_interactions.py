import pandas as pd

# Read the engagement score CSV file
engagement_df = pd.read_csv("../data/engagement_scores.csv")

# Read the experience score CSV file
experience_df = pd.read_csv("../data/experience_scores.csv")

# Merge engagement and experience data based on 'MSISDN/Number'
user_interaction_df = pd.merge(
    engagement_df, experience_df, on="MSISDN/Number", how="outer"
)

# Save the merged DataFrame to a new CSV file
user_interaction_df.to_csv("../data/user_interaction_with_scores.csv", index=False)
