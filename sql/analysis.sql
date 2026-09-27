-- Consumer Market Research SQL analysis
-- Load cleaned_survey_data.csv into a table named survey_responses.

-- 1. Respondent count by platform
SELECT preferred_platform, COUNT(*) AS respondents
FROM survey_responses
GROUP BY preferred_platform
ORDER BY respondents DESC;

-- 2. Satisfaction by platform
SELECT preferred_platform,
       COUNT(*) AS respondents,
       ROUND(AVG(overall_satisfaction), 2) AS avg_satisfaction,
       ROUND(AVG(repeat_purchase_intent), 2) AS avg_repeat_intent,
       ROUND(AVG(recommendation_score), 2) AS avg_recommendation
FROM survey_responses
GROUP BY preferred_platform
ORDER BY avg_satisfaction DESC;

-- 3. Satisfaction by shopping frequency
SELECT shopping_frequency,
       COUNT(*) AS respondents,
       ROUND(AVG(overall_satisfaction), 2) AS avg_satisfaction,
       ROUND(AVG(monthly_online_spend_inr), 0) AS avg_monthly_spend
FROM survey_responses
GROUP BY shopping_frequency
ORDER BY avg_satisfaction DESC;

-- 4. Customer segment summary
SELECT age_group, income_range,
       COUNT(*) AS respondents,
       ROUND(AVG(overall_satisfaction), 2) AS avg_satisfaction,
       ROUND(AVG(switching_intent), 2) AS avg_switching_intent
FROM survey_responses
GROUP BY age_group, income_range
ORDER BY respondents DESC;

-- 5. High-risk customers: low satisfaction + high switching intent
SELECT COUNT(*) AS high_risk_customers
FROM survey_responses
WHERE overall_satisfaction <= 2
  AND switching_intent >= 4;
