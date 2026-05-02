# Power BI Tables Dictionary

A plain-English reference for every table and column loaded into Power BI.
Use this as your field guide when building visuals or writing DAX.

---

## Table Index

| Table Name in Power BI | Source File | Rows | Purpose |
|---|---|---|---|
| `Employees` | employee_data.csv | 1,470 | Main fact table — one row per employee |
| `RiskScores` | risk_scores.csv | 1,470 | Flight risk score per employee |
| `AttritionByDept` | attrition_by_department.csv | 3 | Attrition KPIs rolled up by department |
| `AttritionByRole` | attrition_by_role.csv | 11 | Attrition KPIs by department + job role |
| `AttritionByDemographic` | attrition_by_demographics.csv | 18 | Attrition across age, marital status, education, distance |
| `SatisfactionAnalysis` | satisfaction_analysis.csv | 16 | How each satisfaction score level drives attrition |
| `SalaryAnalysis` | salary_analysis.csv | 26 | Income statistics by job level and role |
| `TenureAnalysis` | tenure_analysis.csv | 37 | Attrition and career patterns by years at company |
| `OvertimeImpact` | overtime_impact.csv | 8 | How overtime and job satisfaction interact on attrition |
| `ExecutiveSummary` | executive_summary.csv | 9 | Top-level KPI snapshot for headline cards |

---

## Employees
**Source:** `employee_data.csv` | **Rows:** 1,470 | **Grain:** One row per employee

This is the **main fact table**. Every other table is a pre-aggregated summary derived from this one.
Use `Employees` whenever you need individual-level filtering, drill-through, or custom DAX aggregations.

