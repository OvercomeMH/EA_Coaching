import streamlit as st

def display_assumptions_tab():
    st.header("Model Assumptions")
    st.markdown(""" 
    This model relies on several key assumptions that are not directly configurable as numerical inputs. 
    Understanding these is crucial for interpreting the results:

    - **Fixed Timeframe of Interest (12 months):** The model calculates benefits over a standard 12-month 
      period for all programmes. This timeframe is used to sum up the total productive hours gained, 
      applying the selected decay model and its parameters.

    - **Market Size & Sign-up Feasibility:** The model calculates outcomes based on the 'Number of Participants' 
      you set for each programme. It does not assess whether it's feasible to attract that many participants 
      at the specified retention rates.

    - **Decay Model Accuracy:** The different decay models (Exponential, Linear) are simplifications 
      of how benefits actually diminish over time. The default decay parameters for each programme are based 
      on the best available evidence or conservative estimates where evidence is limited.

    - **Accuracy of User Inputs:** The validity of the outputs heavily depends on the accuracy of your inputs for:
        - Pre- and post-intervention hours.
        - Productivity multiplier.
        - Expected effect duration.
        - Retention rates.
      These are often estimates and can significantly influence the cost-effectiveness figures.

    - **Zero Net Productivity Gain for Dropouts (for the gain calculation):** While the *time cost* of dropouts 
      (time spent in sessions/homework before dropping out) is now subtracted from the gross productivity gain, 
      it's assumed that dropouts do not contribute any *positive* productivity gains themselves. Any partial benefits 
      they might have received are not counted towards the 'Productive Hours Bought'.

    - **Homogeneity of Participants:** The model uses average or median values for participant characteristics 
      and outcomes. It does not capture the full distribution or range of individual experiences or benefits.

    - **Nature of "EA Activities":** The hours worked (pre and post intervention) are assumed to be dedicated to 
      "EA activities." The model assumes these hours have a uniform value/impact, and the productivity multiplier 
      applies equally across these hours.
    
    - **Cost Model for Financial Costs:** The total financial cost for each programme offering is calculated based on 
      the full number of `sessions_per_participant` for *all* initial `total_EAs` (participants at the start), 
      regardless of the retention rate. This means the cost reflects reserving a full slot for every participant 
      who enrolls. If costs are only incurred for attended sessions, the actual financial outlay might be lower.

    - **Additionality:** The model assumes that any productivity gains are purely additional and would not have 
      occurred without the intervention.

    - **No Follow-up Sessions:** The model assumes no additional coaching sessions are provided beyond the initially defined programme length.

    - **No Self-Funding Post-Programme:** It is assumed that 0% of participants will opt to self-fund additional sessions after completing the programme.

    - **No Change in Attitude to Coaching/Therapy:** The intervention is not assumed to change a participant's general attitude towards seeking coaching or therapy in the future, beyond the direct effects modelled.

    - **Single Programme per Participant:** The model assumes each individual will only participate in one of the listed programmes. There are no overlaps or combined effects from multiple programme participations by the same individual.
    """) 