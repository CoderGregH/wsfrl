import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler



def run_logistic_regression_pipeline_in_stages(df_feature: pd.DataFrame, df_target: pd.DataFrame, target_column: str) -> tuple:
    # Transform the test data using the preprocessor part of the pipeline
    preprocessed_df = pipeline.named_steps['preprocessor'].transform(df_feature)

    # Scale the preprocessed test data
    scaled_df = pipeline.named_steps['scaler'].transform(preprocessed_df)

    classifier = LogisticRegression(penalty=None)

    classifier.fit(
        scaled_df,
        df_target[target_column],
    )

    return scaled_df, classifier