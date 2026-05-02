# Data Dictionary

## Source: IBM HR Analytics Employee Attrition Dataset

**Original file:** `WA_Fn-UseC_-HR-Employee-Attrition.csv`
**Source:** Kaggle / IBM Watson Analytics
**Rows:** 1,470  **Columns:** 35 (raw) → 32 after removing constants

---

## Raw Columns (Bronze Layer)

| Column | Type | Range / Values | Description |
|---|---|---|---|
| Age | int | 18–60 | Employee age in years |
| Attrition | str | Yes / No | **Target variable** — whether employee left |
| BusinessTravel | str | Non-Travel, Travel_Rarely, Travel_Frequently | Travel frequency for work |
| DailyRate | int | 102–1499 | Daily pay rate (USD) |
| Department | str | Human Resources, Research & Development, Sales | Department |
| DistanceFromHome | int | 1–29 | Miles from home to office |
| Education | int | 1–5 | 1=Below College, 2=College, 3=Bachelor, 4=Master, 5=Doctor |
| EducationField | str | HR, Life Sciences, Marketing, Medical, Other, Technical Degree | Field of study |
| EmployeeCount | int | 1 (constant) | **Removed in Silver** — zero-variance |
| EmployeeNumber | int | 1–2068 | Unique employee identifier |
| EnvironmentSatisfaction | int | 1–4 | 1=Low, 2=Medium, 3=High, 4=Very High |
| Gender | str | Male / Female | Gender |
| HourlyRate | int | 30–100 | Hourly pay rate (USD) |
| JobInvolvement | int | 1–4 | 1=Low, 2=Medium, 3=High, 4=Very High |
| JobLevel | int | 1–5 | Seniority level (1=entry, 5=executive) |
| JobRole | str | 9 roles | See role list below |
| JobSatisfaction | int | 1–4 | 1=Low, 2=Medium, 3=High, 4=Very High |
| MaritalStatus | str | Single, Married, Divorced | Marital status |
| MonthlyIncome | int | 1009–19999 | Monthly gross income (USD) |
| MonthlyRate | int | 2094–26999 | Monthly rate (not same as income) |
| NumCompaniesWorked | int | 0–9 | Prior employers count |
| Over18 | str | Y (constant) | **Removed in Silver** — zero-variance |
| OverTime | str | Yes / No | Currently working overtime |
| PercentSalaryHike | int | 11–25 | Last salary hike percentage |
| PerformanceRating | int | 3–4 | 3=Excellent, 4=Outstanding |
| RelationshipSatisfaction | int | 1–4 | 1=Low, 2=Medium, 3=High, 4=Very High |
| StandardHours | int | 80 (constant) | **Removed in Silver** — zero-variance |
| StockOptionLevel | int | 0–3 | 0=None, 1=Low, 2=Medium, 3=High |
| TotalWorkingYears | int | 0–40 | Total career experience |
| TrainingTimesLastYear | int | 0–6 | Training sessions attended last year |
| WorkLifeBalance | int | 1–4 | 1=Bad, 2=Good, 3=Better, 4=Best |
| YearsAtCompany | int | 0–40 | Tenure at current company |
| YearsInCurrentRole | int | 0–18 | Years in current role |
| YearsSinceLastPromotion | int | 0–15 | Years since last promotion |
| YearsWithCurrManager | int | 0–17 | Years with current manager |

**Job Roles:**
Healthcare Representative, Human Resources, Laboratory Technician,
Manager, Manufacturing Director, Research Director, Research Scientist,
Sales Executive, Sales Representative

---

## Engineered Columns (Silver Layer — added)

| Column | Formula | Interpretation |
|---|---|---|
| SatisfactionComposite | mean(EnvSat, JobSat, RelSat, WLB) | Overall satisfaction index (1–4) |
| YearsPerCompany | TotalWorkingYears / NumCompaniesWorked | Avg tenure per employer; low = job-hopper |
| IncomeVsLevelMedian | (Income − LevelMedian) / LevelMedian | Salary position relative to job-level peers |
| PromotionLag | YearsSinceLastPromotion / YearsAtCompany | Stagnation ratio; high = long time without promotion |
| ManagerTenureRatio | YearsWithCurrManager / YearsAtCompany | Manager stability; high = loyal relationship |
| DistanceTier | cut(DistanceFromHome, [0,5,10,20,∞]) | Near / Moderate / Far / Very Far |
| AgeBand | cut(Age, [17,25,35,45,55,∞]) | 18-25 / 26-35 / 36-45 / 46-55 / 55+ |

---

## Gold Tables (data/exports/)

| File | Key Columns | Primary Use |
|---|---|---|
| attrition_by_department.csv | Department, AttritionRate, OvertimeRate | Department-level bar charts |
| attrition_by_role.csv | JobRole, AttritionRate, AvgSatisfactionComposite | Role risk ranking |
| attrition_by_demographics.csv | Dimension, DimensionValue, AttritionRate | Demographic slicers |
| satisfaction_analysis.csv | SatisfactionDimension, Score, AttritionRate | Satisfaction trend lines |
| salary_analysis.csv | JobLevel, JobRole, MedianIncome, AttritionRate | Compensation analysis |
| tenure_analysis.csv | YearsAtCompany, AttritionRate, AvgYearsSincePromotion | Tenure curve |
| overtime_impact.csv | OverTime, JobSatisfaction, AttritionRate | OT interaction heat map |
| risk_scores.csv | EmployeeNumber, FlightRiskScore, RiskBand | Individual risk table |
| executive_summary.csv | Metric, Value | KPI cards |
