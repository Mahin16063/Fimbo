import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from config import FINANCE_FOLDER
from analyzer import analyze_expenses, analyze_monthly_trends
from insight import generate_insights
from predictor import predict_month_end
from data_loader import load_finance_data
from features import extract_features
from dataset_builder import build_training_dataset

plt.rcParams.update({
    "text.color": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "axes.edgecolor": "white",
})

st.set_page_config(page_title="Fimbo Financial Advisor", layout="wide")

st.title("Fimbo Financial Advisor Dashboard")

st.markdown(
    """
    Welcome back!

    Here's your financial overview for this month.
    """
)

transactions, budgets, workbook = load_finance_data(FINANCE_FOLDER)

df = transactions

results, total_spent, total_budget = analyze_expenses(
    transactions,
    budgets
)



# =========================
# TOP METRICS
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Budget", f"${total_budget:.2f}")

with col2:
    st.metric("💳 Spent", f"${total_spent:.2f}")

with col3:
    remaining = total_budget - total_spent
    st.metric("🏦 Remaining", f"${remaining:.2f}")

with col4:
    savings = (remaining / total_budget) * 100
    st.metric("📈 Savings", f"{savings:.1f}%")
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

features = extract_features(df, budgets)

# temporary display of extracted features for debugging purposes
st.subheader("🧪 Extracted Features")

st.json(features)

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
# MONTHLY DATA FEATURES
# =========================

training_df = build_training_dataset(df, budgets)

st.subheader("Training Dataset")

st.dataframe(training_df)


# =========================
# MONTHLY TRENDS
# =========================
monthly_total, monthly_category = analyze_monthly_trends(df)

st.subheader("Monthly Spending Trend")

fig3, ax3 = plt.subplots(figsize=(6, 3))

fig3.patch.set_alpha(0)
ax3.set_facecolor("none")

ax3.plot(
    monthly_total["Month Name"],
    monthly_total["Amount"],
    marker="o",
    linewidth=2
)

ax3.set_ylabel("Amount ($)", color="white")
ax3.set_xlabel("Month", color="white")

ax3.tick_params(axis="x", labelrotation=35, labelsize=8, colors="white")
ax3.tick_params(axis="y", labelsize=8, colors="white")

for spine in ax3.spines.values():
    spine.set_color("white")

st.pyplot(fig3, transparent=True)

# Monthly Category Breakdown

st.subheader("Fimbo's Financial Insights")

insights = generate_insights(
    results,
    total_spent,
    total_budget,
    monthly_total
)

for insight in insights:
    st.markdown(f"- {insight}")

# =========================
# PREDICTIONS
# =========================

prediction = predict_month_end(df, budgets)

st.subheader("🔮 Orchid's Forecast")

if prediction:

    predicted = prediction["predicted_total"]

    budget = prediction["budget"]

    if predicted > budget:

        st.error(
            f"At your current spending pace, "
            f"you are projected to spend "
            f"${predicted:.2f}, exceeding your "
            f"budget by ${predicted-budget:.2f}."
        )

    else:

        st.success(
            f"You're projected to spend "
            f"${predicted:.2f} this month, "
            f"leaving approximately "
            f"${budget-predicted:.2f} remaining."
        )

    st.metric(
        "Average Daily Spending",
        f"${prediction['average_daily']:.2f}"
    )




# =========================
# SPENDING ADVICE
# =========================

st.subheader("Spending Insights")

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