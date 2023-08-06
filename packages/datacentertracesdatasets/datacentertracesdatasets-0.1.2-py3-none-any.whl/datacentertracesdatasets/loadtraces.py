import pandas as pd
from io import StringIO

def get_alibaba_2018_trace(trace="machine_usage", day=None, stride_seconds=10, format='dataframe'):
    try:
        import importlib.resources as pkg_resources
    except ImportError:
        import importlib_resources as pkg_resources
    from . import alibaba2018
    assert trace in ["machine_usage"], 'only "machine_usage" trace is supported right now'
    assert day is None or (day > 0 and day < 9), 'alibaba days range from 1 to 8'
    assert stride_seconds in [10, 30, 300], 'only 10, 30 and 300 seconds are currently suported as stride_seconds'
    assert format in ['dataframe', 'ndarray'], 'only "dataframe" and "ndarray" are supported right now'
    if (day is None):
        contents = pkg_resources.read_text(alibaba2018, f'{trace}_days_1_to_8_grouped_{stride_seconds}_seconds.csv')
        res = pd.read_csv(StringIO(contents), index=False)
    else:
        contents = pkg_resources.read_text(alibaba2018, f'{trace}_day_{day}_grouped_{stride_seconds}_seconds.csv')
        res = pd.read_csv(StringIO(contents), index=False)
    if format == 'ndarray':
        res = res.to_numpy()
    return res