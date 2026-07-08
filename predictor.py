import pandas as pd
import calendar
from datetime import datetime


def predict_month_end(df, budgets):
    df = df.copy()

    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])

    # Keep only the current month
    today = pd.Timestamp.today()

    current = df[
        (df["Transaction Date"].dt.month == today.month) &
        (df["Transaction Date"].dt.year == today.year)
    ]

    if current.empty:
        return None

    current["Day"] = current["Transaction Date"].dt.day

    days_elapsed = current["Day"].max()

    total_spent = current["Amount"].sum()

    average_daily = total_spent / days_elapsed

    days_in_month = calendar.monthrange(today.year, today.month)[1]

    predicted_total = average_daily * days_in_month

    total_budget = sum(budgets.values())

    return {
        "average_daily": average_daily,
        "predicted_total": predicted_total,
        "remaining_budget": total_budget - total_spent,
        "budget": total_budget
    }