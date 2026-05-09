import pandas as pd

# This function reads an Excel file containing expense data, analyzes it against predefined budgets, and returns a summary of spending by category along with total spending and budget information.
def analyze_expenses(file_path, budgets):
    df = pd.read_excel(file_path)

    required_columns = [
        "Transaction Date",
        "Transaction Type",
        "Category",
        "Amount",
        "Cumulative Amount"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    category_spending = df.groupby("Category")["Amount"].sum()

    results = {}

    for category, budget in budgets.items():
        spent = category_spending.get(category, 0)
        remaining = budget - spent

        results[category] = {
            "budget": budget,
            "spent": spent,
            "remaining": remaining,
            "over_budget": spent > budget
        }

    total_spent = df["Amount"].sum()
    total_budget = sum(budgets.values())

    return results, total_spent, total_budget