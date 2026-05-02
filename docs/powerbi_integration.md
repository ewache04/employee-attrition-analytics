# Power BI Integration Guide

## Connection Setup

After running the pipeline (`python main.py`), all gold tables are exported as CSVs
to `data/exports/`. Connect Power BI to this folder:

1. Open **Power BI Desktop** → **Get Data** → **Text/CSV**
2. Navigate to `<project_root>/data/exports/`
3. Import each CSV file you need (repeat for each table)
4. Use **Transform Data** to set correct column types if needed

Or use the **Folder connector** for a single source:
1. **Get Data** → **Folder**
2. Select `data/exports/`
3. Combine files → Power Query will auto-detect CSVs

---

## Recommended Report Pages

### Page 1 — Executive Overview
**Source:** `executive_summary.csv`, `attrition_by_department.csv`

| Visual | Type | Fields |
|---|---|---|
| Attrition KPI cards | Card | Overall Attrition Rate, Total Employees, High-Risk Count |
| Department attrition | Clustered bar | Department (axis), AttritionRate (value) |
| Overtime rate | Donut chart | OverTime (legend), TotalEmployees (value) |

---

### Page 2 — Role & Department Drill-Through
**Source:** `attrition_by_role.csv`

| Visual | Type | Fields |
|---|---|---|
| Attrition by Role | Horizontal bar | JobRole (axis), AttritionRate (value), sorted descending |
| Dept slicer | Slicer | Department |
| Avg satisfaction | Gauge | AvgSatisfactionComposite |

---

### Page 3 — Satisfaction Analysis
**Source:** `satisfaction_analysis.csv`

| Visual | Type | Fields |
|---|---|---|
| Satisfaction vs Attrition | Line chart | Score (x), AttritionRate (y), SatisfactionDimension (legend) |
| Dimension slicer | Slicer | SatisfactionDimension |

---

### Page 4 — Tenure & Promotion
**Source:** `tenure_analysis.csv`

| Visual | Type | Fields |
|---|---|---|
| Tenure curve | Area chart | YearsAtCompany (x), AttritionRate (y) |
| Reference line | Analytics pane | Constant at 0.161 (company avg) |
| Promotion lag | Scatter | YearsAtCompany (x), AvgYearsSincePromotion (y) |

---

### Page 5 — Salary Analysis
**Source:** `salary_analysis.csv`

| Visual | Type | Fields |
|---|---|---|
| Income by level | Box plot / bar | JobLevel (axis), MedianIncome (value) |
| Income vs attrition | Scatter | MeanIncome (x), AttritionRate (y), JobRole (tooltip) |
| Compression map | Heatmap (Matrix) | JobLevel (row), AvgIncomeVsLevelMedian (values) |

---

### Page 6 — Flight Risk Register
**Source:** `risk_scores.csv`

| Visual | Type | Fields |
|---|---|---|
| Risk band donut | Donut | RiskBand (legend), count (value) |
| Risk register table | Table | EmployeeNumber, JobRole, Department, FlightRiskScore, RiskBand |
| Risk slicer | Slicer | RiskBand (multi-select) |

---

## Suggested DAX Measures

```dax
// Attrition Rate
Attrition Rate =
DIVIDE(
    CALCULATE(COUNTROWS(risk_scores), risk_scores[Attrition] = 1),
    COUNTROWS(risk_scores)
)

// High + Critical Risk Count
High Risk Count =
CALCULATE(
    COUNTROWS(risk_scores),
    risk_scores[RiskBand] IN {"High", "Critical"}
)

// Overtime Relative Risk
OT Relative Risk =
DIVIDE(
    CALCULATE([Attrition Rate], overtime_impact[OverTime] = 1),
    CALCULATE([Attrition Rate], overtime_impact[OverTime] = 0)
)
```

---

## Refresh Schedule

The CSVs in `data/exports/` are regenerated each time `python main.py` runs.
In Power BI Desktop, use **Refresh** to pick up the latest data.

For automated refresh in Power BI Service, publish the report and configure
a **scheduled refresh** that points to a gateway connected to your local `data/exports/` folder.
