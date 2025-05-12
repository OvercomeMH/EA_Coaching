import streamlit as st
import pandas as pd
import numpy as np # For np.nan
from config import ORGANIZATION_RD_BUDGET_USD # Import the R&D budget

def display_overall_comparison_tab(results_data):
    st.header("Programme Comparison: Key Metrics")
    
    if not results_data or not all(isinstance(res, dict) for res in results_data.values()) or \
       not all('Cost per Productive Hour Bought' in res for res in results_data.values()):
        st.info('Adjust parameters in the other tabs to see a comparison here.')
        return

    df = pd.DataFrame.from_dict(results_data, orient='index')

    # Rename columns for clarity in the table
    column_renames = {
        'Total Cost (Money Spent)': 'Direct Programme Cost',
        'Number of Productive Hours Bought': 'Net Prod. Hours Bought',
        'Cost per Productive Hour Bought': 'Cost / Prod. Hr',
        'Total Clients Seen': 'Clients Seen',
        'Clients Retained': 'Clients Retained',
        'Net Hours Gained per Retained Client': 'Net Hrs Gained / Ret. Client'
    }
    df = df.rename(columns=column_renames)

    FTE_HOURS_PER_YEAR = 2080 
    if 'Net Prod. Hours Bought' in df.columns and 'Direct Programme Cost' in df.columns:
        # Ensure 'Net Prod. Hours Bought' is not zero for division
        df['Cost per FTE'] = np.where(
            df['Net Prod. Hours Bought'] != 0,
            df['Direct Programme Cost'] / (df['Net Prod. Hours Bought'] / FTE_HOURS_PER_YEAR),
            np.nan
        )
    else:
        df['Cost per FTE'] = np.nan

    # Desired column order for display
    desired_columns_order = [
        'Direct Programme Cost',
        'Net Prod. Hours Bought',
        'Clients Seen',
        'Clients Retained',
        'Net Hrs Gained / Ret. Client',
        'Cost / Prod. Hr',
        'Cost per FTE'
    ]
    existing_columns_in_order = [col for col in desired_columns_order if col in df.columns]
    df_display = df[existing_columns_in_order]

    ordered_programmes = ['Bespoke Offering', 'Procrastination', 'Insomnia']
    ordered_programmes_in_results = [p for p in ordered_programmes if p in df_display.index]
    df_display = df_display.reindex(ordered_programmes_in_results)

    # Calculate Summary Row (only for display columns)
    if not df_display.empty:
        summary_data = {}
        if 'Direct Programme Cost' in df_display.columns: 
            summary_data['Direct Programme Cost'] = df_display['Direct Programme Cost'].sum()
        if 'Net Prod. Hours Bought' in df_display.columns: 
            summary_data['Net Prod. Hours Bought'] = df_display['Net Prod. Hours Bought'].sum()
        if 'Clients Seen' in df_display.columns: 
            summary_data['Clients Seen'] = df_display['Clients Seen'].sum()
        if 'Clients Retained' in df_display.columns: 
            summary_data['Clients Retained'] = df_display['Clients Retained'].sum()
        
        # For averages/derived metrics in summary:
        total_direct_cost_sum = summary_data.get('Direct Programme Cost', 0)
        total_net_hours_sum = summary_data.get('Net Prod. Hours Bought', 0)
        total_clients_retained_sum = summary_data.get('Clients Retained', 0)

        summary_data['Net Hrs Gained / Ret. Client'] = (total_net_hours_sum / total_clients_retained_sum) if total_clients_retained_sum > 0 else np.nan
        summary_data['Cost / Prod. Hr'] = (total_direct_cost_sum / total_net_hours_sum) if total_net_hours_sum > 0 else np.nan
        summary_data['Cost per FTE'] = (total_direct_cost_sum / (total_net_hours_sum / FTE_HOURS_PER_YEAR)) if total_net_hours_sum > 0 else np.nan
        
        summary_df_cols = {k: [v] for k, v in summary_data.items() if k in df_display.columns}
        summary_row = pd.DataFrame(summary_df_cols, index=["Total/Overall Average"])
        df_display = pd.concat([df_display, summary_row])

    # Formatting dictionary
    formats = {
        'Direct Programme Cost': '${:,.0f}',
        'Net Prod. Hours Bought': '{:,.0f}',
        'Clients Seen': '{:,.0f}',
        'Clients Retained': '{:,.0f}',
        'Net Hrs Gained / Ret. Client': '{:,.1f}',
        'Cost / Prod. Hr': '${:,.2f}',
        'Cost per FTE': '${:,.0f}'
    }
    valid_formats = {k: v for k, v in formats.items() if k in df_display.columns}
    st.dataframe(df_display.style.format(valid_formats, na_rep="N/A"), height=(df_display.shape[0] + 1) * 35 + 3)
    
    st.markdown('---') # Separator
    st.subheader("Understanding the Costs")
    st.markdown("""
    **Direct Programme Cost:** This is the direct cost associated with running each specific EA coaching programme, primarily driven by the number of sessions and participants.
    
    **Net Productive Hours Bought:** This represents the total additional productive hours gained from participants who completed the programme, after accounting for:
    - Time spent by participants in sessions and on homework during work hours.
    - Time spent by participants on sign-up during work hours.
    - Estimated productivity loss due to participants dropping out (disappointment/delay costs).
    
    **Cost per Productive Hour & Cost per FTE:** These metrics show the direct cost-effectiveness of the programmes in terms of buying productive time.
    """)

    st.subheader("Context: Organizational Research & Development (R&D) Budget")
    # Calculate total EA clients from the results_data for the explanation
    total_ea_clients_all_programmes = 0
    baseline_clients_from_one_prog = 0 # We only need one instance of this from any program's data
    if results_data:
        for prog_name, data_dict in results_data.items():
            if isinstance(data_dict, dict):
                total_ea_clients_all_programmes += data_dict.get('Total Clients Seen', 0)
                if baseline_clients_from_one_prog == 0 and 'Baseline Org Yearly Clients Config' in data_dict:
                     baseline_clients_from_one_prog = data_dict.get('Baseline Org Yearly Clients Config',0)

    total_org_clients_for_rd_share = baseline_clients_from_one_prog + total_ea_clients_all_programmes
    rd_share_percentage = 0
    if total_org_clients_for_rd_share > 0:
        rd_share_percentage = (total_ea_clients_all_programmes / total_org_clients_for_rd_share) * 100
    
    conceptual_rd_cost_for_ea_programmes = (rd_share_percentage / 100) * ORGANIZATION_RD_BUDGET_USD

    st.markdown(f"""
    Beyond the direct costs shown above, our organization maintains a fixed annual Research & Development (R&D) budget of **${ORGANIZATION_RD_BUDGET_USD:,.0f}**. 
    This budget supports ongoing improvements, research into new coaching methodologies, and development of materials that benefit all our clients, including EAs.
    
    The EA coaching programmes serve approximately **{total_ea_clients_all_programmes:,.0f}** participants (based on current settings). 
    When considering the organization's other baseline activities serving roughly **{baseline_clients_from_one_prog:,.0f}** clients, the EA programmes represent about **{rd_share_percentage:.1f}%** of the total client interactions.
    
    Conceptually, this means that **${conceptual_rd_cost_for_ea_programmes:,.0f}** of the R&D budget could be considered as supporting the EA coaching offerings. 
    This conceptual share is *not* included in the 'Direct Programme Cost' per hour metrics above, but it's an important context for understanding the full investment in delivering high-quality, evidence-based coaching to EAs.
    """) 