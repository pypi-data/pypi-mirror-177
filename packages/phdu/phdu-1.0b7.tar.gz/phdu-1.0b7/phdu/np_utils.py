import numpy as np
from numpy.lib.stride_tricks import as_strided

def rolling_view(x, window):
    """
    Returns rolling view (no extra memory needed) over first axis of x.
    Output shape: (x.shape[0]-window+1, window, *x.shape[1:])
    """
    stride = x.strides[0]
    shape = [x.shape[0] - window + 1, window]
    strides = [stride, stride]
    if x.ndim > 1:
        shape += [*x.shape[1:]]
        strides += [*x.strides[1:]]    
    return as_strided(x, shape=shape, strides=strides)