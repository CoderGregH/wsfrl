import pandas as pd

def validate_features_vs_target(df_features : pd.DataFrame, df_target : pd.DataFrame):

    if len(df_features) != len(df_target):
        print(f"WARNING Features ({len(df_features)}) != target ({len(df_target)})")
    else:
        print(f"MATCH Features_df shape: {df_features.shape} vs Target {df_target.shape}")


def general_feature_validation(features_df,feature_columns_to_validate):

    # Find columns that are not in the combined feature list
    extra_columns = [col for col in features_df.columns if col not in feature_columns_to_validate]
    print(
        f"WARNING (Be Aware)- Column that exist in the features_df but not in the feature_columns_to_validate list: {extra_columns}")

    missing_columns = [col for col in feature_columns_to_validate if col not in features_df.columns]

    good_prefix = "GOOD"
    bad_prefix = "BAD"

    # Print the results
    if missing_columns:
        print(f"{bad_prefix} - Missing columns in WHOLE set: {missing_columns}")
    else:
        print(
            f"{good_prefix} - All feature columns {len(feature_columns_to_validate)} exist in the DataFrame {len(features_df.columns)}.")


def get_boolean_features(df: pd.DataFrame, prefix: str) -> list:
    binary_columns = []

    for col in df.columns:
        if col.startswith(prefix):
            binary_columns.append(col)

    if len(binary_columns) == 0:
        print(f"No columns found with prefix: {prefix}")

    return binary_columns


def filter_features(df ) -> pd.DataFrame:
    # Drop the target prediction column from the features
    pb_achieved_features_df = df.drop("is_pb")

    # Info about the RACE or runner that is not useful for prediction
    #   runner
    pb_achieved_features_df = pb_achieved_features_df.drop("Bib Number", "Name", "Club")
    pb_achieved_features_df = pb_achieved_features_df.drop('p_of_10_firstname', 'p_of_10_surname',
                                                           'p_of_10_track_age_category', 'p_of_10_xc_age_category',
                                                           'p_of_10_gender', 'p_of_10_club', 'p_of_10_athlete_id')
    #   race
    pb_achieved_features_df = pb_achieved_features_df.drop("date", 'year', 'month', 'day', 'distance')

    # achieved time position which would be unknown at the start of the race!
    pb_achieved_features_df = pb_achieved_features_df.drop("Time", "pace", 'Position', 'time_in_seconds',
                                                           'Gender Position', 'Points', 'club_position',
                                                           'club_position_gender', 'first_time_run')

    # Prior info on years which are versus the current year or just contains the year
    pb_achieved_features_df = pb_achieved_features_df.drop("prior_quickest_run_in_year", "prior_time_vs_current_change",
                                                           "prior_time_vs_current_time", "prior_quickest_run_time",
                                                           'prior_quickest_vs_run_time', 'position_record_best_year',
                                                           'position_record_worst_year')

    pb_achieved_features_df = pb_achieved_features_df.drop('match_type', 'matches', 'parameters_used', 'min_age',
                                                           'max_age', 'min_dob', 'max_dob', 'avg_dob')

    return pb_achieved_features_df