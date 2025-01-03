import marimo

__generated_with = "0.9.30"
app = marimo.App()


@app.cell
def __():
    import polars as pl
    import pandas as pd
    from IPython.display import display
    return display, pd, pl


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Load 

        Load from CSV and clean up the data
        1. Remove all rows where the year is 2014 because its the first year there are no pbs
        2. Clean up gender as it contains "M" or "Male" and "F" or "Female". Just take the first character for simplity
        3. Data Types
        """
    )
    return


@app.cell
def __(display, pl):
    results_with_pb_df: pl.DataFrame = pl.read_csv("data/withpb_and_age-all-results.csv")


    results_with_pb_df = results_with_pb_df.drop("XC_Count_of_event", "XC_Position_Min", "XC_Position_Max", "XC_Min_Age", "XC_Max_Age","exists", "from_file")

    # Gender Clean up
    results_with_pb_df = results_with_pb_df.with_columns(
        pl.col("Gender").str.slice(0, 1).alias("Gender")
    )

    results_with_pb_df = results_with_pb_df.with_columns(
        pl.col("is_pb").cast(pl.Boolean),
        pl.col("first_time_run").cast(pl.Boolean)
    )

    display(results_with_pb_df)
    return (results_with_pb_df,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Do we have balanced target classes?

        We calculate the PB from the prior runs. 
        - The first year is 2014 which has no pbs because there is no prior data
        - This needs to be removed as its unbalances the data

        We also need to remove any first time only runs as a first is always a pb (technically) and will unbalance the data
        """
    )
    return


@app.cell
def __(display, pl, results_with_pb_df):
    results_with_pb_df_all = results_with_pb_df

    def pivot_on_year(df: pl.DataFrame):
        df_first_timers = df.filter(pl.col("first_time_run") == True)

        number_of_first_time_runs = len(df_first_timers)
        if number_of_first_time_runs > 0:
            print(f"WARNING this data set includes {number_of_first_time_runs} first time runs that will never be a PB")
        else:
            print("PERFECT No first time runs in the data set")
        
        print(f"Total number of rows: {len(df)}")
        
        # Pivot the DataFrame
        pivot_df = df.pivot(
            values=["is_pb"],
            index="year",
            on="is_pb",
            aggregate_function="len"
        ).sort("year")
        
        display(pivot_df)



    # Remove all rows where the year is 2014
    results_with_pb_df_filtered = results_with_pb_df.filter(
        (pl.col("year") != 2014) & (pl.col("first_time_run") == False)
    )


    print ('Before')

    pivot_on_year(results_with_pb_df_all)

    print ('After - without 2014 and first time runs == false')

    pivot_on_year(results_with_pb_df_filtered)
    return (
        pivot_on_year,
        results_with_pb_df_all,
        results_with_pb_df_filtered,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Find Categoricals

        These are columns with limited subset of values.

        For example **education** could be 
        - Graduate
        - Not Graduate

        In our data set
        - Club 
        - RaceName
        - Gender
        All of which are unlikely to influence a pb

        However, I'll add of these are categorical variables to the model.
        - RaceName
        - Gender

        The two `to_dummies` colum will turn these into columns with 1s and 0s.
        - So for `RaceName` it will create a column for each unique value in the column and set it to 1 if the value is present and 0 if not.
        - `RaceName_Downland Dash`
        - `RaceName_Fittleworth`
        - for each race combo




        """
    )
    return


@app.cell
def __(results_with_pb_df_filtered):
    results_with_pb_with_dummies_df = results_with_pb_df_filtered.to_dummies(
        ["Gender", "RaceName", 'p_of_10_road_age_category','is_club_member'], drop_first=True
    )
    return (results_with_pb_with_dummies_df,)


@app.cell
def __(display, results_with_pb_with_dummies_df):
    display(results_with_pb_with_dummies_df)
    return


@app.cell
def __(pd):
    def validate_features_vs_target(df_features : pd.DataFrame, df_target : pd.DataFrame):

        if len(df_features) != len(df_target):
            print(f"WARNING Features ({len(df_features)}) != target ({len(df_target)})")
        else:
            print(f"MATCH Features_df shape: {df_features.shape} vs Target {df_target.shape}")
    return (validate_features_vs_target,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Split the data

        Remove the target column from the features. **is_pb**

        Features are the columns that will be used to predict the target variable. 

        In this case, the features are all the columns that **Known before the race starts**
        - Prior performance 
        - Gender
        - Club mates (you would see them before the start and on course that could inspire you to run faster)
         

        """
    )
    return


