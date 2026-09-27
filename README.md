# Consumer Market Research & Survey Analytics

## Important
This portfolio project uses **synthetic survey data**. No real respondents were surveyed. The dataset is designed to demonstrate an end-to-end primary-market-research workflow.

## Objective
Analyze e-commerce consumer behavior and identify factors associated with satisfaction, repeat purchase intention, and switching intent.

## Workflow
1. Synthetic questionnaire response generation
2. Data-quality checks
3. Cleaning and validation
4. SQL tabulation
5. Quantitative analysis in Python
6. Excel reporting
7. Streamlit dashboard
8. PowerPoint research report

## Tech
Python, Pandas, NumPy, SQL, Excel, Plotly/Streamlit, PowerPoint

## Run
```bash
pip install -r requirements.txt
python analysis/clean_and_validate.py
streamlit run dashboard/app.py
```

## Suggested interview explanation
"I built a synthetic primary-market-research pipeline to practice the complete workflow from survey responses through quality checking, cleaning, tabulation, quantitative analysis and reporting. I deliberately introduced common survey-quality issues such as duplicates, missing values, invalid responses and straight-lining, then created rules to flag and clean them before analysis."
