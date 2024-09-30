# Save this script as app.py

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Set the page layout to wide
st.set_page_config(layout="wide")

st.title('Cost-Effectiveness Analysis for Founder Coaching Programme')

# ==========================================================
#                 INSTRUCTIONS
# ==========================================================

st.markdown("""

**Context**
We're Overcome, an EA-aligned mental health charity. You can see our pitch deck [here](https://www.canva.com/design/DAGM7Ubl1oA/fBZEjZuOavd0VkWIl2r2Gg/edit?utm_content=DAGM7Ubl1oA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton). 
We had a successful pilot coaching founders with our very best coaches. We want to hire those coaches and scale up our offering.            

**Instructions:**

- Use the sliders in the **Adjustable Parameters** section to modify the variables.
- The financial metrics and visualizations will update automatically based on your inputs.
- Hover over the charts to see more details.
""")

st.markdown("""
**Key Points:**

- One dollar of expected value, as defined here, is equivalent to one dollar donated to a GiveWell top charity.
- Play around with different values then look right to see how they affect the bottom line.
""")

# ==========================================================
#                 USER INPUT SECTION WITH SLIDERS
# ==========================================================

st.header('Adjustable Parameters')

# 1. Program Costs
st.subheader('Program Costs')
st.markdown(
    '<p style="font-size:16px; color:black;">Includes all associated costs. The default value, $60k, is all inclusive and what we\'re requesting. We could be ~30% more impactful by hiring a specialist, allowing us to treat more founders overall and give specialised support to those who need it.</p>',
    unsafe_allow_html=True
)
total_coaching_cost = st.slider(
    'Total Coaching Cost ($)',
    min_value=30000,  # Minimum value set to $30,000
    max_value=100000,
    value=60000,      # Default value set to $60,000
    step=1000
)

# 2. Number of Participating Founders
st.subheader('Number of Participating Founders')
st.markdown(
    '<p style="font-size:16px; color:black;">Should we not be able to max out our capacity, we\'ll offer the slots to other high-impact people with similar responsibilities (e.g. executives).</p>',
    unsafe_allow_html=True
)
total_founders = st.slider(
    'Total Number of Founders',
    min_value=10,
    max_value=500,
    value=172,
    step=1
)

# 3. Retention Metrics
st.subheader('Retention')
st.markdown(
    '<p style="font-size:16px; color:black;">Retention = proportion of founders to complete the programme. Our Pilot retained <90% of founders (n=12). Our general offerings to EAs retain ~70% (n= ~100).</p>',
    unsafe_allow_html=True
)
retention_rate = st.slider(
    'Retention Rate (%)',
    min_value=0.0,
    max_value=100.0,
    value=90.0,
    step=0.1
) / 100

# 4. Outcome Parameters
st.subheader('Outcome Parameters')

st.markdown(
    '<p style="font-size:16px; color:black;">We assume that all progress will be gone after this number of months to simplify the model.</p>',
    unsafe_allow_html=True
)
months_effects_last = st.slider(
    'Months Effects Last',
    min_value=1.0,
    max_value=12.0,
    value=5.14,
    step=0.1
)

st.markdown(
    '<p style="font-size:16px; color:black;">This is the most important variable but we are deeply uncertain and no hard evidence exists. Here are some relevant facts drawn from the general population: On average, depression reduces productivity by ~25% and anxiety is pretty similar. On average, our coaching clients gain two points of life satisfaction (measured on a scale of 0-10) over the first six weeks. Academic sources suggest each of life satisfafction point gained results in ~12 percent greater productivity.</p>',
    unsafe_allow_html=True
)

percentage_increase_in_productivity = st.slider(
    'Mean Increase in Productivity (%)',
    min_value=1.0,
    max_value=100.0,
    value=10.0,  # Default value set to 10%
    step=0.1
)

# 5. Expected Value Metrics
st.subheader('Expected Value Metrics')
st.markdown(
    '<p style="font-size:16px; color:black;">Charity entrepreneurship (2018), using conservative assumptions, estimate the expected value per founder is $217k per annum. That\'s our default value.</p>',
    unsafe_allow_html=True
)
ev_per_founder_per_year = st.slider(
    'Expected Value per Founder per Year ($)',
    min_value=10000,
    max_value=1000000,
    value=216000,
    step=2000
)

# 6. Founder Working Hours
st.subheader('Founder Working Hours')

working_hours_per_week = st.slider(
    'Working Hours per Week',
    min_value=10,
    max_value=80,
    value=55,  # Default value set to 55 hours per week
    step=1
)

working_weeks_per_year = st.slider(
    'Working Weeks per Year',
    min_value=1,
    max_value=52,
    value=48,
    step=1
)

# Calculating Cost per Founder Hour
total_working_hours_per_year = working_hours_per_week * working_weeks_per_year
cost_per_founder_hour = ev_per_founder_per_year / total_working_hours_per_year

# 7. Founder Opportunity Cost
st.subheader('Founder Opportunity Cost')

