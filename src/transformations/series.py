from typing import Dict

import numpy as np
import pandas as pd

TIMESERIES_COLS = ["timeframe", 'espresso_flow',
                   'espresso_weight', 'espresso_pressure', 'espresso_flow_goal',
                   'espresso_resistance', 'espresso_flow_weight', 'espresso_state_change',
                   'espresso_pressure_goal', 'espresso_flow_weight_raw',
                   'espresso_temperature_mix', 'espresso_water_dispensed',
                   'espresso_temperature_goal', 'espresso_resistance_weight',
                   'espresso_temperature_basket']


def least_common(series: pd.Series):
    return series.value_counts().tail(1).index[0]


AGGREGATIONS = {
    "espresso_flow": np.mean,
    'espresso_weight': np.mean,
    'espresso_pressure': np.mean,
    'espresso_flow_goal': np.mean,
    'espresso_resistance': np.mean,
    'espresso_flow_weight': np.mean,
    'espresso_state_change': "first",
    'espresso_pressure_goal': np.mean,
    'espresso_flow_weight_raw': np.mean,
    'espresso_temperature_mix': np.mean,
    'espresso_water_dispensed': np.mean,
    'espresso_temperature_goal': np.mean,
    'espresso_resistance_weight': np.mean,
    'espresso_temperature_basket': np.mean,
}


def timeseries_to_df_(values: Dict[str, pd.Series], timeframe):
    """

    Args:
        values (): All time series columns besides `timeframe`
        timeframe ():

    Returns:

    """
    try:
        time_index = pd.TimedeltaIndex(timeframe, unit="seconds", name="seconds")
        some_series = values[list(values.keys())[0]]

        if some_series.shape[0] < time_index.shape[0]:
            # print("Clipping timeframe", some_series.shape, time_index.shape)
            time_index = time_index[:some_series.shape[0]]

        elif some_series.shape[0] > time_index.shape[0]:
            # print("Clipping series", some_series.shape, time_index.shape)
            values = {k: v[:time_index.shape[0]] for k, v in values.items()}

        return pd.DataFrame(values, index=time_index)

    except Exception as e:
        print(e)
        return None


def extract_shot_series(shots_df: pd.DataFrame, smooth=[]):
    """

    Args:
        shots_df (DataFrame): A dataframe that contains an np.array for each field in `TIMESERIES_COLS`

    Returns:
        shots_series (DataFrame)
    """
    shots_series = shots_df.filter(TIMESERIES_COLS, axis=1).apply(
        lambda row: timeseries_to_df_(row[1:].to_dict(), timeframe=row.timeframe),
        axis=1)
    shots_series = pd.concat(shots_series.to_dict(), names=["id"])

    shots_series = preprocess_shot_series(shots_series)

    return shots_series


def preprocess_shot_series(shots_series: pd.DataFrame):
    shots_series["espresso_state_change"] = shots_series["espresso_state_change"].astype(str).astype("category")
    shots_series["espresso_state_change"].fillna(shots_series["espresso_state_change"].mode(dropna=True), inplace=True)

    shots_series['espresso_resistance'][shots_series['espresso_resistance'] > 100] = np.NaN

    return shots_series


def resample(shots_series: pd.DataFrame, freq='500L', agg_func=None):
    groupby = shots_series.reset_index().groupby(['id', pd.Grouper(key='seconds', freq=freq)])

    agg_funcs = {col: func for col, func in AGGREGATIONS.items() if col in shots_series.columns}
    if agg_func:
        agg_funcs.update(agg_func)

    resampled = groupby[TIMESERIES_COLS[1:]].agg(agg_funcs)

    return resampled