| Column | Type | Values / Range | What it means |
|---|---|---|---|
| `EmployeeNumber` | Whole Number | 1 – 2,068 | Unique employee ID. Use as the key for relationships and drill-through. |
| `Age` | Whole Number | 18 – 60 | Employee age in years. |
| `AgeBand` | Text | 18-25, 26-35, 36-45, 46-55, 55+ | Age grouped into 5 bands. Easier to use in slicers and bar charts than raw age. |
| `GenderLabel` | Text | Male, Female | Employee gender. (The raw `Gender` column was 1/0 — this is the readable version.) |
| `MaritalStatus` | Text | Single, Married, Divorced | Marital status. Single employees have ~2× higher attrition. |
| `Department` | Text | Sales, Research & Development, Human Resources | The department the employee belongs to. |
| `JobRole` | Text | 9 distinct roles | Specific job title. Sales Representative has the highest attrition (~40%). |
| `JobLevel` | Whole Number | 1 – 5 | Seniority level. 1 = entry-level, 5 = executive/director. |
| `BusinessTravel` | Text | Non-Travel, Travel_Rarely, Travel_Frequently | How often the employee travels for work. |
| `EducationField` | Text | Life Sciences, Medical, Marketing, Technical Degree, Human Resources, Other | The field the employee studied. |
| `Education` | Whole Number | 1 – 5 | Highest education level (numeric code). |
| `Education_Label` | Text | Below College, College, Bachelor, Master, Doctor | Human-readable version of Education. |
| `Attrition` | Text | Yes, No | **Target variable.** Whether the employee left the company. Use this in CALCULATE filters. |
| `OverTime` | Text | Yes, No | Whether the employee works overtime. Overtime employees leave at 3× the rate. |
| `MonthlyIncome` | Whole Number | $1,009 – $19,999 | Monthly gross salary in USD. |
| `DailyRate` | Whole Number | 102 – 1,499 | Daily pay rate. Different from monthly income — used in some compensation analyses. |
| `HourlyRate` | Whole Number | 30 – 100 | Hourly pay rate. |
| `MonthlyRate` | Whole Number | 2,094 – 26,999 | A separate rate figure. Not the same as take-home MonthlyIncome. |
| `PercentSalaryHike` | Whole Number | 11% – 25% | Last year's salary increase as a percentage. |
| `StockOptionLevel` | Whole Number | 0 – 3 | Stock option grant level. 0 = none, 3 = maximum. Level 1 has the lowest attrition. |
| `JobSatisfaction` | Whole Number | 1 – 4 | How satisfied the employee is with their job. 1 = Low, 4 = Very High. |
| `JobSatisfaction_Label` | Text | Low, Medium, High, Very High | Readable version of JobSatisfaction. |
| `EnvironmentSatisfaction` | Whole Number | 1 – 4 | Satisfaction with the physical/cultural work environment. 1 = Low, 4 = Very High. |
| `EnvironmentSatisfaction_Label` | Text | Low, Medium, High, Very High | Readable version of EnvironmentSatisfaction. |
| `RelationshipSatisfaction` | Whole Number | 1 – 4 | Satisfaction with relationships at work. 1 = Low, 4 = Very High. |
| `RelationshipSatisfaction_Label` | Text | Low, Medium, High, Very High | Readable version of RelationshipSatisfaction. |
| `WorkLifeBalance` | Whole Number | 1 – 4 | Self-rated work-life balance. 1 = Bad, 4 = Best. |
| `WorkLifeBalance_Label` | Text | Bad, Good, Better, Best | Readable version of WorkLifeBalance. |
| `JobInvolvement` | Whole Number | 1 – 4 | How involved/engaged the employee feels in their work. |
| `JobInvolvement_Label` | Text | Low, Medium, High, Very High | Readable version of JobInvolvement. |
| `PerformanceRating` | Whole Number | 3 – 4 | Last performance review rating. 3 = Excellent, 4 = Outstanding. (No 1 or 2 in this dataset.) |
| `PerformanceRating_Label` | Text | Excellent, Outstanding | Readable version of PerformanceRating. |
| `SatisfactionComposite` | Decimal | 1.0 – 4.0 | Average of all 4 satisfaction scores (Job + Environment + Relationship + WLB). A single number capturing overall employee wellbeing. The closer to 1, the higher the attrition risk. |
| `YearsAtCompany` | Whole Number | 0 – 40 | Total tenure at the current company. Peak attrition risk is years 1–3 and again at 5–8. |
| `YearsInCurrentRole` | Whole Number | 0 – 18 | How long in the current role (not total company tenure). |
| `YearsSinceLastPromotion` | Whole Number | 0 – 15 | Years since the last promotion. Employees at 4+ years with no promotion have 1.8× higher attrition. |
| `YearsWithCurrManager` | Whole Number | 0 – 17 | Years working under the current manager. Higher values = greater manager loyalty = lower attrition. |
| `TotalWorkingYears` | Whole Number | 0 – 40 | Total career experience across all employers. |
| `NumCompaniesWorked` | Whole Number | 0 – 9 | Number of different employers before this one. High values indicate a job-hopper profile. |
| `TrainingTimesLastYear` | Whole Number | 0 – 6 | Number of training sessions attended last year. |
| `DistanceFromHome` | Whole Number | 1 – 29 | Miles from the employee's home to the office. |
| `DistanceTier` | Text | Near, Moderate, Far, Very Far | DistanceFromHome grouped into 4 bands: Near (≤5), Moderate (6–10), Far (11–20), Very Far (>20). |
| `IncomeVsLevelMedian` | Decimal | -0.62 – +0.87 | How far the employee's income is from the median for their job level. Negative = underpaid vs peers. Positive = above peers. Key salary fairness indicator. |
| `PromotionLag` | Decimal | 0.0 – 1.0 | YearsSinceLastPromotion ÷ YearsAtCompany. High values = long time without a promotion relative to tenure. A stagnation signal. |
| `ManagerTenureRatio` | Decimal | 0.0 – 1.0 | YearsWithCurrManager ÷ YearsAtCompany. High values = employee has stayed with the same manager most of their tenure. Correlates with lower attrition. |
| `YearsPerCompany` | Decimal | 0.0 – 40.0 | TotalWorkingYears ÷ NumCompaniesWorked. Average years spent at each employer. Low = frequent job changes. |
| `FlightRiskScore` | Decimal | 0.11 – 0.89 | Composite weighted risk score (0 = lowest risk, 1 = highest). Combines overtime, satisfaction, promotion lag, distance, income, marital status, and tenure. |
| `RiskBand` | Text | Low, Moderate, High, Critical | FlightRiskScore grouped into 4 bands. Low = 0–0.30, Moderate = 0.30–0.50, High = 0.50–0.70, Critical = 0.70+. Use for conditional formatting and slicer filtering. |

