# Configuration data for the CEA Coaching EAs Streamlit app

offerings = {
    "Bespoke Offering": {
        "retention": 70.0,
        "num_participants": 400,
        "sessions_per_participant": 6,
        "default_effect_duration": 6.0,  # months
        "pre_intervention_hours": 40,    # example default
        "post_intervention_hours": 45,   # example default
        "productivity_multiplier": 1.10  # example default (10% more productive)
    },
    "Procrastination": {
        "retention": 80.0,
        "num_participants": 300,
        "sessions_per_participant": 4,
        "default_effect_duration": 4.0,
        "pre_intervention_hours": 35,
        "post_intervention_hours": 40,
        "productivity_multiplier": 1.08
    },
    "Insomnia": {
        "retention": 80.0,
        "num_participants": 150,
        "sessions_per_participant": 4,
        "default_effect_duration": 4.0,
        "pre_intervention_hours": 30,
        "post_intervention_hours": 36,
        "productivity_multiplier": 1.06
    }
}

DEFAULT_COST_PER_SESSION = 5.0
DEFAULT_WORKING_WEEKS_PER_YEAR = 46
DEFAULT_PROPORTION_TIME_DURING_WORK = 0.5  # 50%
DEFAULT_HOMEWORK_HOURS_PER_SESSION = 1.0
DEFAULT_AVG_SESSIONS_FOR_DROPOUTS = 2.0
DEFAULT_SESSION_DURATION = 1.0 # hour 

DEFAULT_TIMEFRAME_OF_INTEREST_MONTHS = 12.0 

# New Advanced Cost Parameters
DEFAULT_DISAPPOINTMENT_HOURS_PER_DROPOUT = 40.0
# DEFAULT_ORGANIZATION_YEARLY_CLIENTS = 3600.0
DEFAULT_BASELINE_ORG_YEARLY_CLIENTS = 3100.0 # Baseline yearly clients for the org, EXCLUDING this specific EA offering's participants

# Constants for overall cost explanation
ORGANIZATION_RD_BUDGET_USD = 149160.0 # Fixed R&D Budget in USD 