import polars as pl

from data.Constants.ColumnNames import WsfrlColumnOverall, WsfrlColumnCalculated, WsfrlColumnPriorStats


def get_data():
    results_with_pb_df: pl.DataFrame = pl.read_csv("../../data/withpb_and_age-all-results.csv")

    results_with_pb_df = results_with_pb_df.drop("XC_Count_of_event", "XC_Position_Min", "XC_Position_Max",
                                                 "XC_Min_Age", "XC_Max_Age", "exists", "from_file")

    # Gender Clean up
    results_with_pb_df = results_with_pb_df.with_columns(
        pl.col("Gender").str.slice(0, 1).alias("Gender")
    )

    bool_columns = [WsfrlColumnCalculated.IsPBClub,
                     WsfrlColumnCalculated.IsClubMember,
                     WsfrlColumnCalculated.IsBigClub,
                     WsfrlColumnCalculated.IsFirstTimeRun]

    results_with_pb_df = results_with_pb_df.with_columns(
        [pl.col(col).cast(pl.Boolean) for col in bool_columns]
    )

    results_with_pb_df = results_with_pb_df.with_columns(
        pl.col(WsfrlColumnCalculated.IsPBClub).cast(pl.Boolean),
        pl.col(WsfrlColumnCalculated.IsFirstTimeRun).cast(pl.Boolean)
    )

    # Cast float columns to integers
    convert_to_int_columns = [str(WsfrlColumnOverall.TimeInSeconds),
                              str(WsfrlColumnOverall.GenderPosition),
                              str(WsfrlColumnOverall.ClubPosition),
                              str(WsfrlColumnOverall.ClubPositionGender),
                              str(WsfrlColumnOverall.BibNumber),
                              str(WsfrlColumnOverall.Points),
                              str(WsfrlColumnPriorStats.PriorRunAttempt)]

    convert_to_int_columns.extend([str(col) for col in WsfrlColumnPriorStats])

    results_with_pb_df = results_with_pb_df.with_columns(
        [pl.col(col).cast(pl.Int32) for col in convert_to_int_columns]
    )



    return results_with_pb_df
