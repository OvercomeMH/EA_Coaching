import streamlit as st
import numpy as np
# pandas and altair are not directly used by display_programme_tab itself,
# but by display_decay_visualisation which it calls from utils.py.
# So, they are not strictly needed here if display_decay_visualisation handles its own chart objects.

# Import helper functions from utils.py
from utils import display_decay_visualisation, calculate_total_gain_per_ea
# No direct config import needed here as `offerings` (tab_defaults) is passed in.
from config import DEFAULT_TIMEFRAME_OF_INTEREST_MONTHS
from config import programme_introductions, programme_productivity_gain_explanations

def display_programme_tab(
    tab_name, 
    tab_defaults, 
    cost_per_session_global,
    working_weeks_global,
    prop_time_work_global,
    homework_hrs_global,
    avg_sessions_dropouts_global,
    session_duration_global,
    # New advanced cost parameters (simplified)
    disappointment_hours_config,
    baseline_org_yearly_clients_config # Retained for context if needed, but not used for cost calculation here
):
    st.header(f"{tab_name} Programme")
    # Use config-based introduction text
    intro_text = programme_introductions.get(tab_name, "")
    if intro_text:
        st.markdown(intro_text)
    
    st.subheader("Benefit Duration and Decay")
    decay_model_options = ["Exponential Decay", "Linear Decay", "Custom Curve"]
    default_decay_model = tab_defaults.get("default_decay_model", "Exponential Decay")

    # Evidence base text (optional, keep if you want to show it)
    if tab_name == "Bespoke Offering":
        st.markdown("""
        **Evidence Base:** The UK's Improving Access to Psychological Therapies (IAPT) program provides 
        the closest studied model to our general programme. Like IAPT, we use low-intensity, CBT-focused 
        interventions, though we use psychology graduates rather than the nurses or social workers often 
        used in IAPT services.
        
        [Research on IAPT outcomes](https://pmc.ncbi.nlm.nih.gov/articles/PMC9790710/) shows significant 
        decay in benefits over time, with approximately 50% annual decay in effects being a reasonable estimate.
        """)
    elif tab_name == "Insomnia":
        st.markdown("""
        **Evidence Base:** Meta-analysis of cognitive behavioral therapy for insomnia 
        ([van der Zweerde et al., 2019](https://pubmed.ncbi.nlm.nih.gov/31491656/)) shows that 
        effects decline over time. While CBT-I produces clinically significant effects that last up to a year 
        after therapy, the evidence suggests approximately 60% annual decay in effects.
        """)
    elif tab_name == "Procrastination":
        st.markdown("""
        **Evidence Base:** Very little research exists on the long-term durability of procrastination interventions. 
        We suspect that it will decay sharply without additional intervention, which is why we provide a free GoalsWon referral to help prevent relapse.
        """)
    
    decay_model = st.selectbox(
        "Benefit Decay Model", 
        options=decay_model_options, 
        index=decay_model_options.index(default_decay_model),
        key=f"decay_model_{tab_name}",
        help="'Exponential Decay': Benefits reduce by a fixed percentage each period. 'Linear Decay': Benefits reduce by a fixed amount each period until zero. 'Custom Curve': Define your own decay curve by adjusting control points.'"
    )

    timeframe_of_interest_months = DEFAULT_TIMEFRAME_OF_INTEREST_MONTHS
    timeframe_of_interest_weeks = (timeframe_of_interest_months / 12) * working_weeks_global

    annual_decay_rate_input = None
    months_to_zero_input = None
    custom_month_sliders = {}

    if decay_model == "Exponential Decay":
        default_decay_rate = tab_defaults.get("default_decay_rate", 25.0)
        annual_decay_rate_input = st.slider(
            'Annual Decay Rate (%)', 0.1, 99.9, default_decay_rate, 0.1, key=f"annual_decay_{tab_name}",
            help="The percentage by which the remaining benefit decreases each year. Cannot be 0% or 100%."
        ) / 100.0
        if tab_name == "Insomnia": st.caption("Based on meta-analysis of CBT-I studies (van der Zweerde et al., 2019).")
        elif tab_name == "Bespoke Offering": st.caption("Based on IAPT outcome data for similar CBT-based interventions.")
        else: st.caption("Happier Lives Institute and Founders Pledge cite a decay of ~25% each year for group therapy for depression.")
    elif decay_model == "Linear Decay":
        default_months_to_zero = tab_defaults.get("default_months_to_zero", 12.0)
        months_to_zero_input = st.slider(
            'Months until Effect is Zero', 1.0, 60.0, default_months_to_zero, 0.1, key=f"months_to_zero_{tab_name}",
            help="How many months until the linearly decaying effect reaches zero."
        )
        if tab_name == "Procrastination": st.caption("Conservative estimate based on clinical experience, as limited research exists.")
    elif decay_model == "Custom Curve":
        st.markdown("**Define your custom decay curve by adjusting the benefit value at each control point:**")
        col1, col2 = st.columns(2)
        with col1:
            custom_month_sliders['month_3'] = st.slider('Benefit at 3 months (%)', 0.0, 100.0, 75.0, 1.0, key=f"custom_3month_{tab_name}") / 100.0
            custom_month_sliders['month_9'] = st.slider('Benefit at 9 months (%)', 0.0, 100.0, 30.0, 1.0, key=f"custom_9month_{tab_name}") / 100.0
        with col2:
            custom_month_sliders['month_6'] = st.slider('Benefit at 6 months (%)', 0.0, 100.0, 50.0, 1.0, key=f"custom_6month_{tab_name}") / 100.0
            custom_month_sliders['month_12'] = st.slider('Benefit at 12 months (%)', 0.0, 100.0, 15.0, 1.0, key=f"custom_12month_{tab_name}") / 100.0
    
    weekly_points_for_calc = display_decay_visualisation(
        decay_model,
        annual_decay_rate_input=annual_decay_rate_input,
        months_to_zero_input=months_to_zero_input,
        month_3_slider=custom_month_sliders.get('month_3'),
        month_6_slider=custom_month_sliders.get('month_6'),
        month_9_slider=custom_month_sliders.get('month_9'),
        month_12_slider=custom_month_sliders.get('month_12'),
        timeframe_of_interest_weeks_calc=timeframe_of_interest_weeks
    )

    st.subheader("Intervention Impact & Participants")
    # Add explanatory sentence about dropouts
    st.markdown("We assume that anyone who who dropped out without telling us they were better got zero benefit. So, we only need to consider people who've completed the programme.")
    pre_hours = st.slider(
        'How many hours do you think our median completer would spend on EA activities before the intervention?',
        min_value=0, max_value=80, value=30 if tab_name == "Procrastination" else tab_defaults["pre_intervention_hours"], step=1, key=f"pre_hours_{tab_name}"
    )
    post_hours = st.slider(
        'How many hours do you expect them to work after?',
        min_value=0, max_value=80, value=39 if tab_name == "Procrastination" else tab_defaults["post_intervention_hours"], step=1, key=f"post_hours_{tab_name}"
    )
    if tab_name == "Bespoke Offering":
        pass
    else:
        st.caption('For calibration: In our data, a typical improvement is 3–6 hours/week for those with significant barriers, and 1–2 hours/week for those with mild issues.')
    
    # Productivity multiplier slider: always use config value
    productivity_multiplier = st.slider(
        'How much more productive is each working hour after the intervention? (e.g. 1.10 = 10% more productive)',
        min_value=0.0, max_value=2.0, value=1.01 if tab_name == "Procrastination" else tab_defaults["productivity_multiplier"], step=0.01, key=f"productivity_multiplier_{tab_name}",
        help="Multiplier for productivity per hour post-intervention. >1 means more productive, <1 means less productive, 1 means no change."
    )
    
    implied_productivity_gain = ((post_hours * productivity_multiplier) - pre_hours) / pre_hours * 100 if pre_hours > 0 else 0
    # Make the implied productivity gain text larger
    st.markdown(f"<span style='font-size:1.5em'><b>Implied Productivity Gain: {implied_productivity_gain:.1f}%</b></span>", unsafe_allow_html=True)
    
    # Add section to help user interpret the implied productivity gain (now config-based)
    st.markdown("### How do I know if the implied productivity gain makes sense?")
    productivity_explanation = programme_productivity_gain_explanations.get(tab_name, "The productivity gain estimate is based on the best available evidence and expert judgment for this type of intervention.")
    st.markdown(productivity_explanation)
    
    retention_rate = st.slider(
        'Retention Rate (%)', 0.0, 100.0, value=tab_defaults["retention"], step=0.1, key=f"retention_rate_{tab_name}"
    ) / 100
    # Add explanation and 65% statistic next to retention rate for Bespoke Offering
    if tab_name == "Bespoke Offering":
        st.caption("On average, 65% of EAs who do one session will go on to do at least six sessions. Retention rate here means the probability that a participant will complete every session in the programme, given that they attended the first session.")
    elif tab_name in ["Insomnia", "Procrastination"]:
        st.caption("Our average EA completion rate is ~60%. Both RCTs retrained >80% of users. We're estimating 70%.")
    else:
        st.caption("Our average EA completion rate is ~60%. Both RCTs retrained >80% of users. We're estimating for 75%, adjusted upwards because we think the RCT would have retained more users if they had known the results for those who completed, and we'll be advertising those results hard.")
    num_participants = st.slider(
        'Participants', min_value=10, max_value=1000, value=tab_defaults["num_participants"], step=1, key=f"num_participants_{tab_name}"
    )
    sessions_per_participant = tab_defaults["sessions_per_participant"]
    
    total_EAs = num_participants
    overall_retention_rate = retention_rate
    total_retained_EAs = total_EAs * overall_retention_rate
    
    initial_weekly_gain_per_ea_abs = ( (post_hours * productivity_multiplier) - pre_hours )
    if pre_hours == 0: 
        initial_weekly_gain_per_ea_abs = (post_hours * productivity_multiplier)

    # This calculates GROSS hours gained per EA over the period, before accounting for time spent on intervention
    gross_gain_over_period_per_ea_who_completes = calculate_total_gain_per_ea(
        initial_weekly_gain_per_ea_abs=initial_weekly_gain_per_ea_abs,
        decay_model=decay_model,
        timeframe_of_interest_weeks=timeframe_of_interest_weeks,
        working_weeks_per_year=working_weeks_global,
        annual_decay_rate=annual_decay_rate_input,
        months_to_zero=months_to_zero_input,
        custom_weekly_points=weekly_points_for_calc
    )

    # Total gross hours from all EAs who are retained
    gross_productive_hours_gain_from_retained = gross_gain_over_period_per_ea_who_completes * total_retained_EAs
    
    time_spent_retained_during_work = (
        total_retained_EAs *
        sessions_per_participant *
        (session_duration_global + homework_hrs_global) *
        prop_time_work_global
    )
    time_spent_dropouts_during_work = (
        (total_EAs - total_retained_EAs) *
        avg_sessions_dropouts_global *
        (session_duration_global + homework_hrs_global) *
        prop_time_work_global
    )

    SIGN_UP_HOURS_PER_PARTICIPANT = 0.5 # Assuming this is a constant
    time_spent_on_sign_up_during_work = (
        total_EAs * 
        SIGN_UP_HOURS_PER_PARTICIPANT * 
        prop_time_work_global
    )

    num_dropouts = total_EAs - total_retained_EAs
    total_dropout_productivity_loss = num_dropouts * disappointment_hours_config

    number_of_productive_hours_bought = (
        gross_productive_hours_gain_from_retained - 
        time_spent_retained_during_work - 
        time_spent_dropouts_during_work - 
        time_spent_on_sign_up_during_work - 
        total_dropout_productivity_loss
    )
    
    # Calculate base cost from sessions (This is now the total direct cost for this programme)
    base_sessions_cost = sessions_per_participant * cost_per_session_global * total_EAs
    total_cost = base_sessions_cost # Total cost is now only the direct sessions cost

    cost_per_productive_hour_bought = total_cost / number_of_productive_hours_bought if number_of_productive_hours_bought != 0 else np.nan

    # Calculate metrics for display
    net_hours_gained_per_retained_client = (number_of_productive_hours_bought / total_retained_EAs) if total_retained_EAs > 0 else 0
    cost_per_retained_client = (total_cost / total_retained_EAs) if total_retained_EAs > 0 else np.nan

    st.subheader("Programme Outcomes")
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    with row1_col1:
        st.metric(
            label="Total Direct Cost",
            value=f"${total_cost:,.0f}"
        )
    with row1_col2:
        st.metric(
            label="Net Prod. Hours Bought (All)",
            value=f"{number_of_productive_hours_bought:,.0f}"
        )
    with row1_col3:
        cost_display_overall = f"${cost_per_productive_hour_bought:,.2f}" if not np.isnan(cost_per_productive_hour_bought) else "N/A"
        st.metric(
            label="Cost / Prod. Hour (Overall)",
            value=cost_display_overall
        )
    
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1:
        st.metric(
            label="Clients Retained",
            value=f"{total_retained_EAs:,.0f}"
        )
    with row2_col2:
        cost_per_retained_display = f"${cost_per_retained_client:,.0f}" if not np.isnan(cost_per_retained_client) else "N/A"
        st.metric(
            label="Direct Cost / Retained Client",
            value=cost_per_retained_display
        )
    with row2_col3:
        st.metric(
            label="Net Prod. Hrs / Ret. Client",
            value=f"{net_hours_gained_per_retained_client:,.1f}"
        )

    return {
        "Total Cost (Money Spent)": total_cost, # This is the direct cost
        "Number of Productive Hours Bought": number_of_productive_hours_bought,
        "Cost per Productive Hour Bought": cost_per_productive_hour_bought,
        "Total Clients Seen": total_EAs,
        "Clients Retained": total_retained_EAs,
        "Net Hours Gained per Retained Client": net_hours_gained_per_retained_client,
        "Baseline Org Yearly Clients Config": baseline_org_yearly_clients_config # Pass this through for Overall tab context
    } 