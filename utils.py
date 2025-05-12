import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from scipy.interpolate import PchipInterpolator

# --- Function to display Decay Visualisation --- (Phase 2)
def display_decay_visualisation(decay_model, annual_decay_rate_input, months_to_zero_input, month_3_slider, month_6_slider, month_9_slider, month_12_slider, timeframe_of_interest_weeks_calc):
    # Generate data for visualization
    months = np.arange(0, 13, 1)  # 0 to 12 months
    custom_curve_weekly_points = None

    if decay_model == "Exponential Decay":
        if annual_decay_rate_input is None: # Handle case where it might be None if not selected
            st.warning("Annual decay rate not set for Exponential Decay. Visualization may be incorrect.")
            return None # Or display a placeholder chart
        monthly_decay_rate = 1 - (1 - annual_decay_rate_input)**(1/12)
        decay_values = [1 * (1 - monthly_decay_rate)**month for month in months]
        
        decay_df = pd.DataFrame({
            'Month': months,
            'Relative Benefit': decay_values
        })
        
        decay_chart = alt.Chart(decay_df).mark_line(point=True).encode(
            x=alt.X('Month:Q', title='Month'),
            y=alt.Y('Relative Benefit:Q', title='Relative Benefit', scale=alt.Scale(domain=[0, 1])),
            tooltip=['Month', 'Relative Benefit']
        ).properties(
            title=f"Exponential Decay with {annual_decay_rate_input*100:.1f}% Annual Decay Rate",
            width=600,
            height=300
        )
        st.altair_chart(decay_chart, use_container_width=True)
        st.caption("This graph shows how the benefit decays exponentially over 12 months with the selected annual decay rate.")
        
    elif decay_model == "Linear Decay":
        if months_to_zero_input is None:
            st.warning("Months to zero not set for Linear Decay. Visualization may be incorrect.")
            return None
        months_to_plot = np.arange(0, max(13, months_to_zero_input + 1), 1)
        decay_values = [max(0, 1 - month/months_to_zero_input) for month in months_to_plot]
        
        decay_df = pd.DataFrame({
            'Month': months_to_plot,
            'Relative Benefit': decay_values
        })
        
        decay_chart = alt.Chart(decay_df).mark_line(point=True).encode(
            x=alt.X('Month:Q', title='Month'),
            y=alt.Y('Relative Benefit:Q', title='Relative Benefit', scale=alt.Scale(domain=[0, 1])),
            tooltip=['Month', 'Relative Benefit']
        ).properties(
            title=f"Linear Decay to Zero After {months_to_zero_input} Months",
            width=600,
            height=300
        )
        st.altair_chart(decay_chart, use_container_width=True)
        st.caption("This graph shows how the benefit decays linearly to zero over the specified number of months.")
        
    elif decay_model == "Custom Curve":
        # Ensure slider values are not None before using them
        if not all([month_3_slider is not None, month_6_slider is not None, month_9_slider is not None, month_12_slider is not None]):
            st.warning("Custom curve control points not fully defined. Visualization may be incorrect.")
            return None
            
        control_points_custom = {
            0: 1.0, 3: month_3_slider, 6: month_6_slider,
            9: month_9_slider, 12: month_12_slider
        }
        x_points = np.array(list(control_points_custom.keys()))
        y_points = np.array(list(control_points_custom.values()))
        
        interp_func = PchipInterpolator(x_points, y_points)
        months_fine = np.linspace(0, 12, 100)
        decay_values_fine = np.clip(interp_func(months_fine), 0, 1)
        
        custom_curve_weekly_points = []
        weeks_in_period_calc = int(timeframe_of_interest_weeks_calc)
        for w in range(weeks_in_period_calc):
            month_equiv = (w / weeks_in_period_calc) * 12
            benefit_at_week = float(interp_func(month_equiv))
            custom_curve_weekly_points.append(max(0, min(1, benefit_at_week)))

        custom_decay_df = pd.DataFrame({'Month': months_fine, 'Relative Benefit': decay_values_fine})
        control_df = pd.DataFrame({'Month': x_points, 'Relative Benefit': y_points})
        
        line_chart = alt.Chart(custom_decay_df).mark_line().encode(
            x=alt.X('Month:Q', title='Month'),
            y=alt.Y('Relative Benefit:Q', title='Relative Benefit', scale=alt.Scale(domain=[0, 1]))
        )
        point_chart = alt.Chart(control_df).mark_circle(size=100).encode(
            x='Month:Q', y='Relative Benefit:Q', tooltip=['Month', 'Relative Benefit']
        )
        combined_chart = (line_chart + point_chart).properties(
            title="Custom Decay Curve with Control Points", width=600, height=300
        )
        st.altair_chart(combined_chart, use_container_width=True)
        st.caption("This graph shows your custom decay curve. Adjust sliders to reshape.")

    return custom_curve_weekly_points

# --- Function to calculate total gain per EA --- 
def calculate_total_gain_per_ea(
    initial_weekly_gain_per_ea_abs,
    decay_model,
    timeframe_of_interest_weeks, 
    working_weeks_per_year, 
    annual_decay_rate=None, 
    months_to_zero=None,
    custom_weekly_points=None
):
    total_gain = 0.0

    if decay_model == "Exponential Decay":
        if annual_decay_rate is None:
            raise ValueError("Annual decay rate must be provided for Exponential Decay model.")

        if annual_decay_rate == 0.0 or annual_decay_rate == 1.0:
            raise ValueError("Annual decay rate cannot be 0% (0.0) or 100% (1.0) for Exponential Decay. Please choose a value strictly between 0 and 1.")

        if working_weeks_per_year > 0 and 0 < annual_decay_rate < 1:
            weekly_decay_factor = (1.0 - annual_decay_rate)**(1.0 / working_weeks_per_year)
            if abs(1.0 - weekly_decay_factor) < 1e-9: 
                 total_gain = initial_weekly_gain_per_ea_abs * timeframe_of_interest_weeks
            else:
                total_gain = initial_weekly_gain_per_ea_abs * \
                                            (1.0 - weekly_decay_factor**timeframe_of_interest_weeks) / \
                                            (1.0 - weekly_decay_factor)
        elif working_weeks_per_year <= 0:
            total_gain = 0.0
        else:
            total_gain = initial_weekly_gain_per_ea_abs * timeframe_of_interest_weeks

    elif decay_model == "Linear Decay":
        if months_to_zero is not None and working_weeks_per_year > 0 and months_to_zero > 0:
            weeks_to_zero_calc = (months_to_zero / 12) * working_weeks_per_year
            if weeks_to_zero_calc > 0: # Redundant check but safe
                effective_weeks = min(timeframe_of_interest_weeks, weeks_to_zero_calc)
                for w_idx in range(int(effective_weeks)):
                    weekly_benefit = initial_weekly_gain_per_ea_abs * max(0, (1 - w_idx / weeks_to_zero_calc))
                    total_gain += weekly_benefit
        else: 
             total_gain = 0 

    elif decay_model == "Custom Curve":
        if custom_weekly_points:
            for week_benefit_factor in custom_weekly_points:
                total_gain += initial_weekly_gain_per_ea_abs * week_benefit_factor
        else:
            total_gain = initial_weekly_gain_per_ea_abs * timeframe_of_interest_weeks * 0.5
    
    return total_gain 