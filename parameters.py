# parameters.py
import pandas as pd

# --- 1. GLOBAL CONSTANTS (Top Row) ---
GWP_DEFAULTS = {
    "CO2": 1,
    "CH4": 34,
    "NMVOC": 3.4,
    "CO": 1.8,
    "N2O": 265
}

REF_SOC_DEFAULT = 19
CARBON_FRACTION_DEFAULT = 0.47

# --- 2. ENERGY MATRICES ---

# Emission factor traditional cookstoves (g/kg)
EF_COOKSTOVES_DATA = {
    "Type": ["Trad. cookstoves [Wood]", "Trad. cookstoves [Charcoal]", "Trad. cookstoves [Other]"],
    "CO2": [1638, 2533, 0],
    "CH4": [5, 11, 0],
    "NMVOCs": [10, 16, 0],
    "CO": [113, 313, 0],
    "Black carbon": [1.06, 0.38, 0]
}

# Quantity of fuel used (ton/household/year)
FUEL_QTY_DATA = {
    "Fuel Type": ["Wood", "Charcoal", "Other"],
    "Value": [5.475, 5.475, 5.475]
}

# Energy generated (MWh/kg)
ENERGY_GEN_DATA = {
    "Type": ["Trad. Cookstove"],
    "MWh/kg": [0.003]
}

# Emission factor charcoal production (g/kg)
EF_CHARCOAL_DATA = {
    "Type": ["Earth mounds / pits"],
    "CO2": [9778],
    "CH4": [47],
    "NMVOCs": [0],
    "CO": [0],
    "Black carbon": [0]
}

# Emission factor of substitution fuel
EF_SUBSTITUTION_DATA = {
    "Fuel": [
        "Modern fuel", "LPG", "Electric (incl. induction)", "Natural gas", "Kerosene", "Propane",
        "Renewable fuel", "Ethanol", "Biodiesel", "Other biogas"
    ],
    "CO2 [kg/MWh]": [None, 210.61, 24.46, 181.09, 256.66, 214.57, None, 233.58, 252.01, 177.71],
    "CH4 [g/MWh]": [None, 10.24, 0.00, 3.41, 10.24, 10.24, None, 3.75, 3.75, 10.92],
    "N2O [g/MWh]": [None, 2.048, 0.000, 0.341, 2.048, 2.048, None, 0.375, 0.375, 2.150]
}

# Carbon intensity of electricity (Congo Basin)
C_INTENSITY_DATA = {
    "Country": ["Cameroon", "CAR", "Congo", "DRC", "Eq. Guinea", "Gabon"],
    "kgCO2/MWh": [305.42, 0.00, 700.00, 24.46, 591.84, 491.60]
}

# --- 3. FORESTRY ---
RIL_C_DATA = {
    "Parameter": [
        "Felled trees abandoned (tC/ 1 trees / tree)",
        "Felled log length left (tC/ 1% / ha)",
        "Trees killed by skidding (tC/ 1 tree/ha)",
        "Area of haul road and log-landing corridors (tC/m2/ha)"
    ],
    "Value": [0.3092, 0.0257, 0.4500, 0.0132]
}

# --- 4. AGRI (Helper) ---
try:
    import imported_data
    AGRI_DATA = imported_data.AGRI_CROP_DATA
except ImportError:
    AGRI_DATA = {}

def get_agri_params(country):
    return {"agb_bgb_soil": AGRI_DATA}