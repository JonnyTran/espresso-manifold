import pandas as pd
from typing import Dict

TIMESERIES_COLS = ["timeframe", 'espresso_flow',
                   'espresso_weight', 'espresso_pressure', 'espresso_flow_goal',
                   'espresso_resistance', 'espresso_flow_weight', 'espresso_state_change',
                   'espresso_pressure_goal', 'espresso_flow_weight_raw',
                   'espresso_temperature_mix', 'espresso_water_dispensed',
                   'espresso_temperature_goal', 'espresso_resistance_weight',
                   'espresso_temperature_basket']


def timeseries_to_df(values: Dict[str, pd.Series], timeframe):
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


def extract_shot_series(shots_df: pd.DataFrame):
    """

    Args:
        shots_df (DataFrame): A dataframe that contains an np.array for each field in `TIMESERIES_COLS`

    Returns:
        shots_series (DataFrame)
    """
    shots_series = shots_df.filter(TIMESERIES_COLS, axis=1).apply(
        lambda row: timeseries_to_df(row[1:].to_dict(), timeframe=row.timeframe),
        axis=1)

    shots_series = pd.concat(shots_series.to_dict(), names=["id"])

    return shots_series


def resample_shot_series(shots_series: pd.DataFrame, freq='500L'):
    groupby = shots_series.reset_index().groupby(['id', pd.Grouper(key='seconds', freq=freq)])
    resampled = groupby[TIMESERIES_COLS[1:]].mean()
    
    return resampled