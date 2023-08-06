import re
from typing import List

import numpy as np
import pandas as pd
from pandas import DataFrame, MultiIndex
from pandas.core.tools.datetimes import DatetimeScalarOrArrayConvertible

from .._tools import custom_convert_dtypes


def convert_df_columns_to_datetime(
    df: pd.DataFrame, entry: str, utc: bool = None, delete_tz: bool = False
) -> pd.DataFrame:
    """Converts particular dataframe columns to datetime according the pattern.

    Converts particular dataframe column or columns if one of more columns
    matches the pattern, returns same dataframe otherwise.

    Parameters
    ----------
    df : pd.DataFrame
        Pandas dataframe to convert.
    entry: str
        Pattern to find a column to convert.
    utc : bool
        Convert to UTC if True.
    delete_tz : bool
        Convert to timezone-unaware if True.

    Returns
    -------
    pd.DataFrame
        Converted dataframe
    """
    columns_indexes = [
        index
        for index, name in enumerate(df.columns.values)
        if entry.lower() in name.lower()
    ]

    return convert_df_columns_to_datetime_by_idx(df, columns_indexes, utc, delete_tz)


def convert_df_columns_to_datetime_by_idx(
    df: pd.DataFrame,
    columns_indexes: List[int],
    utc: bool = None,
    delete_tz: bool = False,
):
    """Convert dataframe columns to datetime by index.

    Parameters
    ----------
    df : pd.Dataframe
        Pandas dataframe to convert.
    columns_indexes : List[int]
        List of indexes of columns to convert.
    utc : bool
        Convert to UTC if True.
    delete_tz : bool
        Convert to timezone-unaware if True.

    Returns
    -------
    df
        Converted dataframe.
    """
    for idx in columns_indexes:
        df.iloc[:, idx] = pd.to_datetime(df.iloc[:, idx], utc=utc, errors="coerce")
        if delete_tz:
            df.iloc[:, idx] = df.iloc[:, idx].dt.tz_localize(None)

    return df


def convert_df_columns_to_datetime_re(
    df: pd.DataFrame, pattern: re.compile
) -> pd.DataFrame:
    """Convert dataframe columns to datetime using regular expression pattern.

    Parameters
    ----------
    df : pd.Dataframe
        Pandas dataframe to convert.
    pattern : re.compile
        Regular expression pattern to check columns.

    Returns
    -------
    df
        Converted dataframe
    """
    column_indexes = [
        index for index, name in enumerate(df.columns.values) if pattern.search(name)
    ]

    return convert_df_columns_to_datetime_by_idx(
        df, column_indexes, utc=True, delete_tz=True
    )


def convert_str_to_datetime(s: str) -> DatetimeScalarOrArrayConvertible:
    date = pd.to_datetime(s, utc=True, errors="coerce")
    date = date.tz_localize(None)
    return date


def sort_df_by_universe(df: DataFrame, universe: List[str]) -> DataFrame:
    length = len(universe)

    if length == 1:
        return df

    columns = df.columns

    def make_getidx():
        get_index = universe.index
        if isinstance(columns, MultiIndex):

            def geti(i):
                return i[0]

        else:

            def geti(i):
                return i

        def inner(i):
            try:
                index = get_index(geti(i))
            except ValueError:
                index = length
            return index

        return inner

    getidx = make_getidx()
    # [3, 0, 2, 1]
    curr_order = [getidx(col) for col in columns]
    # [0, 1, 2, 3]
    expected_order = list(range(length))
    if curr_order != expected_order:
        sorted_columns = (col for _, col in sorted(zip(curr_order, columns)))
        df = df.reindex(columns=sorted_columns)
    return df


def convert_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function is an extension to the standard pandas.DataFrame.convert_dtypes.

    Correct return dataframe if we have this columns in dataframe:

    GOOG.O                    Currency
    Date
    2020-12-31 00:00:00+00:00     <NA>
    2020-12-31 00:00:00+00:00     <NA>

    Correct convert None, np.nan, pd.NA, pd.NaN to pd.NA, see official docs:
    https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html#missing-data-na

    Correct convert big int from Linux, Windows platform.


    Parameters
    ----------
    df: pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    if df.empty:
        return df

    name = df.columns.name
    df.fillna(np.nan, inplace=True)
    df = custom_convert_dtypes(df)
    df.fillna(pd.NA, inplace=True)
    df.columns.name = name
    return df