---

## RiskScores
**Source:** `risk_scores.csv` | **Rows:** 1,470 | **Grain:** One row per employee

A lean version of the employee data focused purely on risk scoring.
Use this table for the **Flight Risk Register** table visual and the risk donut chart.
It has fewer columns than `Employees` so it's faster to render in large visuals.

| Column | Type | Values / Range | What it means |
|---|---|---|---|
| `EmployeeNumber` | Whole Number | 1 – 2,068 | Unique employee ID. Links to `Employees`. |
| `JobRole` | Text | 9 roles | Employee's job role. |
| `Department` | Text | 3 departments | Employee's department. |
| `MonthlyIncome` | Whole Number | $1,009 – $19,999 | Monthly salary. |
| `YearsAtCompany` | Whole Number | 0 – 40 | Tenure in years. |
| `FlightRiskScore` | Decimal | 0.11 – 0.89 | Composite risk score. Sort descending to find highest-risk employees. |
| `RiskBand` | Text | Low, Moderate, High, Critical | Risk category. Apply red/amber/green conditional formatting to this column. |
| `Attrition` | Whole Number | 0, 1 | Whether the employee actually left (1 = left, 0 = stayed). Use to validate how well risk scores predict actual outcomes. |

---

## AttritionByDept
**Source:** `attrition_by_department.csv` | **Rows:** 3 | **Grain:** One row per department

Pre-aggregated department summary. Use this for department-level bar charts and KPI comparisons.
Faster to render than aggregating `Employees` at report time.

| Column | Type | Values / Range | What it means |
|---|---|---|---|
| `Department` | Text | Sales, R&D, Human Resources | Department name. Use as the axis on bar/column charts. |
| `TotalEmployees` | Whole Number | 63 – 961 | Total headcount in this department. |
| `AttritionCount` | Whole Number | 12 – 133 | Number of employees who left. |
| `AttritionRate` | Decimal | 0.14 – 0.21 | Proportion who left. Format as % in Power BI. |
| `AvgMonthlyIncome` | Decimal | $6,281 – $6,959 | Average monthly salary in this department. |
| `AvgJobSatisfaction` | Decimal | 2.60 – 2.75 | Average job satisfaction score (1–4 scale). |
| `AvgYearsAtCompany` | Decimal | 6.9 – 7.3 | Average employee tenure in years. |
| `OvertimeRate` | Decimal | 0.27 – 0.29 | Proportion of employees working overtime. Format as %. |

---

## AttritionByRole
**Source:** `attrition_by_role.csv` | **Rows:** 11 | **Grain:** One row per department × job role

Department and role breakdown. Use for horizontal bar charts sorted by AttritionRate.
Reveals which specific roles drive departmental attrition.

| Column | Type | Values / Range | What it means |
|---|---|---|---|
| `Department` | Text | 3 departments | Department this role belongs to. |
| `JobRole` | Text | 9 roles | Job role name. |
| `TotalEmployees` | Whole Number | 11 – 326 | Headcount in this role. |
| `AttritionCount` | Whole Number | 0 – 62 | Number who left from this role. |
| `AttritionRate` | Decimal | 0.00 – 0.40 | Proportion who left. Sales Representative is highest (~40%). |
| `AvgMonthlyIncome` | Decimal | $2,626 – $18,089 | Average monthly salary for this role. |
| `AvgJobLevel` | Decimal | 1.1 – 4.6 | Average seniority level within this role (1–5 scale). |
| `AvgSatisfactionComposite` | Decimal | 2.69 – 2.84 | Average composite satisfaction score for this role. |

---

## AttritionByDemographic
**Source:** `attrition_by_demographics.csv` | **Rows:** 18 | **Grain:** One row per dimension value

Attrition rates across four demographic dimensions in a single tall table.
The `Dimension` column tells you which grouping each row belongs to.
Use a slicer on `Dimension` to switch between views.

