from sklearn.pipeline import Pipeline

# from feature-engine
from feature_engine.imputation import MeanMedianImputer,AddMissingIndicator
from feature_engine.selection import DropFeatures
from sklearn.naive_bayes import GaussianNB
from model.config.core import config

pipe = Pipeline([

    # ===== IMPUTATION =====
    (
        "drop_features",
        DropFeatures(features_to_drop=config.model_config.drop_features),
    ),
    (
        "missing_indicator",
        AddMissingIndicator(variables=config.model_config.numerical_vars_with_na),
    ),
    # impute numerical variables with the mean
    (
        "mean_imputation",
        MeanMedianImputer(
            imputation_method="mean",
            variables=config.model_config.numerical_vars_with_na,
        ),
    ),
    ('GaussianNB', GaussianNB())
   
   ])