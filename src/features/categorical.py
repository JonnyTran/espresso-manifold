import pandas as pd

def agtron_to_roast_level(roast_level):
    """
    {'[25, 35)': "Very Dark",
     "[35, 41)": "Dark",
     "[41, 51)": "Medium-Dark",
     "[51, 61)": "Medium",
     "[61, 70)": "Medium-Light",
     "[70, 85)": "Light",
     "[85, 100)": "Very Light"}

    Args:
        roast_level ():

    Returns:

    """
    return pd.cut(roast_level, bins=[25, 35, 41, 51, 61, 70, 85, 100], include_lowest=True, right=False,
                  labels=["Very Dark", "Dark", "Medium-Dark", "Medium", "Medium-Light", "Light", "Very Light"])