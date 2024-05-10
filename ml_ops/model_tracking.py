import os
import datetime
import pandas as pd


# Model tracking function
def track_model_change(
    version, start_time, end_time, source, parameters, metrics, artifacts
):
    # Create ml_ops directory if it doesn't exist
    if not os.path.exists("ml_ops"):
        os.makedirs("ml_ops")

    # Record model details
    tracking_record = {
        "Version": version,
        "Start Time": start_time,
        "End Time": end_time,
        "Source": source,
        "Parameters": parameters,
        "Metrics": metrics,
        "Artifacts": artifacts,
    }

    # Append tracking record to CSV file
    tracking_file = "ml_ops/tracking.csv"
    if not os.path.exists(tracking_file):
        # Create new CSV file with header if it doesn't exist
        with open(tracking_file, "w") as f:
            f.write("Version,Start Time,End Time,Source,Parameters,Metrics,Artifacts\n")

    with open(tracking_file, "a") as f:
        f.write(",".join(str(tracking_record[key]) for key in tracking_record) + "\n")


# Example usage
if __name__ == "__main__":
    version = "1.0"
    start_time = datetime.datetime.now()

    # Your model training code here
    # For example, train a regression model
    from sklearn.linear_model import LinearRegression
    from sklearn.datasets import make_regression

    X, y = make_regression(n_samples=100, n_features=1, noise=0.1, random_state=42)
    model = LinearRegression()
    model.fit(X, y)

    end_time = datetime.datetime.now()
    source = "model_training.py"
    parameters = {"n_samples": 100, "noise": 0.1, "random_state": 42}
    metrics = {"r2_score": model.score(X, y)}
    artifacts = {"model.pkl": model}

    track_model_change(
        version, start_time, end_time, source, parameters, metrics, artifacts
    )
