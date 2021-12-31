import numpy as np


def numpy_fill(arr):
    '''Solution provided by Divakar.'''
    isna = np.isnan(arr)

    if not any(isna):
        return arr

    idx = np.where(~isna, np.arange(isna.shape[0]), 0)
    np.maximum.accumulate(idx, axis=0, out=idx)
    out = arr[idx]
    return out