@app.cell
def __(
    display,
    results_with_pb_df_filtered,
    results_with_pb_with_dummies_df,
    validate_features_vs_target,
):
    # Drop the target prediction column from the features
    pb_achieved_features_df = results_with_pb_with_dummies_df.drop("is_pb")

    # Info about the RACE or runner that is not useful for prediction  
    #   runner
    pb_achieved_features_df = pb_achieved_features_df.drop("Bib Number", "Name", "Club")
    pb_achieved_features_df = pb_achieved_features_df.drop(  'p_of_10_firstname', 'p_of_10_surname', 'p_of_10_track_age_category', 'p_of_10_xc_age_category', 'p_of_10_gender', 'p_of_10_club', 'p_of_10_athlete_id')
    #   race
    pb_achieved_features_df = pb_achieved_features_df.drop("date", 'year', 'month', 'day', 'distance' )

    # achieved time position which would be unknown at the start of the race! 
    pb_achieved_features_df = pb_achieved_features_df.drop( "Time", "pace", 'Position', 'time_in_seconds','Gender Position','Points', 'club_position', 'club_position_gender', 'first_time_run' )

    # Prior info on years which are versus the current year or just contains the year
    pb_achieved_features_df = pb_achieved_features_df.drop( "prior_quickest_run_in_year", "prior_time_vs_current_change", "prior_time_vs_current_time", "prior_quickest_run_time", 'prior_quickest_vs_run_time', 'position_record_best_year', 'position_record_worst_year' )

    pb_achieved_features_df = pb_achieved_features_df.drop(  'match_type',  'matches','parameters_used', 'min_age', 'max_age', 'average_age', 'min_dob', 'max_dob', 'avg_dob')


    pb_achieved_target_df = results_with_pb_df_filtered.select("is_pb")

    validate_features_vs_target(pb_achieved_features_df,pb_achieved_target_df)



    display(pb_achieved_features_df)
    return pb_achieved_features_df, pb_achieved_target_df


@app.cell
def __(
    pb_achieved_features_df,
    pb_achieved_target_df,
    validate_features_vs_target,
):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    SEED = 123

    (
        pb_achieved_feature_train_df,
        pb_achieved_feature_test_df,
        pb_achieved_target_train_df,
        pb_achieved_target_test_df,
    ) = train_test_split(
        pb_achieved_features_df,
        pb_achieved_target_df,
        test_size=0.30,
        random_state=SEED,
    )

    total_rows = len(pb_achieved_features_df)
    train_rows = len(pb_achieved_feature_train_df)
    test_rows = len(pb_achieved_feature_test_df)

    test_percentage_of_total = train_rows / total_rows

    print(f"Total Rows: {total_rows} Training Rows: {train_rows} Test Rows: {test_rows} Test Percentage of Total: {test_percentage_of_total:.2f}")

    validate_features_vs_target(pb_achieved_feature_train_df,pb_achieved_target_train_df)
    validate_features_vs_target(pb_achieved_feature_test_df,pb_achieved_target_test_df)
    return (
        SEED,
        StandardScaler,
        pb_achieved_feature_test_df,
        pb_achieved_feature_train_df,
        pb_achieved_target_test_df,
        pb_achieved_target_train_df,
        test_percentage_of_total,
        test_rows,
        total_rows,
        train_rows,
        train_test_split,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Scale the data

        It is important to scale the data so that the model is not distorted by really large values.

        ### My notes are 
        - Dimensionality reduction, which 
        1. Rotates the data. Some like 45 degrees
        2. Keeps the same data but reduce the complexity
        - Principal Component Analysis (PCA) is a technique that can be used to reduce the dimensionality of the data.

        ### Notes from Copilot
        The StandardScaler standardizes a feature by subtracting the mean and then scaling to unit variance. Unit variance means dividing all the values by the standard deviation.
        """
    )
    return


@app.cell
def __(
    StandardScaler,
    pb_achieved_feature_test_df,
    pb_achieved_feature_train_df,
):
    scaler = StandardScaler()

    pb_achieved_feature_train_scaled_df = scaler.fit_transform(
        pb_achieved_feature_train_df
    )

    pb_achieved_feature_test_scaled_df = scaler.fit_transform(
        pb_achieved_feature_test_df
    )

    print(f"Scaled Training data shape: {pb_achieved_feature_train_scaled_df.shape} vs Test {pb_achieved_feature_test_scaled_df.shape}")
    return (
        pb_achieved_feature_test_scaled_df,
        pb_achieved_feature_train_scaled_df,
        scaler,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        Do we have balanced target classes?
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        # Logistic regression example

        ```
        from sklearn.linear_model import LogisticRegression

        logistic_regression_classifier = LogisticRegression(penalty=None)

        logistic_regression_classifier.fit(
            pb_achieved_feature_train_scaled_df,
            pb_achieved_target_train_df.get_column("is_pb"),
        )
        ```

        ## Constraints

        > ValueError: Input X contains NaN.
        LogisticRegression does not accept missing values encoded as NaN natively. For supervised learning, you might want to consider sklearn.ensemble.HistGradientBoostingClassifier and Regressor which accept missing values encoded as NaNs natively. Alternatively, it is possible to preprocess the data, for instance by using an imputer transformer in a pipeline or drop samples with missing values


        One common strategy is to use the mean or median of the column to fill in the missing values. Here is how you can do it using SimpleImputer from sklearn.impute:  
        Import SimpleImputer.
        Create an imputer instance with the desired strategy (e.g., mean, median).
        Fit the imputer on the training data and transform both the training and test data.

        ```
        import numpy as np
        from sklearn.impute import SimpleImputer

        # Create an imputer instance with the mean strategy
        imputer = SimpleImputer(strategy="mean")

        # Fit the imputer on the training data and transform both the training and test data
        pb_achieved_feature_train_scaled_df = imputer.fit_transform(pb_achieved_feature_train_scaled_df)
        pb_achieved_feature_test_scaled_df = imputer.transform(pb_achieved_feature_test_scaled_df)

        # Create and fit the logistic regression classifier
        logistic_regression_classifier = LogisticRegression(penalty=None)

        logistic_regression_classifier.fit(
            pb_achieved_feature_train_scaled_df,
            pb_achieved_target_train_df.get_column("is_pb"),
        )
        ```




        """
    )
    return


