import pytest
import polars as pl

from Predictors.DataPrep import get_data
from data.Constants.ColumnNames import WsfrlColumnCalculated, WsfrlColumnOverall


def test_get_data_convert_to_int():
    df = get_data()

    assert len(df) > 0
    assert df[WsfrlColumnOverall.TimeInSeconds].dtype == pl.Int32
    assert df[WsfrlColumnOverall.GenderPosition].dtype == pl.Int32
    assert df[WsfrlColumnOverall.Points].dtype == pl.Int32


def test_get_data_convert_to_bool():

    df = get_data()

    assert len(df) > 0
    assert df[WsfrlColumnCalculated.IsPBClub].dtype == pl.Boolean
    assert df[WsfrlColumnCalculated.IsFirstTimeRun].dtype == pl.Boolean

    assert df[WsfrlColumnCalculated.IsClubMember].dtype == pl.Boolean
    assert df[WsfrlColumnCalculated.IsBigClub].dtype == pl.Boolean
