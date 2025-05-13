# Configuration data for the CEA Coaching EAs Streamlit app

offerings = {
    "Bespoke Offering": {
        "retention": 60.0,
        "num_participants": 400,
        "sessions_per_participant": 6,
        "default_effect_duration": 6.0,  # months
        "pre_intervention_hours": 39,    # updated default
        "post_intervention_hours": 45,   # updated default
        "productivity_multiplier": 1.04,  # updated default (4% more productive)
        "default_decay_rate": 50.0,       # percent, for Exponential Decay
        "default_months_to_zero": 12.0,   # months, for Linear Decay
        "default_decay_model": "Exponential Decay"
    },
    "Procrastination": {
        "retention": 70.0,
        "num_participants": 300,
        "sessions_per_participant": 4,
        "default_effect_duration": 4.0,
        "pre_intervention_hours": 35,
        "post_intervention_hours": 40,
        "productivity_multiplier": 1.08,
        "default_decay_rate": 80.0,       # percent, for Exponential Decay
        "default_months_to_zero": 6.0,
        "default_decay_model": "Exponential Decay"
    },
    "Insomnia": {
        "retention": 70.0,
        "num_participants": 150,
        "sessions_per_participant": 4,
        "default_effect_duration": 4.0,
        "pre_intervention_hours": 30,
        "post_intervention_hours": 36,
        "productivity_multiplier": 1.06,
        "default_decay_rate": 60.0,       # percent, for Exponential Decay
        "default_months_to_zero": 12.0,
        "default_decay_model": "Exponential Decay"
    }
}

DEFAULT_COST_PER_SESSION = 5.0
DEFAULT_WORKING_WEEKS_PER_YEAR = 46
DEFAULT_PROPORTION_TIME_DURING_WORK = 0.5  # 50%
DEFAULT_HOMEWORK_HOURS_PER_SESSION = 1.0
DEFAULT_AVG_SESSIONS_FOR_DROPOUTS = 2.0
DEFAULT_SESSION_DURATION = 1.0 # hour 

DEFAULT_TIMEFRAME_OF_INTEREST_MONTHS = 12.0 

DEFAULT_DISAPPOINTMENT_HOURS_PER_DROPOUT = 40.0
DEFAULT_BASELINE_ORG_YEARLY_CLIENTS = 3100.0 # Baseline yearly clients for the org, EXCLUDING this specific EA offering's participants

# Constants for overall cost explanation
ORGANISATION_FIXED_COSTS = 136000 # Fixed R&D Budget in USD 

# Programme-specific introduction text
programme_introductions = {
    "Bespoke Offering": '''
        **About the Bespoke Offering:**
        - This programme covers a wide range of issues, from dietary improvement and habit change to severe depression and anxiety.
        - Users include everyone from executives and grantmakers to unemployed EA-adjacents trying to break into EA roles.
        - Our best estimate for the median, representative client is someone working in an entry-level role at a mid-tier EA charity who has moderate clinical anxiety.
        - The median EA user will gain approximately **1.5 points of happiness (on a 0–10 scale)** if they came in seeking help with a mental illness, or about **0.8 points** if they came in for help with behaviour change or productivity.
    ''',
    "Insomnia": '''
        **About the Insomnia Programme:**
        - This programme is designed for EAs struggling with sleep, especially those with moderate to severe insomnia.
        - The intervention is based on cognitive behavioral therapy for insomnia (CBT-I), the gold standard treatment.
        - Participants are typically high-performing but experience significant productivity loss due to poor sleep.
    ''',
    "Procrastination": '''
        This four session programme helps people who're in the top 20% of procrastinators relative to the general population.

        Very little research exists on the long-term durability of procrastination interventions. We suspect that it will decay sharply without additional intervention. To help prevent relapse, completers will get a free referral link to [GoalsWon, a daily accountability service](https://www.goalswon.com/giving-back) (free for EAs). We think this is likely to dramatically reduce the likelihood of relapse. Their CEO reached out to me asking for more EA clients, so it's a win-win at no cost to you / us / users.
    '''
}

# Programme-specific productivity gain explanation text
programme_productivity_gain_explanations = {
    "Bespoke Offering": """
The average case of depression/anxiety is estimated to reduce productivity by 35%. The treatments we use reduce symptoms by ~42% on average, which would reduce the impairment down to a level associated with ~7% productivity loss instead., so a net gain of ~28%. However, ~25% of people seek help for diet, exercise and other things less severe with longer time to pay off. 

Our best guess is 20%, but the error bars are wide.
""",
    "Insomnia": """
An RCT of a CBT-I programme with a ~20% smaller effect size than ours caused a net gain of ~7 hours of at-work productivity per week. Our programme focuses on higher severity cases, where the burden is likely more extreme. Our best estimate is 25%.
""",
    "Procrastination": """
Chronic procrastination is associated with the same income loss as moderate depression (~35%). Given that our intervention takes someone to the 50th percentile, we think the best guess is thus around 35%.
"""
}