@app.cell
def __(
    pb_achieved_feature_test_df,
    pb_achieved_feature_train_df,
    pb_achieved_target_test_df,
    pb_achieved_target_train_df,
):
    # Convert Polars DataFrame to Pandas DataFrame
    pb_achieved_feature_train_df_pandas = pb_achieved_feature_train_df.to_pandas()
    pb_achieved_target_train_df_pandas = pb_achieved_target_train_df.to_pandas()
    pb_achieved_feature_test_df_pandas = pb_achieved_feature_test_df.to_pandas()
    pb_achieved_target_test_df_pandas = pb_achieved_target_test_df.to_pandas()
    return (
        pb_achieved_feature_test_df_pandas,
        pb_achieved_feature_train_df_pandas,
        pb_achieved_target_test_df_pandas,
        pb_achieved_target_train_df_pandas,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        # Define Column for Defaults

        **All columns** need **default values** for **missing values**.

        This can have quite an impact on the model. For example if 
        - You defaulted missing **points to 10** which is the **highest point** you can score 
        - You would **create an artificially high amount** of high points scores when the data is much lower

        The second section of the code checks the column exist in the data frame. If they do not exist you will get an error.

        > ValueError: A given column is not a column of the dataframe 
        """
    )
    return


@app.cell
def __(pd):
    def get_boolean_features(df : pd.DataFrame, exclude_races = True, exclude_ages = True) -> list:
        binary_columns = []
        
        for col in df.columns:
            if exclude_races is False and col.startswith('RaceName_'):
                binary_columns.append(col)
            elif exclude_ages is False and col.startswith('p_of_10_road_age_category_'):
                binary_columns.append(col)
         
        binary_columns.append("is_club_member_false")
        binary_columns.append("Gender_F")
        
        return binary_columns
    return (get_boolean_features,)


@app.cell
def __(get_boolean_features, pb_achieved_feature_train_df_pandas):
    binary_columns = get_boolean_features(pb_achieved_feature_train_df_pandas, True, False)

    print(binary_columns)
    return (binary_columns,)


@app.cell
def __(display, pd):
    def validate_features(features_df, 
                          low_value_good_features: list,
                          high_value_good_features: list,
                          boolean_features: list,
                          time_in_seconds_features: list,
                          years_since_value_features: list) -> list:
        
      
        feature_columns_to_validate = (low_value_good_features 
                                          + high_value_good_features 
                                          + boolean_features 
                                          + time_in_seconds_features 
                                          + years_since_value_features)
      

        # Find columns that are not in the combined feature list
        extra_columns = [col for col in features_df.columns if col not in feature_columns_to_validate]
        print(f"WARNING (Be Aware)- Column that exist in the features_df but not in the feature_columns_to_validate list: {extra_columns}")
        
        # Check if columns exist in the DataFrame
        missing_columns = [col for col in feature_columns_to_validate if col not in features_df.columns]
        missing_low_value_good_columns = [col for col in low_value_good_features if col not in features_df.columns]
        missing_high_value_good_columns = [col for col in high_value_good_features if col not in features_df.columns]
        
        good_prefix ="GOOD"
        bad_prefix ="BAD"
        
        
        # Print the results
        if missing_columns:
            print(f"{bad_prefix} - Missing columns in WHOLE set: {missing_columns}")
        else:
            print(f"{good_prefix} - All feature columns {len(feature_columns_to_validate)} exist in the DataFrame {len(features_df.columns)}.")
        
        if missing_low_value_good_columns:
            print(f"{bad_prefix} - Missing columns in low_value_good_columns: {missing_low_value_good_columns}")
        else:
            print(f"{good_prefix} - All columns in low_value_good_columns exist in the DataFrame.")
        
        if missing_high_value_good_columns:
            print(f"{bad_prefix} - Missing columns in high_value_good_columns: {missing_high_value_good_columns}")
        else:
            print(f"{good_prefix} - All columns in high_value_good_columns exist in the DataFrame.")
        
        
        # Create a DataFrame with the count of NaN values for each column
        nan_counts_df = pd.DataFrame({
            'column': features_df.columns,
            'nan_count': features_df.isna().sum()
        })
        
        # Sort the DataFrame by nan_count in descending order
        nan_counts_df = nan_counts_df.sort_values(by='nan_count', ascending=False)
        nan_counts_df = nan_counts_df[nan_counts_df['nan_count'] > 0]
        
        # Set the maximum number of rows to display
        pd.set_option('display.max_rows', 30)
        
        display(nan_counts_df.head(8))
        
        return feature_columns_to_validate
    return (validate_features,)


@app.cell
def __():
    # Define the columns
    # "Position", "Gender Position", 
    time_in_seconds_columns = [ "prior_quickest_run_time_in_seconds"]

    years_since_value_columns = ["position_record_years_since_best", "position_record_years_since_worst"]

    low_value_good_columns = [
        "best_position_year_to_date", "average_position_year_to_date", "worst_position_year_to_date", "position_record_best_position_all_time", "position_record_worst_position_all_time", "prior_quickest_run_position",  "position_record_average_position_all_time"]


    high_value_good_columns = ["fellow_club_mates_running", "fellow_club_mates_running_male", "fellow_club_mates_running_female", "average_points_year_to_date", "best_points_year_to_date", "worst_points_year_to_date", "runs_in_wsfrl_year_to_date", 'wsfrl_tenure_in_runs','wsfrl_tenure_in_years', 'prior_run_attempts']
    return (
        high_value_good_columns,
        low_value_good_columns,
        time_in_seconds_columns,
        years_since_value_columns,
    )


@app.cell
def __(
    binary_columns,
    high_value_good_columns,
    low_value_good_columns,
    pb_achieved_feature_train_df_pandas,
    time_in_seconds_columns,
    validate_features,
    years_since_value_columns,
):
    # Combine the lists
    all_feature_columns = validate_features(pb_achieved_feature_train_df_pandas,
                                            low_value_good_columns, 
                                            high_value_good_columns, 
                                            binary_columns, 
                                            time_in_seconds_columns, 
                                            years_since_value_columns)
    return (all_feature_columns,)


@app.cell
def __(
    LogisticRegression,
    SimpleImputer,
    StandardScaler,
    binary_columns,
    high_value_good_columns,
    low_value_good_columns,
    np,
    pb_achieved_feature_train_df_pandas,
    pb_achieved_target_train_df_pandas,
    time_in_seconds_columns,
    years_since_value_columns,
):
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline

    # Create imputers for different columns

    seconds_value_imputer = SimpleImputer(strategy="constant", fill_value=400000)
    low_value_imputer = SimpleImputer(strategy="constant", fill_value=400)
    high_value_imputer = SimpleImputer(strategy="constant", fill_value=0) #-np.inf is too big for a float 
    binary_value_imputer = SimpleImputer(strategy="constant", fill_value=np.uint8(0))


    # Combine the imputers using ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ("low_value_good", low_value_imputer, low_value_good_columns),
            ("high_value_good", high_value_imputer, high_value_good_columns),
            ("binary", binary_value_imputer, binary_columns),
            ("seconds", seconds_value_imputer, time_in_seconds_columns),
            ("years_since", SimpleImputer(strategy="constant", fill_value=0), years_since_value_columns),
        ]
    )

    PIPELINE_STEP_PREPROCESSOR = "preprocessor"
    PIPELINE_STEP_SCALER = "scaler"

    # Create a pipeline with the preprocessor, scaler, and the logistic regression classifier
    pipeline = Pipeline(steps=[
        (PIPELINE_STEP_PREPROCESSOR, preprocessor),
        (PIPELINE_STEP_SCALER, StandardScaler()),
        ("classifier", LogisticRegression(penalty=None))
    ])

    # Fit the pipeline on the training data
    pipeline.fit(pb_achieved_feature_train_df_pandas, pb_achieved_target_train_df_pandas["is_pb"])

    # 
    # # Transform the test data
    # pb_achieved_feature_test_scaled_df = pipeline.transform(pb_achieved_feature_test_df)
    return (
        ColumnTransformer,
        PIPELINE_STEP_PREPROCESSOR,
        PIPELINE_STEP_SCALER,
        Pipeline,
        binary_value_imputer,
        high_value_imputer,
        low_value_imputer,
        pipeline,
        preprocessor,
        seconds_value_imputer,
    )


@app.cell
def __(binary_columns, display):
    display(binary_columns)
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Run Pipeline Stages explicitly

        To run the full pipeline 
        `pb_achieved_feature_test_scaled_df = pipeline.transform(pb_achieved_feature_test_df)`

        However this does not work 
        > AttributeError: This 'Pipeline' has no attribute 'transform'

        this is because `LogisticRegression` does not have a `transform` method, but a `fit`. 
          

        """
    )
    return


