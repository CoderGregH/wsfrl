import pandas as pd

def get_boolean_features(df : pd.DataFrame, exclude_races = True, exclude_ages = True):


    binary_columns = [
        col for col in df.columns
        if (not exclude_races or not col.startswith('RaceName_')) and
           (not exclude_ages or not col.startswith('p_of_10_road_age_category_'))
    ]
    binary_columns.append("is_club_member_false")
    binary_columns.append("Gender_F")

    return binary_columns