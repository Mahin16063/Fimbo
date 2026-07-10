import pandas as pd
from features import extract_features
from pathlib import Path
from training_loader import find_all_workbooks
from data_loader import load_finance_data


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


def build_master_dataset(training_folder: Path):

    master_dataset = []

    workbooks = find_all_workbooks(training_folder)

    for item in workbooks:

        user = item["user"]

        workbook = item["workbook"]

        transactions, budgets, workbook_path = load_finance_data(workbook)

        monthly_dataset = build_training_dataset(
            transactions,
            budgets
        )

        monthly_dataset["user"] = user

        monthly_dataset["year"] = workbook.stem

        master_dataset.append(monthly_dataset)

        print(monthly_dataset.head())
    
    if not master_dataset:
        return pd.DataFrame()

    return pd.concat(
        master_dataset,
        ignore_index=True
)


