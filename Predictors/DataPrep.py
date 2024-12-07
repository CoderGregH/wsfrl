import polars as pl


def get_data():
    results_with_pb_df: pl.DataFrame = pl.read_csv("../../data/withpb_and_age-all-results.csv")

    results_with_pb_df = results_with_pb_df.drop("XC_Count_of_event", "XC_Position_Min", "XC_Position_Max",
                                                 "XC_Min_Age", "XC_Max_Age", "exists", "from_file")

    # Gender Clean up
    results_with_pb_df = results_with_pb_df.with_columns(
        pl.col("Gender").str.slice(0, 1).alias("Gender")
    )

    results_with_pb_df = results_with_pb_df.with_columns(
        pl.col("is_pb").cast(pl.Boolean),
        pl.col("first_time_run").cast(pl.Boolean)
    )



    return results_with_pb_df
