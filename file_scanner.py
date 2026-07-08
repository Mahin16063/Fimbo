from pathlib import Path
"""
This file was used to scan the data folder for the latest Excel file. It is no longer used in the current implementation, but it may be useful for future reference or modifications.
"""

def find_latest_excel_file(folder: Path):
    """
    Scans the specified folder for Excel files and returns the path to the most recently modified one.
    """
    # Get a list of all Excel files in the folder
    excel_files = list(folder.glob("*.xlsx"))

    if not excel_files:
        raise FileNotFoundError("No Excel files found in the data folder.")

    # Get the most recently modified Excel file
    latest_file = max(excel_files, key=lambda file: file.stat().st_mtime)
    return latest_file