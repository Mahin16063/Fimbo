from pathlib import Path

# scans the current directory for a file named "tracker.csv" and sets the path to it
DATA_FOLDER = Path("data")
TRACKER_FILE = DATA_FOLDER / "tracker.csv"

# predefined budgets for each category, can be modified as needed
BUDGETS = {
    "Food": 300,
    "Transport": 120,
    "Rent": 900,
    "Entertainment": 100,
    "Shopping": 150,
    "Subscriptions": 50,
    "Misc": 100
}