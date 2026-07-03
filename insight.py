def generate_insights(results, total_spent, total_budget, monthly_total):

    insights = []

    # Overall budget
    if total_spent > total_budget:
        insights.append(
            f"🚨 You are over your total budget by ${total_spent-total_budget:.2f}."
        )
    else:
        insights.append(
            f"✅ You still have ${total_budget-total_spent:.2f} remaining this month."
        )

    # Biggest spending category
    biggest = max(results.items(), key=lambda x: x[1]["spent"])

    insights.append(
        f"💰 Your largest expense is {biggest[0]} (${biggest[1]['spent']:.2f})."
    )

    # Best managed category
    under_budget = [
        (cat, data)
        for cat, data in results.items()
        if not data["over_budget"]
    ]

    if under_budget:
        best = min(
            under_budget,
            key=lambda x: x[1]["spent"] / x[1]["budget"]
            if x[1]["budget"] > 0 else 1
        )

        insights.append(
            f"🏆 Your best managed category is {best[0]}."
        )

    # Most overspent category
    over_budget = [
        (cat, data)
        for cat, data in results.items()
        if data["over_budget"]
    ]

    if over_budget:
        worst = max(
            over_budget,
            key=lambda x: x[1]["spent"] - x[1]["budget"]
        )

        insights.append(
            f"⚠ {worst[0]} exceeded its budget by "
            f"${worst[1]['spent']-worst[1]['budget']:.2f}."
        )

    # Month-over-month trend
    if len(monthly_total) >= 2:

        current = monthly_total["Amount"].iloc[-1]
        previous = monthly_total["Amount"].iloc[-2]

        if previous > 0:

            change = (current - previous) / previous * 100

            if change > 0:
                insights.append(
                    f"📈 Spending increased {change:.1f}% compared to last month."
                )
            else:
                insights.append(
                    f"📉 Spending decreased {abs(change):.1f}% compared to last month."
                )

    return insights