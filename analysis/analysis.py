import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("../data/cleaned_survey_data.csv")

# Basic profile
print(df.shape)
print(df.describe(include="all").T)

# Platform-level summary
platform_summary = (
    df.groupby("preferred_platform")
      .agg(
          respondents=("response_id","count"),
          avg_satisfaction=("overall_satisfaction","mean"),
          avg_repeat_intent=("repeat_purchase_intent","mean"),
          avg_recommendation=("recommendation_score","mean")
      )
      .round(2)
      .sort_values("avg_satisfaction", ascending=False)
)
print(platform_summary)

# Shopping frequency
freq_summary = (
    df.groupby("shopping_frequency")
      .agg(
          respondents=("response_id","count"),
          avg_satisfaction=("overall_satisfaction","mean"),
          avg_monthly_spend=("monthly_online_spend_inr","mean"),
          avg_switching_intent=("switching_intent","mean")
      )
      .round(2)
)
print(freq_summary)

# Driver correlations
driver_cols = [
    "price_sensitivity","discount_importance","delivery_satisfaction",
    "product_quality","reviews_importance","return_experience","customer_support",
    "overall_satisfaction","repeat_purchase_intent","switching_intent"
]
print(df[driver_cols].corr()["overall_satisfaction"].sort_values(ascending=False))

# Simple OLS-style regression if statsmodels is installed
try:
    import statsmodels.api as sm
    X = df[[
        "delivery_satisfaction","product_quality","reviews_importance",
        "return_experience","customer_support"
    ]]
    X = sm.add_constant(X)
    y = df["overall_satisfaction"]
    model = sm.OLS(y, X).fit()
    print(model.summary())
except ImportError:
    print("Install statsmodels to run the regression: pip install statsmodels")