st.markdown(
    '<p style="font-size:16px; color:black;">Based on our estimates of tasks given to clients.</p>',
    unsafe_allow_html=True
)
homework_hours_per_session = st.slider(
    'Homework Hours per Session',
    min_value=0.0,
    max_value=10.0,
    value=1.0,  # Default value set to 1 hour
    step=0.1
)

st.markdown(
    '<p style="font-size:16px; color:black;">We don\'t know whether time spent on coaching and related activities come at the expense of work-time or not.</p>',
    unsafe_allow_html=True
)
proportion_time_during_work = st.slider(
    'Proportion of Coaching Time During Work Hours (%)',
    min_value=0.0,
    max_value=100.0,
    value=50.0,  # Default value set to 50%
    step=1.0
) / 100

# ==========================================================
#            CALCULATIONS BASED ON USER INPUTS
# ==========================================================

# Assume an average number of sessions per founder
average_sessions_per_founder = 12  # You can adjust this value as needed

# Cost per session
cost_per_session = total_coaching_cost / (total_founders * average_sessions_per_founder)
cost_per_founder = cost_per_session * average_sessions_per_founder

# Overall retention rate (since every retained founder gets the improvement)
overall_retention_rate = retention_rate

# Cost per retained founder
cost_per_retained_founder = cost_per_founder / overall_retention_rate if overall_retention_rate != 0 else np.nan

# Total number of retained founders
total_retained_founders = total_founders * overall_retention_rate

# Weeks Effects Last
weeks_effects_last = (months_effects_last / 12) * working_weeks_per_year

# Total Working Hours of Increased Productivity per Retained Founder
total_working_hours_increased_productivity = working_hours_per_week * weeks_effects_last

# Expected Value per Retained Founder
expected_value_per_retained_founder = (
    cost_per_founder_hour *
    total_working_hours_increased_productivity *
    (percentage_increase_in_productivity / 100)
)

# Total expected value gained
total_expected_value_gained = expected_value_per_retained_founder * total_retained_founders

# Number of productive hours bought
number_of_productive_hours_bought = (
    total_working_hours_increased_productivity *
    (percentage_increase_in_productivity / 100) *
    total_retained_founders
)

# Total founder hours spent (adjusted for drop-outs and proportion during work hours)
# Retained founders
founder_hours_retained = (
    retention_rate *
    total_founders *
    (average_sessions_per_founder * homework_hours_per_session * proportion_time_during_work)
)

# Drop-outs (attend 2 sessions)
founder_hours_dropouts = (
    (1 - retention_rate) *
    total_founders *
    (2 * homework_hours_per_session * proportion_time_during_work)
)

total_founder_hours = founder_hours_retained + founder_hours_dropouts

# Total cost of founder opportunity
total_founder_opportunity_cost = total_founder_hours * cost_per_founder_hour

# Total cost (time + money)
total_cost = total_coaching_cost + total_founder_opportunity_cost

# Net expected value
net_expected_value = (
    total_expected_value_gained -
    total_cost
)

# Cost per productive hour bought
if number_of_productive_hours_bought != 0:
    cost_per_productive_hour_bought = total_cost / number_of_productive_hours_bought
else:
    cost_per_productive_hour_bought = np.nan

# Return on investment
return_on_investment = net_expected_value / total_cost if total_cost != 0 else np.nan

# ==========================================================
#                DISPLAY RESULTS AND VISUALIZATIONS
# ==========================================================

# Place Key Metrics in the Sidebar
st.sidebar.header('Key Financial Metrics')
st.sidebar.metric('Return on Investment', f"{return_on_investment:.2f}" + "x")
st.sidebar.metric('Number of Productive Hours Bought', f"{number_of_productive_hours_bought:.0f} hours")
st.sidebar.metric('Cost per Productive Hour Bought', f"${cost_per_productive_hour_bought:.2f} per hour")
st.sidebar.metric('Net Expected Value', f"${net_expected_value:,.0f}")

# Main content continues
st.header('Financial Analysis Results')

st.subheader('Additional Metrics')

st.write(f"**Cost per Session:** ${cost_per_session:.2f}")
st.write(f"**Average Sessions per Founder:** {average_sessions_per_founder:.2f}")
st.write(f"**Cost per Founder:** ${cost_per_founder:.2f}")
st.write(f"**Cost per Retained Founder:** ${cost_per_retained_founder:.2f}")
st.write(f"**Total Number of Retained Founders:** {total_retained_founders:.2f}")
st.write(f"**Expected Value per Retained Founder:** ${expected_value_per_retained_founder:,.2f}")
st.write(f"**Total Cost (Time + Money):** ${total_cost:,.2f}")

# Add a new section at the bottom for removed metrics
st.markdown("---")
st.subheader('Detailed Cost Metrics')

st.write(f"**Total Coaching Cost:** ${total_coaching_cost:,.2f}")
st.write(f"**Total Founder Opportunity Cost:** ${total_founder_opportunity_cost:,.2f}")