# Save this script as app.py

import streamlit as st
from config import offerings

# Import tab display functions
from tabs.model_params_tab import display_model_parameters_tab
from tabs.assumptions_tab import display_assumptions_tab
from tabs.overall_tab import display_overall_comparison_tab
from tabs.programme_tab import display_programme_tab
from tabs.advanced_cost_settings_tab import display_advanced_cost_settings_tab # New import

# Set the page layout to wide
st.set_page_config(layout="wide")

st.title('CEA: Coaching EAs')

# ==========================================================
#                 INSTRUCTIONS
# ==========================================================

st.markdown("""
**Instructions:**
- Use the tabs below to switch between different programme offerings.
- Adjust the sliders to see how cost per productive hour bought changes.
- All calculations are focused on the cost to buy one productive hour for an EA participant.
""")

# ==========================================================
#                 DEFAULT VALUES FOR EACH TAB
# ==========================================================

# Define default model parameters (these will be overridden by the new tab's inputs)
# but are needed for the app to load initially before tab interactions.
# Keeping them here also serves as a reference for their original default values.

# ==========================================================
#                 TABS FOR EACH OFFERING
# ==========================================================

# Define tab names and create tabs
programme_tab_names = list(offerings.keys())
# New tabs will be inserted before "Overall"
tab_names = programme_tab_names + ["Model Parameters", "Advanced Cost Settings", "Assumptions", "Overall"] # Added new tab

all_tabs = st.tabs(tab_names)

# Assign tabs to meaningful variables
programme_st_tabs = all_tabs[:len(programme_tab_names)]
model_params_tab_ui = all_tabs[len(programme_tab_names)] 
advanced_cost_settings_tab_ui = all_tabs[len(programme_tab_names) + 1] # New tab UI
assumptions_tab_ui = all_tabs[len(programme_tab_names) + 2] # Adjusted index
overall_tab_ui = all_tabs[-1] # Remains last

offering_results = {}

# --- Render Model Parameters Tab ---
with model_params_tab_ui:
    (
        cost_per_session_input,
        working_weeks_input,
        prop_time_work_input,
        homework_hrs_input,
        avg_sessions_dropouts_input,
        session_duration_input
    ) = display_model_parameters_tab()

# --- Render Advanced Cost Settings Tab ---
with advanced_cost_settings_tab_ui:
    (
        disappointment_hours_input,
        baseline_org_yearly_clients_input
    ) = display_advanced_cost_settings_tab()

# --- Render Programme Tabs ---
for i, tab_name in enumerate(programme_tab_names):
    with programme_st_tabs[i]:
        tab_defaults = offerings[tab_name]
        offering_results[tab_name] = display_programme_tab(
            tab_name, 
            tab_defaults, 
            cost_per_session_input,
            working_weeks_input,
            prop_time_work_global=prop_time_work_input,
            homework_hrs_global=homework_hrs_input,
            avg_sessions_dropouts_global=avg_sessions_dropouts_input,
            session_duration_global=session_duration_input,
            disappointment_hours_config=disappointment_hours_input,
            baseline_org_yearly_clients_config=baseline_org_yearly_clients_input
        )

# --- Render Assumptions Tab ---
with assumptions_tab_ui:
    display_assumptions_tab()

# --- Render Overall Comparison Tab ---
with overall_tab_ui:
    display_overall_comparison_tab(offering_results)

# All function definitions previously here should have been removed by this edit.