| Column | Type | Values / Range | What it means |
|---|---|---|---|
| `Dimension` | Text | AgeBand, MaritalStatus, EducationField, DistanceTier | Which demographic grouping this row represents. Filter or use as a slicer. |
| `DimensionValue` | Text | e.g. "Single", "26-35", "Far" | The specific value within that dimension (e.g. a specific age band or marital status). |
| `TotalEmployees` | Whole Number | 27 – 673 | Headcount for this group. |
| `AttritionCount` | Whole Number | 7 – 120 | Number who left from this group. |
| `AttritionRate` | Decimal | 0.09 – 0.36 | Proportion who left. Format as %. |

**Example use:** Filter `Dimension = "MaritalStatus"` → bar chart of `DimensionValue` vs `AttritionRate` → shows Single (25%) vs Married (12%) vs Divorced (10%).

---

## SatisfactionAnalysis
**Source:** `satisfaction_analysis.csv` | **Rows:** 16 | **Grain:** One row per satisfaction dimension × score level

Shows how each score level (1–4) within each satisfaction dimension maps to attrition rate.
Use for line charts to show the "as satisfaction falls, attrition rises" trend.

| Column | Type | Values / Range | What it means |
|---|---|---|---|
| `SatisfactionDimension` | Text | EnvironmentSatisfaction, JobSatisfaction, RelationshipSatisfaction, WorkLifeBalance | Which satisfaction dimension this row belongs to. Use as legend on a multi-line chart. |
| `Score` | Whole Number | 1 – 4 | The satisfaction score level. 1 = Low / Bad, 4 = Very High / Best. Use as the X-axis. |
| `TotalEmployees` | Whole Number | 80 – 893 | Number of employees with this score. |
| `AttritionRate` | Decimal | 0.11 – 0.31 | Attrition rate for employees at this score level. Higher scores = lower attrition. |

**Example use:** Line chart — X = Score, Y = AttritionRate, Legend = SatisfactionDimension → one line per dimension showing how satisfaction drives departures.

---

## SalaryAnalysis
**Source:** `salary_analysis.csv` | **Rows:** 26 | **Grain:** One row per job level × job role

Income statistics and attrition rates broken down by seniority and role.
Use for compensation analysis — spotting underpaid roles and income compression.

| Column | Type | Values / Range | What it means |
|---|---|---|---|
| `JobLevel` | Whole Number | 1 – 5 | Seniority level. 1 = entry, 5 = executive. |
| `JobRole` | Text | 9 roles | Job role. Not all levels exist for every role — some combinations are blank. |
| `TotalEmployees` | Whole Number | 1 – 234 | Headcount for this level + role combination. |
| `MinIncome` | Whole Number | $1,009 – $18,172 | Lowest salary in this group. |
| `MedianIncome` | Decimal | $2,553 – $19,287 | Middle salary. More reliable than mean for skewed distributions. |
| `MeanIncome` | Decimal | $2,507 – $19,205 | Average salary. |
| `MaxIncome` | Whole Number | $4,400 – $19,999 | Highest salary in this group. |
| `AttritionRate` | Decimal | 0.00 – 0.42 | Proportion who left from this group. High values signal underpaid or high-pressure roles. |
| `AvgIncomeVsLevelMedian` | Decimal | -0.40 – +0.27 | How far average income for this role deviates from the overall median for that job level. **Negative = underpaid vs peers. Positive = above peers.** Apply red/green diverging conditional formatting to this column. |

---

## TenureAnalysis
**Source:** `tenure_analysis.csv` | **Rows:** 37 | **Grain:** One row per year of tenure (0–40)

Year-by-year attrition and career metrics. The source of the "Dual-Crisis Curve" chart.
Use for area/line charts with YearsAtCompany on the X-axis.

| Column | Type | Values / Range | What it means |
|---|---|---|---|
| `YearsAtCompany` | Whole Number | 0 – 40 | Years of tenure. Use as the X-axis on the tenure curve chart. |
| `TotalEmployees` | Whole Number | 1 – 196 | Headcount at each tenure milestone. Low counts at high years (40+) mean those data points are less statistically reliable. |
| `AttritionCount` | Whole Number | 0 – 59 | Number who left at this tenure year. |
| `AttritionRate` | Decimal | 0.00 – 1.00 | Proportion who left. Peak at year 1–3 (onboarding failure) and again at year 5–8 (career plateau). |
| `AvgYearsSincePromotion` | Decimal | 0.0 – 15.0 | Average time since last promotion for employees at this tenure level. Rising values = stagnation accumulating over time. |
| `AvgManagerTenureRatio` | Decimal | 0.0 – 0.87 | Average manager stability at this tenure level. Low values at early tenure = new hires frequently change managers. |

