import pandas as pd

CATEGORY_COLUMNS = [
    "Food",
    "Rent",
    "Transport",
    "Shopping",
    "Entertainment",
    "Subscription",
    "Misc"
]


def extract_features(df, budgets):

    df = df.copy()

    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])

    features = {}

    # -----------------------------
    # Overall Spending
    # -----------------------------

    total_spent = df["Amount"].sum()

    total_budget = sum(budgets.values())

    features["total_spent"] = total_spent
    features["total_budget"] = total_budget
    features["budget_utilization"] = total_spent / total_budget

    # -----------------------------
    # Transactions
    # -----------------------------

    features["transaction_count"] = len(df)

    features["average_transaction"] = df["Amount"].mean()

    features["largest_transaction"] = df["Amount"].max()

    features["smallest_transaction"] = df["Amount"].min()

    features["transaction_std"] = df["Amount"].std()

    # -----------------------------
    # Daily
    # -----------------------------

    daily = (
        df.groupby("Transaction Date")["Amount"]
        .sum()
    )

    features["average_daily_spending"] = daily.mean()

    features["highest_daily_spending"] = daily.max()

    # -----------------------------
    # Weekend Spending
    # -----------------------------

    weekend = df[
        df["Transaction Date"].dt.dayofweek >= 5
    ]["Amount"].sum()

    features["weekend_ratio"] = (
        weekend / total_spent
        if total_spent > 0
        else 0
    )

    # -----------------------------
    # Category Percentages
    # -----------------------------

    category_totals = (
        df.groupby("Category")["Amount"]
        .sum()
    )

    category_totals = (
        df.groupby("Category")["Amount"]
        .sum()    
    )

    for category in CATEGORY_COLUMNS:

        amount = category_totals.get(category, 0)

        features[
            category.lower() + "_percentage"
        ] = (
            amount / total_spent
            if total_spent > 0
            else 0
        )

    features["over_budget"] = (
        total_spent > total_budget
    )

    return features