@app.cell
def __(LogisticRegression, pd, pipeline):
    def run_pipeline_in_stages(df_feature : pd.DataFrame, df_target : pd.DataFrame):

        # Transform the test data using the preprocessor part of the pipeline
        preprocessed_df = pipeline.named_steps['preprocessor'].transform(df_feature)

        # Scale the preprocessed test data
        scaled_df = pipeline.named_steps['scaler'].transform(preprocessed_df)
        
        classifier = LogisticRegression(penalty=None)

        classifier.fit(
            scaled_df,
            df_target["is_pb"],
        )
        
        return scaled_df, classifier
    return (run_pipeline_in_stages,)


@app.cell
def __(
    pb_achieved_feature_train_df_pandas,
    pb_achieved_target_train_df_pandas,
    run_pipeline_in_stages,
):
    (scaled_train_df,
    logistic_regression_classifier) = run_pipeline_in_stages(
        pb_achieved_feature_train_df_pandas,
        pb_achieved_target_train_df_pandas)
    return logistic_regression_classifier, scaled_train_df


@app.cell
def __(
    pb_achieved_feature_test_df_pandas,
    pb_achieved_target_test_df_pandas,
    run_pipeline_in_stages,
):
    (scaled_test_df,
    logistic_regression_classifier_junk) = run_pipeline_in_stages(
        pb_achieved_feature_test_df_pandas,
        pb_achieved_target_test_df_pandas)
    return logistic_regression_classifier_junk, scaled_test_df


