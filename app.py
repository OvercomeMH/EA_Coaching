# Save this script as app.py

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title('Financial Analysis of Coaching Program for Founders')

st.markdown("""
This interactive app allows you to adjust key variables of a coaching program for founders and see how these changes affect the financial outcomes, including the expected value (EV) and return on investment (ROI).
""")

# ==========================================================
#                 USER INPUT SECTION WITH SLIDERS
# ==========================================================

st.header('Adjustable Parameters')

# 1. Program Costs
st.subheader('Program Costs')
st.write('Adjust the total cost of running the coaching program, including all expenses.')

total_coaching_cost = st.slider(
    'Total Coaching Cost ($)',
    min_value=10000,
    max_value=50000,
    value=60000,
    step=2500,
    help= 'default = our current budget'
)

# 2. Number of Founders Affected
st.subheader('Number of Founders Affected')
st.write('Set the total number of founders participating in the coaching program.')

total_founders = st.slider(
    'Total Number of Founders who attend at least one session',
    min_value=10,
    max_value=500,
    value=172,
    step=1,
    help = "default = the most we could see using the staff we'd hire to run the program"
)

# 3. Success Metrics
st.subheader('Success Metrics')
st.write('Define the percentage of founders who complete the coaching program. The average for founders, coached by paid staff is 100% (n=12). The average for EAs in general is ~70% (n>100).')

retention_rate = st.slider(
    'Retention Rate (%)',
    min_value=0.0,
    max_value=100.0,
    value=80.0,
    step=1.0,
) / 100

# 4. Outcome Parameters
st.subheader('Outcome Parameters')
st.write('Choose how to calculate the productivity increase resulting from the program.')

# Radio buttons for selecting the calculation method
outcome_method = st.radio(
    'Select Outcome Calculation Method:',
    ('Use Mean Life Satisfaction Points Earned', 'Input Productivity Increase Directly')
)

if outcome_method == 'Use Mean Life Satisfaction Points Earned':
    st.write('Input the mean life satisfaction points earned and the percentage increase in productivity per point.')
    mean_life_satisfaction_points = st.slider(
        'Mean Life Satisfaction Points Earned',
        min_value=0.1,
        max_value=5.0,
        value=0.64,
        step=0.01
    )
    
    percentage_increase_productivity_per_point = st.slider(
        'Percentage Increase in Productivity per Life Satisfaction Point (%)',
        min_value=1.0,
        max_value=50.0,
        value=13.95,
        step=0.1
    )
    
    # Calculate total productivity increase
    productivity_increase_per_retained_founder = mean_life_satisfaction_points * (percentage_increase_productivity_per_point / 100)
else:
    st.write('Input the overall productivity increase as a result of the program.')
    productivity_increase_per_retained_founder = st.slider(
        'Productivity Increase per Retained Founder (%)',
        min_value=0.1,
        max_value=100.0,
        value=8.93,  # Default value from 0.64 * 13.95
        step=0.1
    ) / 100

# 5. Expected Value Metrics
st.subheader('Expected Value Metrics')
st.write('Set the monetary value a founder contributes to the organization per year.')

ev_per_founder_per_year = st.slider(
    'Expected Value per Founder per Year ($)',
    min_value=30000,
    max_value=1000000,
    value=217000,
    step=1000,
    help = "default = Charity Entrepreurship's conservative estimate (2018)"
)

# 6. Founder Time Costs
st.subheader('Founder Time Costs')
st.write('Adjust the cost associated with one hour of a founder\'s time.')

founder_hourly_rate = st.slider(
    'Founder Hourly Rate ($/hour)',
    min_value=10.0,
    max_value=200.0,
    value=52.47,
    step=0.1
)

st.write('Set the percentage of coaching time that occurs during work hours, impacting the opportunity cost.')

proportion_time_during_work = st.slider(
    'Proportion of Coaching Time During Work Hours (%)',
    min_value=0.0,
    max_value=100.0,
    value=100.0,
    step=1.0
) / 100

