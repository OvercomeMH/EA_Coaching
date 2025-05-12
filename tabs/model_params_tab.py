import streamlit as st
# Import DEFAULT values from the main config file
from config import (
    DEFAULT_COST_PER_SESSION, 
    DEFAULT_WORKING_WEEKS_PER_YEAR, 
    DEFAULT_PROPORTION_TIME_DURING_WORK,
    DEFAULT_HOMEWORK_HOURS_PER_SESSION,
    DEFAULT_AVG_SESSIONS_FOR_DROPOUTS,
    DEFAULT_SESSION_DURATION
)

def display_model_parameters_tab():
    st.header("Model Parameters")
    st.markdown("Adjust the global parameters that affect all programme calculations.")
    
    cost_per_session = st.number_input(
        "Cost per Coaching Session ($)", 
        min_value=0.0, 
        value=DEFAULT_COST_PER_SESSION, 
        step=0.50,
        help="The direct financial cost for one coaching session."
    )
    working_weeks_per_year = st.number_input(
        "Working Weeks Per Year", 
        min_value=1, 
        max_value=52, 
        value=DEFAULT_WORKING_WEEKS_PER_YEAR, 
        step=1,
        help="Assumed number of weeks a participant works in a year."
    )
    proportion_time_during_work = st.slider(
        "Proportion of Coaching/Homework Time During Work Hours (%)", 
        0.0, 
        100.0, 
        DEFAULT_PROPORTION_TIME_DURING_WORK * 100, 
        0.1,
        help="What percentage of time spent on coaching sessions and related homework is assumed to occur during typical work hours?"
    ) / 100.0
    homework_hours_per_session = st.number_input(
        "Homework Hours Per Session", 
        min_value=0.0, 
        value=DEFAULT_HOMEWORK_HOURS_PER_SESSION, 
        step=0.1,
        help="Assumed hours of homework or preparation per coaching session."
    )
    avg_sessions_for_dropouts = st.number_input(
        "Average Sessions Completed by Dropouts", 
        min_value=0.0, 
        value=DEFAULT_AVG_SESSIONS_FOR_DROPOUTS, 
        step=0.1,
        help="On average, how many sessions does a participant who drops out complete? This affects their time cost."
    )
    session_duration = st.number_input(
        "Duration of a Single Coaching Session (hours)",
        min_value=0.1, 
        value=DEFAULT_SESSION_DURATION,
        step=0.1,
        help="How long is one coaching session in hours?"
    )
    return (
        cost_per_session,
        working_weeks_per_year,
        proportion_time_during_work,
        homework_hours_per_session,
        avg_sessions_for_dropouts,
        session_duration
    ) 