@app.cell
def __(logistic_regression_classifier):
    logistic_regression_classifier.classes_
    return


@app.cell
def __(all_feature_columns, logistic_regression_classifier, pl):
    import altair as alt

    # Convert the set to a list to maintain order
    all_feature_columns_list = list(all_feature_columns)


    # Create a DataFrame with the features and their coefficients
    feature_coefficients_df = pl.DataFrame(
        {
            "feature": all_feature_columns_list,
            "coefficient": logistic_regression_classifier.coef_[0][:len(all_feature_columns_list)],
        }
    )

    # Sort the DataFrame by coefficient in descending order
    sorted_feature_coefficients_df = feature_coefficients_df.sort("coefficient", descending=True)

    # Plot the bar chart
    alt.Chart(sorted_feature_coefficients_df.to_pandas()).mark_bar().encode(
        x="coefficient",
        y=alt.Y("feature", sort="-x")
    ).properties(
        width=500,
        height=300,
    ).display()
    return (
        all_feature_columns_list,
        alt,
        feature_coefficients_df,
        sorted_feature_coefficients_df,
    )


@app.cell
def __(logistic_regression_classifier):
    logistic_regression_classifier.coef_
    return


@app.cell
def __(pipeline, scaled_train_df):
    # Make predictions on the test data
    predictions = pipeline.named_steps['classifier'].predict(scaled_train_df)

    # Print the predictions
    print(predictions)
    return (predictions,)