# ==========================================================
#            CALCULATIONS BASED ON USER INPUTS
# ==========================================================

# Assumptions
# - Total weeks is set to 48 weeks
# - Sessions per founder is set to 12 (one session per month)
# - Homework hours per session is assumed to be 1 hour

total_weeks = 48  # Fixed value
sessions_per_founder = 12  # Fixed value
homework_hours_per_session = 1  # Fixed value

# Adjusted Sessions per Founder Considering Drop-Outs
# Assume drop-outs leave after session 2
average_sessions_per_founder = (
    (retention_rate * sessions_per_founder) +
    ((1 - retention_rate) * 2)  # Drop-outs attend 2 sessions
)

# Cost per session
total_sessions = total_founders * average_sessions_per_founder
cost_per_session = total_coaching_cost / total_sessions

# Cost per founder
cost_per_founder = cost_per_session * average_sessions_per_founder

# Total founder hours spent
# Founders spend time only during the proportion specified
# Drop-outs spend time for 2 sessions, retained founders for the full sessions
founder_hours_retained = (
    retention_rate *
    total_founders *
    sessions_per_founder *
    homework_hours_per_session *
    proportion_time_during_work
)

founder_hours_dropouts = (
    (1 - retention_rate) *
    total_founders *
    2 *
    homework_hours_per_session *
    proportion_time_during_work
)

total_founder_hours = founder_hours_retained + founder_hours_dropouts

# Total cost of founder time
total_founder_time_cost = total_founder_hours * founder_hourly_rate

# Total expected value gained
total_retained_founders = retention_rate * total_founders
total_expected_value_gained = (
    total_retained_founders *
    ev_per_founder_per_year *
    productivity_increase_per_retained_founder
)

# Net expected value
net_expected_value = (
    total_expected_value_gained -
    total_coaching_cost -
    total_founder_time_cost
)

# Return on investment
roi_to_funders = net_expected_value / total_coaching_cost if total_coaching_cost != 0 else np.nan
roi_to_founders = net_expected_value / total_founder_time_cost if total_founder_time_cost != 0 else np.nan

# New calculations for additional productive hours
# Assumed working hours per year
working_hours_per_year = 1920  # 40 hours/week * 48 weeks/year

# Additional productive hours per retained founder
additional_hours_per_founder = working_hours_per_year * productivity_increase_per_retained_founder

# Total additional productive hours gained
total_additional_hours = additional_hours_per_founder * total_retained_founders

# Expense per additional productive hour gained
cost_per_additional_hour = total_coaching_cost / total_additional_hours if total_additional_hours != 0 else np.nan

# ==========================================================
#                DISPLAY RESULTS AND VISUALIZATIONS
# ==========================================================

st.header('Financial Analysis Results')

st.subheader('Key Financial Metrics')

col1, col2 = st.columns(2)

with col1:
    st.metric('Total Coaching Cost', f"${total_coaching_cost:,.2f}")
    st.metric('Total Founder Time Cost', f"${total_founder_time_cost:,.2f}")
    st.metric('Total Investment', f"${total_coaching_cost + total_founder_time_cost:,.2f}")

with col2:
    st.metric('Total Expected Value Gained', f"${total_expected_value_gained:,.2f}")
    st.metric('Net Expected Value', f"${net_expected_value:,.2f}")
    st.metric('ROI to Funders', f"{roi_to_funders:.2f}")
    st.metric('ROI to Founders', f"{roi_to_founders:.2f}")

st.subheader('Additional Metrics')

st.write(f"**Cost per Session:** ${cost_per_session:.2f}")
st.write(f"**Average Sessions per Founder:** {average_sessions_per_founder:.2f}")
st.write(f"**Cost per Founder:** ${cost_per_founder:.2f}")
st.write(f"**Total Founder Hours Spent:** {total_founder_hours:.2f} hours")
st.write(f"**Productivity Increase per Retained Founder:** {productivity_increase_per_retained_founder * 100:.2f}%")
st.write(f"**Total Number of Retained Founders:** {total_retained_founders:.2f}")
st.write(f"**Total Additional Productive Hours Gained:** {total_additional_hours:,.2f} hours")
st.write(f"**Cost per Additional Productive Hour Gained:** ${cost_per_additional_hour:.2f}")