---

## OvertimeImpact
**Source:** `overtime_impact.csv` | **Rows:** 8 | **Grain:** One row per overtime status × job satisfaction score

The interaction between overtime and satisfaction. 8 rows = 2 (Yes/No) × 4 (score levels).
Use as a heatmap matrix — the strongest two-factor attrition predictor in the dataset.

| Column | Type | Values / Range | What it means |
|---|---|---|---|
| `OverTime` | Text | Yes, No | Whether employees in this group work overtime. |
| `JobSatisfaction` | Whole Number | 1 – 4 | Job satisfaction score level. 1 = Low, 4 = Very High. |
| `TotalEmployees` | Whole Number | 69 – 321 | Headcount for this overtime + satisfaction combination. |
| `AttritionRate` | Decimal | 0.07 – 0.38 | Attrition rate for this combination. **OverTime=Yes + JobSatisfaction=1 is the highest-risk cell (~53%).** |
| `AvgMonthlyIncome` | Decimal | $6,411 – $6,620 | Average income for this group. Relatively flat — income alone doesn't explain the attrition difference. |

**Example use:** Matrix visual — Rows = OverTime, Columns = JobSatisfaction, Values = AttritionRate. Apply red-to-green conditional formatting. The top-left cell (Yes, Score=1) will be deep red.

---

## ExecutiveSummary
**Source:** `executive_summary.csv` | **Rows:** 9 | **Grain:** One row per KPI metric

Nine top-level numbers for headline cards. Regenerated every time the pipeline runs.
Use each row as a separate card visual using a LOOKUPVALUE DAX measure.

| Column | Type | Values | What it means |
|---|---|---|---|
| `Metric` | Text | See below | The name of the KPI. |
| `Value` | Decimal | Varies | The numeric value. Format each card differently based on its metric. |

**Rows and how to format them:**

| Metric | Value (example) | Format in Power BI |
|---|---|---|
| Total Employees | 1,470 | Whole Number, no decimals |
| Total Attrition Count | 237 | Whole Number, no decimals |
| Overall Attrition Rate | 0.1612 | Percentage, 1 decimal → 16.1% |
| Avg Monthly Income (USD) | 6,502.93 | Currency, 0 decimals → $6,503 |
| Avg Age | 36.9 | Decimal, 1 place → 36.9 |
| Avg Years at Company | 7.0 | Decimal, 1 place → 7.0 |
| Overtime Rate | 0.2830 | Percentage, 1 decimal → 28.3% |
| Avg Satisfaction Composite | 2.73 | Decimal, 2 places → 2.73 |
| High-Risk Employees (OT + Low Satisfaction) | 12 | Whole Number, no decimals |

**DAX to extract a single row:**
```dax
[Total Employees KPI] =
CALCULATE(
    SUM(ExecutiveSummary[Value]),
    ExecutiveSummary[Metric] = "Total Employees"
)
```

---

## Column Cross-Reference — Satisfaction Scores

All four satisfaction dimensions use the same 1–4 scale:

| Score | Label | Meaning |
|---|---|---|
| 1 | Low / Bad | Very dissatisfied. Strong attrition risk indicator. |
| 2 | Medium / Good | Somewhat dissatisfied. Worth monitoring. |
| 3 | High / Better | Satisfied. Attrition close to company average. |
| 4 | Very High / Best | Very satisfied. Lowest attrition risk. |

---

## Quick Filter Reference

Common Power BI slicer/filter combinations and what they reveal:

| Filter | Insight surfaced |
|---|---|
| `Attrition = Yes` | Profile of employees who left |
| `OverTime = Yes` + `Attrition = Yes` | The overtime trap in action |
| `RiskBand = Critical` | Employees at highest departure risk |
| `YearsAtCompany` between 1–3 | Onboarding failure window |
| `YearsSinceLastPromotion` >= 4 | Promotion stagnation cohort |
| `SatisfactionComposite` < 2 | The Satisfaction Trinity danger zone |
| `IncomeVsLevelMedian` < -0.10 | Significantly underpaid employees |
