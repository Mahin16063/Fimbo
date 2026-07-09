from pathlib import Path

def find_all_workbooks(training_folder: Path):

    workbooks = []

    for user_folder in training_folder.iterdir():

        if not user_folder.is_dir():
            continue

        for workbook in user_folder.glob("*.xlsx"):

            if workbook.name.startswith("~$"):
                continue

            workbooks.append({
                "user": user_folder.name,
                "workbook": workbook
            })

    return workbooks