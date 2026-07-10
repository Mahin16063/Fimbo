from pathlib import Path
from training_loader import find_all_workbooks

"""
This script scans the training_data folder for all Excel workbooks and prints their paths."""
# workbooks = find_all_workbooks(Path("training data"))

# for item in workbooks:
#     print(item)


"""
This script builds a master dataset from all the Excel workbooks in the training_data folder and prints the first few rows of each monthly dataset."""


# from dataset_builder import build_master_dataset

# build_master_dataset(Path("training data"))

"""This script builds a master dataset from all the Excel workbooks in the training_data folder and prints the first few rows of each monthly dataset."""

from dataset_builder import build_master_dataset

master_df = build_master_dataset(Path("training data"))

print(master_df)
print(master_df.info())