@app.cell
def __(
    pb_achieved_feature_test_df_pandas,
    pb_achieved_feature_train_df_pandas,
    pb_achieved_target_test_df_pandas,
    pb_achieved_target_train_df_pandas,
    scaled_train_df,
    validate_features_vs_target,
):
    validate_features_vs_target(pb_achieved_feature_train_df_pandas, pb_achieved_target_train_df_pandas)
    validate_features_vs_target(scaled_train_df, pb_achieved_target_train_df_pandas)

    validate_features_vs_target(pb_achieved_feature_test_df_pandas, pb_achieved_target_test_df_pandas)
    return


@app.cell
def __(mo):
    mo.md(
        r"""

        """
    )
    return


app._unparsable_cell(
    r"""
    > What are the probabilities that each of the observations in the test dataset have been assigned to the classes?
    """,
    name="__"
)


@app.cell
def __(logistic_regression_classifier, scaled_test_df):
    logistic_regression_classifier.predict_proba(scaled_test_df)
    return


@app.cell
def __(logistic_regression_classifier, scaled_test_df):
    logistic_regression_classifier.predict(scaled_test_df)
    return


@app.cell
def __(mo):
    mo.md(
        r"""


        ```
        ValueError: Input X contains NaN.
        LogisticRegression does not accept missing values encoded as NaN natively. For supervised learning, you might want to consider sklearn.ensemble.HistGradientBoostingClassifier and Regressor which accept missing values encoded as NaNs natively. Alternatively, it is possible to preprocess the data, for instance by using an imputer transformer in a pipeline or drop samples with missing values. See https://scikit-learn.org/stable/modules/impute.html You can find a list of all estimators that handle NaN values at the following page: https://scikit-learn.org/stable/modules/impute.html#estimators-that-handle-nan-values
        ```
        """
    )
    return


@app.cell
def __(
    logistic_regression_classifier,
    pb_achieved_target_test_df,
    scaled_test_df,
    validate_features_vs_target,
):
    from sklearn.metrics import classification_report

    validate_features_vs_target(scaled_test_df, pb_achieved_target_test_df)


    print(
        classification_report(
            pb_achieved_target_test_df.get_column("is_pb"),
            logistic_regression_classifier.predict(scaled_test_df),
        )
    )
    return (classification_report,)


