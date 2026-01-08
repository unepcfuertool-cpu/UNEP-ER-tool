# parameters.py

# 1. Try to load Excel data
try:
    import imported_data
    HAS_IMPORTED_DATA = True
    AGRI_DATA = imported_data.AGRI_CROP_DATA
    FOREST_DATA = imported_data.DEFORESTATION_RATES
except ImportError:
    HAS_IMPORTED_DATA = False
    # Fallback Defaults (Safety Net)
    AGRI_DATA = {
        "Alley cropping": (2.75, 0.59, 27.3),
        "Hedgerow": (0.47, 0.11, 27.3),
        "Multistrata": (2.98, 0.72, 27.3),
        "Parkland": (0.59, 0.21, 27.3),
        "Perennial fallow": (5.3, 1.27, 27.3),
        "Shaded perennial": (1.82, 0.44, 27.3),
        "Tea": (1.82, 0.44, 27.3),
        "Silvopasture": (2.91, 0.79, 27.3),
        "Silvoarable": (5.09, 1.22, 27.3)
    }
    FOREST_DATA = {"Dense Forest": 0.5, "Secondary Forest": 0.8}

# 2. Logic to serve data to app
DEFAULT_AGB_BGB_SOIL_BY_REGION = {
    "Central Africa": AGRI_DATA,
    "Indonesia": AGRI_DATA,
    "Brazil": AGRI_DATA
}

# 3. Fixed Parameters (Standard Constants)
RESIDUE_MULTIPLIER_BY_REGION = {
    "Central Africa": 0.47, "Indonesia": 0.47, "Brazil": 0.47
}

REMOVAL_FACTORS_BY_REGION = {
    region: {
        "tillage": {"Full tillage": 1, "Reduced tillage": 1.04, "No tillage": 1.1},
        "input": {"Low C input": 0.92, "Medium C input": 1, "High C input, no manure": 1.11, "High C input, with manure": 1.44},
        "residue": {"Burned": 2.26, "Retained": 2.26, "Exported": 2.26},
    }
    for region in ["Central Africa", "Indonesia", "Brazil"]
}

DEFORESTATION_RATES = FOREST_DATA