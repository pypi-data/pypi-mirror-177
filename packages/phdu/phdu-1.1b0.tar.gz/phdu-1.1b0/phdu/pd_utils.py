"""
pandas utils

Includes    latex_table:      f:  pd.DataFrame -> latex table.
"""
import pandas as pd
import numpy as np
from functools import reduce     

def latex_table(df, index=False, **kwargs):
    """Pandas DataFrame -> Latex table."""
    col_format = "c" if isinstance(df, pd.core.series.Series) else "c"*len(df.columns)
    if index:
        col_format += "c"
    table_replacements = (("\\toprule", "\\toprule "*2),
                          ("\\bottomrule", "\\bottomrule "*2)
    )
    text_replacements = (("\\textbackslash ", "\\"),
                         ("\{", "{"), 
                         ("\}", "}"),
                         ("\$", "$"),
                         ("\_", "_"),
                         ("\\textasciicircum ", "^")
    )
    table_formatter = lambda x:  reduce(lambda a, kv: a.replace(*kv), table_replacements, x)
    text_formatter = lambda x: reduce(lambda a, kv: a.replace(*kv), text_replacements, x)
    formatter = lambda x: text_formatter(table_formatter(x))
    print(formatter(df.to_latex(index=index, column_format=col_format, **kwargs)))
    return

def expand_sequences(df, dt=1, maxlen=None):
    """
    Input: DataFrame. Each element is an array and all arrays start at the same time and have the same time step dt.
    Returns: MultiColumn DataFrame: (df.index,  (df.columns, time_steps))
    """
    if df.isna().values.any():
        if maxlen is None:
            maxlen = int(df.applymap(lambda x: x.size if isinstance(x, np.ndarray) else np.NaN).max().max())
        df_padded = df.applymap(lambda x: np.hstack((x, np.NaN*np.empty((maxlen-x.size)))) if isinstance(x, np.ndarray) else np.NaN*np.empty((maxlen)))
    else:
        if maxlen is None:
            maxlen = int(df.applymap(lambda x: x.size).values.max())
        df_padded = df.applymap(lambda x: np.hstack((x, np.NaN*np.empty((maxlen-x.size)))))
    df_padded_arr = np.stack([np.vstack(x) for x in df_padded.values]) # shape (df.shape[0], df.shape[1], time_steps)
    return pd.DataFrame(df_padded_arr.reshape((df.shape[0], -1)), 
                        index = df.index, 
                        columns = pd.MultiIndex.from_product([df.columns, dt*np.arange(maxlen)]))
