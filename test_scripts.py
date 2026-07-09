from pathlib import Path
from training_loader import find_all_workbooks

"""
This script scans the training_data folder for all Excel workbooks and prints their paths."""
workbooks = find_all_workbooks(Path("training data"))

for item in workbooks:
    print(item)