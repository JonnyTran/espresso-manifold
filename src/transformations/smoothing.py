import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess

def lowess_smoothing(series:pd.Series, frac=0.05):
    frac = frac * series.index.size / 116 # adjust for length
    x_y = lowess(series, series.index, frac=frac, is_sorted=True, missing='none')

    series = pd.Series(x_y[:, 1], index=series.index)
    series[series <0] = 0
    return series


def lowess_smoothing_arr(arr: pd.Series, frac=0.05):
    x_y = lowess(arr, range(arr.size), frac=frac, is_sorted=True, missing='none')

    return x_y