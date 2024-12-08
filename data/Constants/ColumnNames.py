from enum import auto
from strenum import StrEnum


class WsfrlColumnOverall(StrEnum):
    Position = auto()
    Time = auto()
    TimeInSeconds = "time_in_seconds"
    BibNumber = "Bib Number"
    Name = auto()
    Gender = auto()
    GenderPosition = "Gender Position"
    Club = auto()
    Points = auto()

class WsfrlColumnForPowerOfTen(StrEnum):
    PowerOfTenClub = 'p_of_10_club',
    PowerOfTenGender = 'p_of_10_gender',
    AthleteId ='p_of_10_athlete_id',
    MatchBy = 'match_type',
    MatchCount = 'matches',
    MatchUsingParameters ='parameters_used',




class WsfrlColumnForAges(StrEnum):
    AgeCategoryTrack = 'p_of_10_track_age_category',
    AgeCategoryRoad ='p_of_10_road_age_category',
    AgeCategoryXc ='p_of_10_xc_age_category',
    AgeMinRange = 'min_age',
    AgeMaxRange = 'max_age',
    AgeAvgRange = 'average_age',
    DobMin ='min_dob',
    DobMax ='max_dob',
    DobAvg ='avg_dob'

class WsfrlColumnForAgesGenerated(StrEnum):
    BlendedAgeCategory = 'blended_age_category'

class WsfrlColumnPriorStats(StrEnum):
    ClubMates = 'fellow_club_mates_running'
    ClubMatesMale = 'fellow_club_mates_running_male'
    ClubMatesFemale = 'fellow_club_mates_running_female'
    Tenure = 'wsfrl_tenure_in_years'
    TotalPriorRunCount ='wsfrl_tenure_in_runs'
    PositionBestYear ='position_record_best_year'
    PositionYearsSinceBest = 'position_record_years_since_best'
    PositionWorstYear = 'position_record_worst_year'
    PositionYearSinceWorst = 'position_record_years_since_worst'
    PositionBestEver = 'position_record_best_position_all_time'
    PositionAverageEver = 'position_record_average_position_all_time'
    PositionWorstEver = 'position_record_worst_position_all_time'
    TotalPriorRunCountYtd = 'runs_in_wsfrl_year_to_date'
    PositionBestYtd = 'best_position_year_to_date'
    PositionAverageYtd = 'average_position_year_to_date'
    PositionWorstYtd = 'worst_position_year_to_date'
    PointsBestYtd = 'best_points_year_to_date'
    PointsAverageYtd = 'average_points_year_to_date'
    PointsWorstYtd = 'worst_points_year_to_date'

