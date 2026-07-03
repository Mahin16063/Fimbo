import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from config import DATA_FOLDER, BUDGETS
from file_scanner import find_latest_excel_file
from analyzer import analyze_expenses, analyze_monthly_trends

plt.rcParams.update({
    "text.color": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "axes.edgecolor": "white",
})

st.set_page_config(page_title="Fimbo Financial Advisor", layout="wide")

st.title("Fimbo Financial Advisor Dashboard")

latest_file = find_latest_excel_file(DATA_FOLDER)

df = pd.read_excel(latest_file)

results, total_spent, total_budget = analyze_expenses(
    latest_file,
    BUDGETS
)

# =========================
# TOP METRICS
# =========================

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Spent", f"${total_spent:.2f}")

with col2:
    st.metric("Total Budget", f"${total_budget:.2f}")

# =========================
# CATEGORY TABLE
# =========================

st.subheader("Category Breakdown")

table_data = []

for category, data in results.items():
    table_data.append({
        "Category": category,
        "Spent": data["spent"],
        "Budget": data["budget"],
        "Remaining": data["remaining"]
    })

table_df = pd.DataFrame(table_data)

st.dataframe(table_df)

# =========================
# CHARTS    
# =========================

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Expense Distribution")

    category_totals = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots(figsize=(4, 4))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    ax.pie(
        category_totals,
        labels=category_totals.index,
        autopct="%1.1f%%",
        textprops={"color": "white", "fontsize": 8}
    )

    ax.axis("equal")
    st.pyplot(fig, transparent=True)

with chart_col2:
    st.subheader("Budget vs Spending")

    fig2, ax2 = plt.subplots(figsize=(5, 3))
    fig2.patch.set_alpha(0)
    ax2.set_facecolor("none")

    categories = table_df["Category"]

    ax2.bar(categories, table_df["Budget"], label="Budget")
    ax2.bar(categories, table_df["Spent"], label="Spent")

    ax2.legend(facecolor="none", labelcolor="white")

    ax2.tick_params(axis="x", labelrotation=35, labelsize=8, colors="white")
    ax2.tick_params(axis="y", labelsize=8, colors="white")

    ax2.set_ylabel("Amount ($)", color="white")

    for spine in ax2.spines.values():
        spine.set_color("white")

    st.pyplot(fig2, transparent=True)


# =========================
# MONTHLY TRENDS
# =========================
monthly_total, monthly_category = analyze_monthly_trends(latest_file)

st.subheader("Monthly Spending Trend")

fig3, ax3 = plt.subplots(figsize=(6, 3))

fig3.patch.set_alpha(0)
ax3.set_facecolor("none")

ax3.plot(
    monthly_total.index,
    monthly_total.values,
    marker="o"
)

ax3.set_ylabel("Amount ($)", color="white")
ax3.set_xlabel("Month", color="white")

ax3.tick_params(axis="x", labelrotation=35, labelsize=8, colors="white")
ax3.tick_params(axis="y", labelsize=8, colors="white")

for spine in ax3.spines.values():
    spine.set_color("white")

st.pyplot(fig3, transparent=True)

# Monthly Category Breakdown

st.subheader("Monthly Trend Advice")

if len(monthly_total) >= 2:
    current_month = monthly_total.iloc[-1]
    previous_month = monthly_total.iloc[-2]

    difference = current_month - previous_month
    percent_change = (difference / previous_month) * 100

    if difference > 0:
        st.warning(
            f"Your spending increased by {percent_change:.1f}% compared to last month."
        )
    else:
        st.success(
            f"Your spending decreased by {abs(percent_change):.1f}% compared to last month."
        )
else:
    st.info("Not enough monthly data yet to compare trends.")



# =========================
# SPENDING ADVICE
# =========================

st.subheader("Spending Advice")

for category, data in results.items():

    if data["over_budget"]:
        st.warning(
            f"You overspent in {category} by "
            f"${abs(data['remaining']):.2f}"
        )

    elif data["remaining"] < data["budget"] * 0.2:
        st.info(
            f"You are close to reaching your "
            f"{category} budget."
        )

    else:
        st.success(
            f"Your {category} spending looks healthy."
        )