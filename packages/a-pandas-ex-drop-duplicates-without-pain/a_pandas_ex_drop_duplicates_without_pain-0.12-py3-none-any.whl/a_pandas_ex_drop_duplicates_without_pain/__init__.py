from typing import Union
from a_pandas_ex_plode_tool import qq_s_isnan
from pandas.core.base import PandasObject
import pandas as pd
import itertools
import operator


def series_to_dataframe(
    df: Union[pd.Series, pd.DataFrame]
) -> (Union[pd.Series, pd.DataFrame], bool):
    dataf = df.copy()
    isseries = False
    if isinstance(dataf, pd.Series):
        columnname = dataf.name
        dataf = dataf.to_frame()

        try:
            dataf.columns = [columnname]
        except Exception:
            dataf.index = [columnname]
            dataf = dataf.T
        isseries = True

    return dataf, isseries


def ds_drop_duplicates_without_pain(
    df: Union[pd.Series, pd.DataFrame],
    subset: Union[None, list] = None,
    keep: str = "first",
    ignore_index: bool = False,
) -> Union[pd.DataFrame, pd.Series]:
    df2, isseries = series_to_dataframe(df)

    if qq_s_isnan(subset):
        subset = df2.columns.to_list()
    df3 = df2[subset].copy()
    df3index = df3.index.__array__().copy()
    df3indexnew = [(x, y) for x, y in zip(range(len(df3index)), df3index)]
    df3.index = df3indexnew.copy()
    dub = (
        df3.fillna(pd.NA)
        .apply(
            lambda li_: pd.Series(
                itertools.accumulate((str(_) for _ in li_), operator.add)
            ),
            axis=1,
        )
        .drop_duplicates(keep=keep, ignore_index=ignore_index)
    )
    df2["____indi"] = df2.index.__array__().copy()
    df2.index = df3indexnew.copy()

    df2 = df2.loc[df2.index.isin(dub.index)].reset_index(drop=True)
    df2.index = df2["____indi"].__array__().copy()
    df2 = df2.drop(columns=["____indi"])

    if isseries:
        return df2[df2.columns[0]]
    return df2


def pd_add_drop_duplicates_without_pain():
    PandasObject.ds_drop_duplicates_without_pain = ds_drop_duplicates_without_pain
