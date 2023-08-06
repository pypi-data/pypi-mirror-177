from functools import reduce
from pandas.core.frame import DataFrame


def search_in_whole_dataframe(df, method, *args, **kwargs):
    cols = df.columns
    allindex = []
    for x in cols:
        try:
            resas = reduce(
                lambda i, j: getattr(i, j), method.strip(" .").split("."), df[x]
            )(*args, **kwargs)
            resas = resas.dropna()
            resas = resas[resas != False]
            allindex.extend(resas.index.to_list().copy())
        except Exception as dea:
            continue
    try:
        return df.loc[sorted(set(allindex))]
    except Exception:
        return df.loc[sorted(allindex)]


def pd_add_loc_no_exceptions():
    DataFrame.d_loc_no_exception = search_in_whole_dataframe
