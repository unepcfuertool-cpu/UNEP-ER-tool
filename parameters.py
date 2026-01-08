# parameters.py

# --- 1. GLOBAL CONSTANTS ---
GWP = {
    "CO2": 1,
    "CH4": 28,  # IPCC AR5
    "N2O": 265
}

CARBON_FRACTION_DEFAULT = 0.47  # Tier 1 Default

# --- 2. SOIL & LAND PARAMETERS ---
# Standard Tier 1 Default (user can override with Tier 2)
REF_SOC_DEFAULT = 47.0 

# --- 3. ENERGY PARAMETERS ---
ENERGY_DEFAULTS = {
    "EF_traditional_cookstove": 2.26, # tCO2e/ton fuel
    "EF_charcoal_production": 3.20,   # tCO2e/ton charcoal
    "EF_substitution_fuel": 63.10,    # tCO2/TJ (LPG)
    "C_intensity_electricity": 0.20,  # tCO2e/MWh (Congo Basin Grid)
    "Default_fuel_qty": 1.50,         # tons/year/household
    "Default_energy_gen": 3.50        # MWh/year
}

# --- 4. FORESTRY PARAMETERS ---
RIL_C_FACTOR = 3.66 # tCO2e/m3

# --- 5. AGRICULTURE DATA ---
try:
    import imported_data
    AGRI_DATA = imported_data.AGRI_CROP_DATA
except ImportError:
    # Safety Net Defaults
    AGRI_DATA = {
        "Alley cropping": (2.75, 0.59, 27.3),
        "Hedgerow": (0.47, 0.11, 27.3),
        "Multistrata": (2.98, 0.72, 27.3),
        "Parkland": (0.59, 0.21, 27.3),
        "Perennial fallow": (5.3, 1.27, 27.3),
        "Shaded perennial": (1.82, 0.44, 27.3),
        "Tea": (1.82, 0.44, 27.3),
        "Silvopasture": (2.91, 0.79, 27.3),
    }

def get_agri_params(country):
    return {
        "agb_bgb_soil": AGRI_DATA,
        "residue_multiplier": 0.47
    }