# Visualizations

st.subheader('Costs and Benefits Analysis')

# Prepare data for visualization
labels = [
    'Total Coaching Cost',
    'Founder Time Cost',
    'Total Expected Value Gained',
    'Net Expected Value'
]
values = [
    total_coaching_cost,
    total_founder_time_cost,
    total_expected_value_gained,
    net_expected_value
]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

fig1, ax1 = plt.subplots(figsize=(10, 6))
bars = ax1.bar(labels, values, color=colors)
ax1.set_ylabel('Amount ($)')
ax1.set_title('Costs and Benefits Analysis')
ax1.tick_params(axis='x', rotation=45)

# Annotate bars with values
for bar in bars:
    yval = bar.get_height()
    ax1.text(
        bar.get_x() + bar.get_width()/2.0,
        yval + max(values)*0.01 if yval >= 0 else yval - max(values)*0.05,
        f'${yval:,.0f}',
        ha='center',
        va='bottom' if yval >= 0 else 'top'
    )

st.pyplot(fig1)

st.subheader('Return on Investment Comparison')

roi_labels = ['ROI to Funders', 'ROI to Founders']
roi_values = [roi_to_funders, roi_to_founders]
roi_colors = ['#17becf', '#e377c2']

fig3, ax3 = plt.subplots(figsize=(6, 6))
bars_roi = ax3.bar(roi_labels, roi_values, color=roi_colors)
ax3.set_ylabel('Return on Investment')
ax3.set_title('ROI Comparison')
ax3.tick_params(axis='x', rotation=45)
ax3.set_ylim(min(roi_values) - 1, max(roi_values) + 1)

# Annotate bars with values
for bar in bars_roi:
    yval = bar.get_height()
    ax3.text(
        bar.get_x() + bar.get_width()/2.0,
        yval + (max(roi_values)*0.05 if yval >= 0 else min(roi_values)*0.05),
        f'{yval:.2f}',
        ha='center'
    )

st.pyplot(fig3)

# ==========================================================
#                PRACTICAL SIGNIFICANCE EXPLANATION
# ==========================================================

st.markdown("""
---
""")

st.header('Understanding the Impact')

st.markdown(f"""
Based on the inputs provided:

- **For every dollar invested in the coaching program**, supported charities gain value equal to a donation of **${roi_to_funders:.2f}** dollars.

- **For every dollar founders invest in terms of their time**, they can expect a return of **${roi_to_founders:.2f}** in net value.

- **The program generates a total of {total_additional_hours:,.2f} additional productive hours**, effectively **buying an hour of founder time for ${cost_per_additional_hour:.2f}**.

- The total expected value gained from the program is **${total_expected_value_gained:,.2f}**, generated by **{total_retained_founders:.0f}** founders who complete the program and experience an average productivity increase of **{(productivity_increase_per_retained_founder * 100):.2f}%**.

- The total investment required is **${(total_coaching_cost + total_founder_time_cost):,.2f}**, which includes:
    - The coaching costs of **${total_coaching_cost:,.2f}**
    - The opportunity cost of the founders' time during work hours of **${total_founder_time_cost:,.2f}**

This means that **each dollar you invest in the coaching program** is expected to generate **${(total_expected_value_gained / total_coaching_cost):.2f}** in increased founder productivity.

Another way of viewing it is that **you're effectively buying an hour of a founder's time for ${cost_per_additional_hour:.2f}**.

---

**Note:** This analysis assumes that the benefits are realized over **one year** and that there are **no lasting benefits** beyond that period.
""")

# ==========================================================
#                END OF APP
# ==========================================================
