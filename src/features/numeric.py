import numpy as np
import pandas as pd


def preinfusion_time(df: pd.DataFrame):
    if df['espresso_flow_weight'] is None or df['espresso_flow_weight'].size < 10:
        return None
    first_drip_idx = np.argmax(df["espresso_flow_weight"].cumsum() > 0.1)
    return df["timeframe"][first_drip_idx]