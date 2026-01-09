# parameters.py
import pandas as pd

# --- 1. GLOBAL CONSTANTS ---
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

# Quantity of fuel used
FUEL_QTY_DATA = {
    "Fuel consumption of a stove (ton/household/year)": ["Wood", "Charcoal", "Other"],
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

# --- 4. AGRICULTURE DATA ---
# Format: "Crop Name": (AGB_Default, BGB_Default, Soil_Default)
# Sourced strictly from 'parameter_with_source.xlsx' (Central Africa)
AGRI_CROP_DATA = {
    "Alley cropping": (2.75, 0.59, 27.3),
    "Hedgerow": (0.47, 0.11, 27.3),
    "Multistrata": (2.98, 0.72, 27.3),
    "Parkland": (0.59, 0.21, 27.3),
    "Perennial fallow": (5.3, 1.27, 27.3),
    "Shade perennial": (1.82, 0.44, 27.3),
    "Silvopasture": (2.91, 0.79, 27.3),
    # The following values are from 'DEFAULT_AGB_BGB_SOIL_BY_REGION.csv' under Central Africa
    "Silvoarable": (5.09, 1.22, 27.3), 
    "Oil Palm": (2.4, 0.0, 27.3),      
    "Rubber": (3.0, 0.0, 27.3),        
    "Tea": (0.7, 0.0, 27.3),
}

def get_agri_params(country):
    return {
        "agb_bgb_soil": AGRI_CROP_DATA,
        "residue_multiplier": 0.47
    }