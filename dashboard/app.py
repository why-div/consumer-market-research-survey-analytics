import streamlit as st
import pandas as pd
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data" / "cleaned_survey_data.csv"

st.set_page_config(
    page_title="Consumer Market Research",
    layout="wide"
)

df = pd.read_csv(DATA)


st.title("Consumer Market Research & Survey Analytics")
st.caption(
    "Synthetic survey dataset — portfolio project; responses are simulated."
)


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Valid Respondents",
    f"{len(df):,}"
)

c2.metric(
    "Avg. Satisfaction",
    f"{df['overall_satisfaction'].mean():.2f}/5"
)

c3.metric(
    "Avg. Repeat Intent",
    f"{df['repeat_purchase_intent'].mean():.2f}/5"
)

c4.metric(
    "Avg. Recommendation",
    f"{df['recommendation_score'].mean():.1f}/10"
)

st.divider()


st.subheader("Platform Comparison")

platform = (
    df.groupby("preferred_platform")
      .agg(
          Respondents=("response_id", "count"),
          Satisfaction=("overall_satisfaction", "mean"),
          RepeatIntent=("repeat_purchase_intent", "mean"),
          Recommendation=("recommendation_score", "mean")
      )
      .round(2)
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Average Satisfaction by Platform**")

    platform_chart = (
        platform[["Satisfaction"]]
        .sort_values("Satisfaction", ascending=False)
    )

    st.bar_chart(platform_chart)

with col2:
    st.markdown("**Platform Summary**")

    st.dataframe(
        platform,
        use_container_width=True
    )


st.subheader("Shopping Frequency")

freq = (
    df.groupby("shopping_frequency")
      .agg(
          Respondents=("response_id", "count"),
          Satisfaction=("overall_satisfaction", "mean"),
          MonthlySpend=("monthly_online_spend_inr", "mean"),
          SwitchingIntent=("switching_intent", "mean")
      )
      .round(2)
)

st.dataframe(
    freq,
    use_container_width=True
)


st.subheader("Satisfaction Driver Relationships")

drivers = [
    "delivery_satisfaction",
    "product_quality",
    "reviews_importance",
    "return_experience",
    "customer_support",
    "price_sensitivity",
    "discount_importance"
]

corr = (
    df[drivers + ["overall_satisfaction"]]
    .corr()["overall_satisfaction"]
    .drop("overall_satisfaction")
    .sort_values(ascending=False)
)

corr_df = corr.reset_index()

corr_df.columns = [
    "Driver",
    "Correlation"
]

corr_df["Driver"] = corr_df["Driver"].str.replace(
    "_", " ", regex=False
).str.title()

st.bar_chart(
    corr_df.set_index("Driver")
)

st.caption(
    "Correlation indicates association with overall satisfaction; "
    "it does not establish causation."
)


st.subheader("Customer Segment View")

age = (
    df.groupby("age_group")
      .agg(
          Respondents=("response_id", "count"),
          Satisfaction=("overall_satisfaction", "mean"),
          SwitchingIntent=("switching_intent", "mean")
      )
      .round(2)
)

st.dataframe(
    age,
    use_container_width=True
)

st.subheader("Key Simulated Insights")

overall_corr = (
    df["overall_satisfaction"]
    .corr(df["repeat_purchase_intent"])
)

delivery_corr = (
    df["overall_satisfaction"]
    .corr(df["delivery_satisfaction"])
)

quality_corr = (
    df["overall_satisfaction"]
    .corr(df["product_quality"])
)

switching_corr = (
    df["overall_satisfaction"]
    .corr(df["switching_intent"])
)

st.markdown(
    f"""
- **Repeat purchase intent:** Overall satisfaction has a positive
  association with repeat purchase intent (**r = {overall_corr:.2f}**).

- **Delivery experience:** Delivery satisfaction shows a positive
  association with overall satisfaction (**r = {delivery_corr:.2f}**).

- **Product quality:** Product quality is also positively associated
  with overall satisfaction (**r = {quality_corr:.2f}**).

- **Switching behaviour:** Switching intent shows a negative association
  with overall satisfaction (**r = {switching_corr:.2f}**).
"""
)


st.info(
    "Interpret findings as simulated market-research insights, "
    "not real consumer statistics."
)