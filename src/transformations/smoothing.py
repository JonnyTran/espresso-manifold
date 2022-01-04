import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess


def lowess_smoothing(series: pd.Series, frac=0.05):
    if isinstance(series.index, pd.MultiIndex):
        time_idx = series.index.get_level_values(-1)
    else:
        time_idx = series.index

    frac = frac * time_idx.size / 116  # adjust for length
    x_y = lowess(series, time_idx, frac=frac, is_sorted=True, missing='none')

    smoothed = pd.Series(x_y[:, 1], index=time_idx)
    smoothed[smoothed < 0] = 0
    return smoothed


def lowess_smoothing_arr(arr: pd.Series, frac=0.05):
    x_y = lowess(arr, range(arr.size), frac=frac, is_sorted=True, missing='none')

    return x_y