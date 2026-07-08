import pandas as pd

from features import extract_features


def build_training_dataset(transactions, budgets):

    dataset = []

    # Ensure dates are datetime
    transactions = transactions.copy()
    transactions["Transaction Date"] = pd.to_datetime(
        transactions["Transaction Date"]
    )

    # Process one month at a time
    for month, df in transactions.groupby("Month"):

        features = extract_features(df, budgets)

        features["month"] = month

        dataset.append(features)

    return pd.DataFrame(dataset)