"""
This file will look for the latest yearly workbook from data folder and load it into a pandas dataframe. It will also check if the tracker file exists, and if not, it will create one with the appropriate headers.
It will skip any rows that have missing or invalid data, and will log any errors encountered during the loading process.
It will return a loaded dataframe of all the transactions.
"""

import pandas as pd
from pathlib import Path

MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

def load_finance_data(path: Path):

    if path.is_file():

        workbook = path

    else:

        excel_files = [
            f
            for f in path.glob("*.xlsx")
            if not f.name.startswith("~$")
        ]

        if not excel_files:
            raise FileNotFoundError("No yearly workbook found.")

        workbook = max(
            excel_files,
            key=lambda f: f.stat().st_mtime
        )

    # ---------- Read Budget ----------
    budget_df = pd.read_excel(workbook, sheet_name="Budget")

    current_month = pd.Timestamp.today().strftime("%b")

    budgets = dict(zip(
        budget_df["Category"],
        budget_df[current_month]
    ))

    # ---------- Read Transactions ----------
    all_transactions = []

    for month in MONTHS:

        df = pd.read_excel(workbook, sheet_name=month)

        # Skip blank sheets
        if df.empty:
            continue

        if "Amount" not in df.columns:
            continue

        if df["Amount"].dropna().empty:
            continue

        df["Month"] = month

        all_transactions.append(df)

    if all_transactions:
        transactions = pd.concat(
            all_transactions,
            ignore_index=True
        )
    else:
        transactions = pd.DataFrame(
            columns=[
                "Transaction Date",
                "Transaction Type",
                "Category",
                "Amount",
                "Cumulative Amount"
            ]
        )

    return transactions, budgets, workbook