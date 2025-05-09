# Save this script as app.py

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Set the page layout to wide
st.set_page_config(layout="wide")

st.title('Cost-Effectiveness Analysis for EA Coaching Programme')

# ==========================================================
#                 INSTRUCTIONS
# ==========================================================

st.markdown("""

**Context**
We're Overcome, an EA-aligned mental health charity. You can see our pitch deck [here](https://www.canva.com/design/DAGSR0iTSfU/SAkv2xJb1BglQNkad1HvdA/edit?utm_content=DAGSR0iTSfU&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton). 
We give EAs our best coaches. This is our best guess at this programme's cost-effectiveness.      

**Instructions:**

- Use the sliders in the **Adjustable Parameters** section to modify the variables.
- See that that affects the cost-effectiveness estimate by looking at the side and bottom sections.
            
""")

# ==========================================================
#                 USER INPUT SECTION WITH SLIDERS
# ==========================================================

st.header('Adjustable Parameters')

# 1. Program Costs
st.subheader('Per Participant Cost')
st.markdown(
    '<p style="font-size:16px; color:black;">Includes all associated costs per participant. The default value, $20, is what it currently costs us per participant.</p>',
    unsafe_allow_html=True
)
per_EA_cost = st.slider(
    'Per Participant Cost ($)',
    min_value=10, 
    max_value=60,
    value=20,     
    step=2
)

# 2. Number of Participating EAs
st.subheader('Number of Participating EAs')

total_EAs = st.slider(
    'Total Number of EAs served.',
    min_value=10,
    max_value=500,
    value=172,
    step=1
)

# 3. Retention Metrics
st.subheader('Retention')
st.markdown(
    '<p style="font-size:16px; color:black;">Retention = proportion of EAs to complete the programme. We currently retain <90% of EAs (n>30). Our general offerings to EAs retain ~70% (n= ~200).</p>',
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
    value=6.0,
    step=0.1
)

st.markdown(
    '<p style="font-size:16px; color:black;">This is the most important variable but we are deeply uncertain and no hard evidence exists. Here are some relevant facts drawn from the general population: On average, procrastination reduces productivity by ~25%. On average, our coaching clients gain two points of life satisfaction (measured on a scale of 0-10) over the first six weeks. Academic sources suggest each point of life satisfaction point gained results in ~12 percent greater productivity.</p>',
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
    '<p style="font-size:16px; color:black;">Charity entrepreneurship (2018) estimate the expected value per EA is $217k per annum. The minimum legal wage (UK) is $30k. The median EAs annual EV likely falls between these two extremes   </p>',
    unsafe_allow_html=True
)
ev_per_EA_per_year = st.slider(
    'Expected Value per EA per Year ($)',
    min_value=0,
    max_value=2000000,
    value=50000,
    step=50
)

# 6. EA Working Hours
st.subheader('EA Working Hours')

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

# Calculating Cost per EA Hour
total_working_hours_per_year = working_hours_per_week * working_weeks_per_year
cost_per_EA_hour = ev_per_EA_per_year / total_working_hours_per_year

# 7. EA Opportunity Cost
st.subheader('EA Opportunity Cost')

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

# Assume an average number of sessions per EA
average_sessions_per_EA = 4  # Default is now 4 sessions

# Cost per session
cost_per_session = per_EA_cost / average_sessions_per_EA
cost_per_EA = per_EA_cost

# Overall retention rate (since every retained EA gets the improvement)
overall_retention_rate = retention_rate

# Cost per retained EA
cost_per_retained_EA = cost_per_EA / overall_retention_rate if overall_retention_rate != 0 else np.nan

# Total number of retained EAs
total_retained_EAs = total_EAs * overall_retention_rate

# Weeks Effects Last
weeks_effects_last = (months_effects_last / 12) * working_weeks_per_year

# Total Working Hours of Increased Productivity per Retained EA
total_working_hours_increased_productivity = working_hours_per_week * weeks_effects_last

# Expected Value per Retained EA
expected_value_per_retained_EA = (
    cost_per_EA_hour *
    total_working_hours_increased_productivity *
    (percentage_increase_in_productivity / 100)
)

# Total expected value gained
total_expected_value_gained = expected_value_per_retained_EA * total_retained_EAs

# Number of productive hours bought
number_of_productive_hours_bought = (
    total_working_hours_increased_productivity *
    (percentage_increase_in_productivity / 100) *
    total_retained_EAs
)

# Total EA hours spent (adjusted for drop-outs and proportion during work hours)
# Retained EAs
EA_hours_retained = (
    retention_rate *
    total_EAs *
    (average_sessions_per_EA * homework_hours_per_session * proportion_time_during_work)
)

# Drop-outs (attend 2 sessions)
EA_hours_dropouts = (
    (1 - retention_rate) *
    total_EAs *
    (2 * homework_hours_per_session * proportion_time_during_work)
)

total_EA_hours = EA_hours_retained + EA_hours_dropouts

# Total cost of EA opportunity
total_EA_opportunity_cost = total_EA_hours * cost_per_EA_hour

# Total cost (time + money)
total_cost = per_EA_cost * total_EAs + total_EA_opportunity_cost

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
st.write(f"**Average Sessions per EA:** {average_sessions_per_EA:.2f}")
st.write(f"**Cost per EA:** ${cost_per_EA:.2f}")
st.write(f"**Cost per Retained EA:** ${cost_per_retained_EA:.2f}")
st.write(f"**Total Number of Retained EAs:** {total_retained_EAs:.2f}")
st.write(f"**Expected Value per Retained EA:** ${expected_value_per_retained_EA:,.2f}")
st.write(f"**Total Cost (Time + Money):** ${total_cost:,.2f}")

# Add a new section at the bottom for removed metrics
st.markdown("---")
st.subheader('Detailed Cost Metrics')

st.write(f"**Total Per Participant Cost:** ${per_EA_cost:,.2f}")
st.write(f"**Total EA Opportunity Cost:** ${total_EA_opportunity_cost:,.2f}")