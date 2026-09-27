import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
raw_path = BASE / "data" / "raw_survey_data.csv"
out_path = BASE / "data" / "cleaned_survey_data.csv"
report_path = BASE / "data" / "quality_report.csv"

df = pd.read_csv(raw_path)
initial_rows = len(df)

# Duplicate response IDs
duplicate_mask = df.duplicated(subset=["response_id"], keep="first")
duplicate_count = int(duplicate_mask.sum())

# Range validation
likert_cols = [
    "price_sensitivity","discount_importance","delivery_satisfaction",
    "product_quality","reviews_importance","return_experience",
    "customer_support","overall_satisfaction","repeat_purchase_intent",
    "switching_intent"
]
invalid_mask = pd.Series(False, index=df.index)
for c in likert_cols:
    invalid_mask |= ~df[c].isna() & ~df[c].between(1,5)

invalid_recommend = ~df["recommendation_score"].isna() & ~df["recommendation_score"].between(0,10)
invalid_count = int((invalid_mask | invalid_recommend).sum())

# Straight-line detection
straight_line_cols = [
    "price_sensitivity","discount_importance","delivery_satisfaction",
    "product_quality","reviews_importance","return_experience","customer_support"
]
straight_line_mask = df[straight_line_cols].nunique(axis=1) == 1
straight_line_count = int(straight_line_mask.sum())

# Fast completion: threshold chosen as a screening rule for this synthetic project
fast_mask = df["completion_time_sec"] < 60
fast_count = int(fast_mask.sum())

# Remove duplicate IDs, invalid records, and straight-line responses.
clean = df.loc[~duplicate_mask].copy()
clean = clean.loc[~invalid_mask].copy()
clean = clean.loc[~invalid_recommend].copy()
clean = clean.loc[~straight_line_mask].copy()

missing_before = int(df.isna().sum().sum())

# Median imputation for numeric survey scores; mode for categorical fields.
for c in likert_cols + ["recommendation_score"]:
    clean[c] = clean[c].fillna(clean[c].median())

for c in ["income_range"]:
    clean[c] = clean[c].fillna(clean[c].mode()[0])

clean.to_csv(out_path, index=False)

report = pd.DataFrame({
    "metric": [
        "raw_rows","duplicate_rows","invalid_rows","straight_line_rows",
        "fast_completion_flags","missing_cells_before_cleaning","clean_rows_removed","final_rows"
    ],
    "value": [
        initial_rows, duplicate_count, invalid_count, straight_line_count,
        fast_count, missing_before, initial_rows-len(clean), len(clean)
    ]
})
report.to_csv(report_path, index=False)

print(report.to_string(index=False))
print(f"\nSaved: {out_path}")
