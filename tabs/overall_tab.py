import streamlit as st
import pandas as pd
import numpy as np # For np.nan
from config import ORGANISATION_FIXED_COSTS # Import the R&D budget

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
    **Net Productive Hours Bought:** This represents the total additional productive hours gained from participants who completed the programme, after accounting for:
    - Time spent by participants in sessions and on homework during work hours.
    - Time spent by participants on sign-up during work hours.
    - Estimated productivity loss due to participants dropping out (disappointment/delay costs).
    
    **Cost per Productive Hour / FTE:** These metrics show the direct cost-effectiveness of the programmes. FTE: One full-time equivalent, for one year, assuming 40 hours a week with no holidays (2080 hours)
    """)

    st.subheader("Fixed Costs")
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
    conceptual_rd_cost_for_ea_programmes = (rd_share_percentage / 100) * ORGANISATION_FIXED_COSTS

    # New, much shorter explanation
    st.markdown(f"""
Our fixed costs are roughly **${ORGANISATION_FIXED_COSTS:,.0f}**. We'd also ask that you cover a fraction of that directly proportional to EA's share of our total clients. If you're up for that, here's an updated table.
""")

    # Add R&D share to direct programme cost for each programme
    if total_org_clients_for_rd_share > 0 and not df_display.empty:
        # Calculate R&D share for each programme
        rd_share_fraction = ORGANISATION_FIXED_COSTS / total_org_clients_for_rd_share
        df_with_rd = df_display.copy()
        # Only add R&D share to actual programmes, not the summary row
        for prog in ordered_programmes_in_results:
            if prog in df_with_rd.index:
                clients = df_with_rd.at[prog, 'Clients Seen'] if 'Clients Seen' in df_with_rd.columns else 0
                df_with_rd.at[prog, 'Direct Programme Cost'] = df_with_rd.at[prog, 'Direct Programme Cost'] + (clients * rd_share_fraction)
        # Update summary row
        if 'Total/Overall Average' in df_with_rd.index:
            total_clients = df_with_rd.at['Total/Overall Average', 'Clients Seen'] if 'Clients Seen' in df_with_rd.columns else 0
            df_with_rd.at['Total/Overall Average', 'Direct Programme Cost'] = df_with_rd.at['Total/Overall Average', 'Direct Programme Cost'] + (total_clients * rd_share_fraction)
        # Recalculate cost metrics
        if 'Net Prod. Hours Bought' in df_with_rd.columns and 'Direct Programme Cost' in df_with_rd.columns:
            df_with_rd['Cost / Prod. Hr'] = np.where(
                df_with_rd['Net Prod. Hours Bought'] != 0,
                df_with_rd['Direct Programme Cost'] / df_with_rd['Net Prod. Hours Bought'],
                np.nan
            )
            df_with_rd['Cost per FTE'] = np.where(
                df_with_rd['Net Prod. Hours Bought'] != 0,
                df_with_rd['Direct Programme Cost'] / (df_with_rd['Net Prod. Hours Bought'] / FTE_HOURS_PER_YEAR),
                np.nan
            )
        # Show updated table
        st.dataframe(df_with_rd.style.format(valid_formats, na_rep="N/A"), height=(df_with_rd.shape[0] + 1) * 35 + 3)

    # New section: What do I get for the extra money spent on covering fixed costs?
    st.markdown("## What do I get for the extra money spent on covering fixed costs?")
    st.markdown("""
1. The bigger the net loss we incur by serving EAs, the harder it is for me to justify it to our other funders, who've thus far covered 100% of the fixed costs and took on the risk of failure.
2. Experimentation on how to make the results decay slower has extremely high EV. Play around with sliders to see for yourself.
3. We we can likely self-fund indefinitely, within twelve months, if we successfully execute on our development plan.
""")
    st.markdown('[Read details here](https://docs.google.com/document/d/11z3Inq8lIgNhgyAmlakWyfbmcvOjJQFH7bjjiwu07IE/edit?usp=sharing)') 