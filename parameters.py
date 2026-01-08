# parameters.py

# 1. Try to load Excel data
try:
    import imported_data
    AGRI_DATA = imported_data.AGRI_CROP_DATA
except ImportError:
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
    }

def get_agri_params(country):
    # Retrieve correct data based on region/country
    return {
        "agb_bgb_soil": AGRI_DATA,
        "residue_multiplier": 0.47
    }