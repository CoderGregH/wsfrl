import pandas as pd

def validate_features_vs_target(df_features : pd.DataFrame, df_target : pd.DataFrame):

    if len(df_features) != len(df_target):
        print(f"WARNING Features ({len(df_features)}) != target ({len(df_target)})")
    else:
        print(f"MATCH Features_df shape: {df_features.shape} vs Target {df_target.shape}")



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