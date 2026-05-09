from config import DATA_FOLDER, BUDGETS
from file_scanner import find_latest_excel_file
from analyzer import analyze_expenses
from voice import speak

def main():
    speak("Welcome back Mahin. I am scanning your finance folder now.")

    try:
        latest_file = find_latest_excel_file(DATA_FOLDER)
        speak(f"I found your latest finance file: {latest_file.name}")

        results, total_spent, total_budget = analyze_expenses(latest_file, BUDGETS)

        speak(f"Your total spending is {total_spent:.2f} dollars out of a total budget of {total_budget:.2f} dollars.")

        for category, data in results.items():
            spent = data["spent"]
            budget = data["budget"]
            remaining = data["remaining"]

            if data["over_budget"]:
                speak(f"You overspent in {category} by {abs(remaining):.2f} dollars.")
            else:
                speak(f"For {category}, you spent {spent:.2f} dollars out of {budget:.2f}. You have {remaining:.2f} dollars remaining.")

    except Exception as error:
        speak(f"Something went wrong. {error}")

if __name__ == "__main__":
    main()