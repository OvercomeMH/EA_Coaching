import streamlit as st
from config import (
    DEFAULT_DISAPPOINTMENT_HOURS_PER_DROPOUT,
    DEFAULT_BASELINE_ORG_YEARLY_CLIENTS
)

def display_advanced_cost_settings_tab():
    st.header("Advanced Cost Settings")
    st.markdown("""
    These settings allow for more detailed configuration of costs,
    particularly those related to participant dropout and understanding the
    organization's baseline client load for contextual R&D cost allocation.
    """)

    disappointment_hours = st.number_input(
        "Disappointment Hours Lost Per Dropout",
        min_value=0.0,
        value=DEFAULT_DISAPPOINTMENT_HOURS_PER_DROPOUT,
        step=1.0,
        help="Estimated productive hours lost by a participant due to dropping out and delaying alternative help."
    )

    st.subheader("Organizational Context for R&D Explanation")
    st.markdown(""" 
    This parameter helps in understanding the scale of the organization's activities
    relative to the EA coaching program. This context is used in the 'Overall' tab
    to explain how the organization's fixed R&D budget might be conceptually
    apportioned.
    """)

    baseline_org_yearly_clients = st.number_input(
        "Organization's Baseline Yearly Clients (Excluding this EA Offering)",
        min_value=0.0, 
        value=DEFAULT_BASELINE_ORG_YEARLY_CLIENTS,
        step=10.0,
        help="Baseline number of clients the organization serves annually, EXCLUDING participants from this specific EA offering being modeled. Used to provide context for R&D budget explanations."
    )
    
    return (
        disappointment_hours,
        baseline_org_yearly_clients
    ) 