@app.cell
def __(
    SimpleImputer,
    classification_report,
    logistic_regression_classifier,
    pb_achieved_feature_test_scaled_df,
    pb_achieved_feature_train_scaled_df,
    pb_achieved_target_test_df_pandas,
    pb_achieved_target_train_df_pandas,
    validate_features_vs_target,
):
    imputer = SimpleImputer(strategy='mean')
    validate_features_vs_target(pb_achieved_feature_train_scaled_df, pb_achieved_feature_test_scaled_df)
    pb_achieved_feature_train_scaled_df_1 = imputer.fit_transform(pb_achieved_feature_train_scaled_df)
    pb_achieved_feature_test_scaled_df_1 = imputer.transform(pb_achieved_feature_test_scaled_df)
    logistic_regression_classifier.fit(pb_achieved_feature_train_scaled_df_1, pb_achieved_target_train_df_pandas['is_pb'])
    print(classification_report(pb_achieved_target_test_df_pandas['is_pb'], logistic_regression_classifier.predict(pb_achieved_feature_test_scaled_df_1)))
    return (
        imputer,
        pb_achieved_feature_test_scaled_df_1,
        pb_achieved_feature_train_scaled_df_1,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Before we did this 

        ```
        logistic_regression_classifier = run_pipeline_in_stages(
            pb_achieved_feature_train_df_pandas,
            pb_achieved_target_train_df_pandas)
        ```

        """
    )
    return


@app.cell
def __(
    pb_achieved_feature_test_df_pandas,
    pb_achieved_target_test_df_pandas,
    run_pipeline_in_stages,
):
    logistic_regression_classifier_test = run_pipeline_in_stages(
        pb_achieved_feature_test_df_pandas,
        pb_achieved_target_test_df_pandas)
    return (logistic_regression_classifier_test,)


@app.cell
def __(
    classification_report,
    logistic_regression_classifier_test,
    pb_achieved_feature_test_scaled_df_1,
    pb_achieved_target_test_df_pandas,
):
    print(classification_report(pb_achieved_target_test_df_pandas['is_pb'], logistic_regression_classifier_test.predict(pb_achieved_feature_test_scaled_df_1)))
    return


@app.cell
def __(mo):
    mo.md(
        r"""

        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Interpreting Results from the Classification Report

        The classification report provides a summary of performance metrics for a classification model. Below is the detailed breakdown and interpretation:

        ### Definitions
        1. **Precision**: The ratio of true positives to total predicted positives. Indicates how many of the predicted "True" labels are actually "True."
           \[
           \text{Precision} = \frac{\text{True Positives}}{\text{True Positives + False Positives}}
           \]

        2. **Recall (Sensitivity)**: The ratio of true positives to total actual positives. Measures the ability of the classifier to identify all "True" instances.
           \[
           \text{Recall} = \frac{\text{True Positives}}{\text{True Positives + False Negatives}}
           \]

        3. **F1-Score**: The harmonic mean of precision and recall, balancing their trade-off.
           \[
           \text{F1-Score} = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision + Recall}}
           \]

        4. **Support**: The number of actual instances in each class.

        ---

        ### Interpreting the Results

        #### **Class: False (Negative Class)**
        - **Precision**: `0.74`  
           - 74% of the predictions for "False" were correct.
        - **Recall**: `0.88`  
           - 88% of the actual "False" cases were correctly identified by the model.
        - **F1-Score**: `0.80`  
           - A strong balance between precision and recall for this class.
        - **Support**: `4468`  
           - There are 4468 instances of "False" in the dataset.

        #### **Class: True (Positive Class)**
        - **Precision**: `0.62`  
           - 62% of the predictions for "True" were correct.
        - **Recall**: `0.38`  
           - Only 38% of the actual "True" cases were correctly identified.
        - **F1-Score**: `0.47`  
           - A relatively low score, indicating that the model struggles with this class.
        - **Support**: `2265`  
           - There are 2265 instances of "True" in the dataset.

        ---

        ### Overall Metrics
        - **Accuracy**: `0.71`  
           - The model correctly classified 71% of all instances.
        - **Macro Average**:
           - **Precision**: `0.68`  
           - **Recall**: `0.63`  
           - **F1-Score**: `0.64`  
           - These averages give equal weight to both classes, regardless of support.
        - **Weighted Average**:
           - **Precision**: `0.70`  
           - **Recall**: `0.71`  
           - **F1-Score**: `0.69`  
           - These averages take into account the support of each class, so the "False" class has more influence due to its larger support.

        ---

        ### Insights
        1. **Class Imbalance**:  
           - There is a class imbalance, with more "False" instances (`4468`) than "True" (`2265`). This likely affects the model's ability to detect the minority class ("True").

        2. **Performance on "True" Class**:
           - The model struggles to correctly identify the "True" class (low recall of `0.38`). This might indicate a need for techniques to handle class imbalance, such as oversampling, undersampling, or class weighting.

        3. **Overall Performance**:
           - While the model performs reasonably well on the majority class ("False"), its performance on the minority class ("True") drags down the overall metrics.

        ---

        ### Recommendations
        1. **Address Class Imbalance**:  
           - Consider using techniques like SMOTE, ADASYN, or class weighting in the logistic regression model to improve recall for the "True" class.

        2. **Threshold Tuning**:  
           - Experiment with adjusting the decision threshold of the model to better balance precision and recall.

        3. **Model Complexity**:  
           - Consider using a more complex model (e.g., ensemble methods like Random Forest or Gradient Boosting) if the dataset supports it.

        4. **Feature Engineering**:  
           - Investigate additional features or transformations to enhance separability between the classes.

        ---

        """
    )
    return


@app.cell
def __(pb_achieved_feature_test_scaled_df_1):
    filtered_df = pb_achieved_feature_test_scaled_df_1.dropna()
    print(filtered_df)
    return (filtered_df,)


@app.cell
def __():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()

