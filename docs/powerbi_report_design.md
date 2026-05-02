# Power BI Report Design — Expert Specification

## Overview

A 6-page dark-theme executive report built on the Medallion gold exports.
Every measure, layout decision, and visual configuration is defined below —
follow this guide in Power BI Desktop and the result is a presentation-grade report.

---

## 1. Setup (Do This First)

### A. Import the theme
1. Open `employee_attrition_report.pbix` in Power BI Desktop
2. **View → Themes → Browse for themes**
3. Select `powerbi/theme.json`
4. Click **Keep current theme** on the color dialog → **Apply**

### B. Load all data tables

Each CSV has a different schema so import them **one by one** via Text/CSV
(the Folder connector shows file metadata, not data — do not use it here).

**Repeat these steps for each file below:**
1. **Home → Get Data → Text/CSV**
2. Navigate to `data/exports/` and select the file
3. In the preview dialog → click **Transform Data** (not Load)
4. Repeat for each file — no renaming needed, Power BI uses the filename as the table name
5. Once all 10 are loaded → **Home → Close & Apply**

| File to select                  | Default table name in Power BI  |
|---------------------------------|---------------------------------|
| `employee_data.csv`             | `employee_data`                 |
| `attrition_by_department.csv`   | `attrition_by_department`       |
| `attrition_by_role.csv`         | `attrition_by_role`             |
| `attrition_by_demographics.csv` | `attrition_by_demographics`     |
| `satisfaction_analysis.csv`     | `satisfaction_analysis`         |
| `salary_analysis.csv`           | `salary_analysis`               |
| `tenure_analysis.csv`           | `tenure_analysis`               |
| `overtime_impact.csv`           | `overtime_impact`               |
| `risk_scores.csv`               | `risk_scores`                   |
| `executive_summary.csv`         | `executive_summary`             |

> **Tip:** After clicking Transform Data on the first file, you can add the remaining 9
> directly inside Power Query Editor via **New Source → Text/CSV** without closing it.
> This is faster than repeating the Get Data flow 10 times.

### C. Set column types in Power Query
In **Transform Data**, set these explicitly for `employee_data`:
- `MonthlyIncome`, `Age`, `YearsAtCompany`, `EmployeeNumber` → **Whole Number**
- `SatisfactionComposite`, `FlightRiskScore`, `IncomeVsLevelMedian` → **Decimal Number**
- `AttritionRate` in aggregation tables → **Decimal Number**
- `Attrition`, `OverTime`, `RiskBand` → **Text**

### D. Canvas settings
For every page: **Format → Page background → Color: `#0D1117` → Transparency: 0%**
**Canvas size: Custom — Width: 1280 px, Height: 720 px**

---

## 2. DAX Measures

Create a dedicated **Measures** table (Home → Enter Data → name it `_Measures`, blank table).
Add all measures below to this table.

```dax
// ── Core Attrition ────────────────────────────────────────────────────────

[Total Employees] =
COUNTROWS(employee_data)

[Attrition Count] =
CALCULATE(COUNTROWS(employee_data), employee_data[Attrition] = "Yes")

[Attrition Rate] =
DIVIDE([Attrition Count], [Total Employees])

[Attrition Rate %] =
FORMAT([Attrition Rate], "0.0%")

[Retention Rate] =
1 - [Attrition Rate]

// ── Overtime ──────────────────────────────────────────────────────────────

[OT Employees] =
CALCULATE(COUNTROWS(employee_data), employee_data[OverTime] = "Yes")

[OT Rate] =
DIVIDE([OT Employees], [Total Employees])

[OT Attrition Rate] =
CALCULATE([Attrition Rate], employee_data[OverTime] = "Yes")

[Non-OT Attrition Rate] =
CALCULATE([Attrition Rate], employee_data[OverTime] = "No")

[OT Relative Risk] =
DIVIDE([OT Attrition Rate], [Non-OT Attrition Rate])

// ── Satisfaction ──────────────────────────────────────────────────────────

[Avg Satisfaction Composite] =
AVERAGE(employee_data[SatisfactionComposite])

[Avg Job Satisfaction] =
AVERAGE(employee_data[JobSatisfaction])

[Avg Env Satisfaction] =
AVERAGE(employee_data[EnvironmentSatisfaction])

[Avg Relationship Satisfaction] =
AVERAGE(employee_data[RelationshipSatisfaction])

[Avg Work Life Balance] =
AVERAGE(employee_data[WorkLifeBalance])

// ── Compensation ──────────────────────────────────────────────────────────

[Avg Monthly Income] =
AVERAGE(employee_data[MonthlyIncome])

[Median Monthly Income] =
MEDIAN(employee_data[MonthlyIncome])

[Income Gap vs Level Median] =
AVERAGE(employee_data[IncomeVsLevelMedian])

[Below Median Income Count] =
CALCULATE(COUNTROWS(employee_data), employee_data[IncomeVsLevelMedian] < -0.05)

[Below Median Attrition Rate] =
CALCULATE([Attrition Rate], employee_data[IncomeVsLevelMedian] < -0.05)

// ── Risk ──────────────────────────────────────────────────────────────────

[Avg Flight Risk Score] =
AVERAGE(risk_scores[FlightRiskScore])

[High Risk Count] =
CALCULATE(
    COUNTROWS(risk_scores),
    risk_scores[RiskBand] IN {"High", "Critical"}
)

[Critical Risk Count] =
CALCULATE(
    COUNTROWS(risk_scores),
    risk_scores[RiskBand] = "Critical"
)

[High Risk Rate] =
DIVIDE([High Risk Count], COUNTROWS(risk_scores))

// ── Tenure & Promotion ────────────────────────────────────────────────────

[Avg Years at Company] =
AVERAGE(employee_data[YearsAtCompany])

[Avg Years Since Promotion] =
AVERAGE(employee_data[YearsSinceLastPromotion])

[Stagnation Risk Count] =
CALCULATE(COUNTROWS(employee_data), employee_data[YearsSinceLastPromotion] >= 4)

[Early Tenure Attrition Rate] =
CALCULATE(
    [Attrition Rate],
    employee_data[YearsAtCompany] >= 1,
    employee_data[YearsAtCompany] <= 3
)

[Stable Tenure Attrition Rate] =
CALCULATE([Attrition Rate], employee_data[YearsAtCompany] > 10)

// ── Dynamic Titles ────────────────────────────────────────────────────────

[Title Attrition Rate] =
"Overall Attrition Rate: " & FORMAT([Attrition Rate], "0.0%")

[Title OT Risk] =
"Overtime employees leave at " & FORMAT([OT Relative Risk], "0.0") & "x the rate"

[Title High Risk] =
FORMAT([High Risk Count], "#,0") & " employees in High / Critical risk band"

// ── KPI Targets (adjust to company benchmarks) ───────────────────────────

[Attrition Target] = 0.10         -- 10% industry benchmark

[Attrition vs Target] =
[Attrition Rate] - [Attrition Target]

[Attrition Target Label] =
IF(
    [Attrition Rate] <= [Attrition Target],
    "BELOW TARGET",
    "ABOVE TARGET " & FORMAT([Attrition vs Target], "+0.0%;-0.0%")
)
```

---

## 3. Report Pages

---

### PAGE 1 — Executive Command Center

**Purpose:** Single-screen overview for C-suite. Every critical number visible at a glance.

**Background:** `#0D1117` | **No page border**

#### Layout (1280 × 720)

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER BAR  (full width, H=70, fill #161B22, bottom border     │
│  #E74C3C 3px)  —  Title text + subtitle + last refresh date     │
├──────────┬────────┬────────┬────────┬────────┬─────────────────┤
│  KPI 1   │  KPI 2 │  KPI 3 │  KPI 4 │  KPI 5 │  KPI 6         │
│ Employees│Attriti-│ Avg Inc │  OT    │Hi-Risk │ Avg Satisfact. │
│          │ on Rate│        │  Rate  │ Count  │                 │
├──────────┴────────┴────────┴────────┴────────┴─────────────────┤
│                                                                 │
│   ATTRITION BY DEPARTMENT          │  ATTRITION BY JOB ROLE   │
│   (Clustered Bar, H=270)           │  (Horizontal Bar, H=270) │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  TENURE ATTRITION CURVE (Area Line, full width, H=160)          │
└─────────────────────────────────────────────────────────────────┘
```

#### Visuals — step by step

**1. Header Bar**
- Insert → **Text Box** — X:0, Y:0, W:1280, H:70
- Fill: `#161B22`, Border bottom: `#E74C3C` 3px
- Text: `EMPLOYEE ATTRITION ANALYTICS` — font: Segoe UI Semibold 18px, color `#F0F6FC`
- Sub-text: `IBM HR Dataset  ·  Medallion Architecture` — font: Segoe UI 11px, color `#8B949E`

**2. Six KPI Cards** (Y:80, H:100, equally spaced across width)

| # | Measure                                    | Label              | Accent Color |
|---|--------------------------------------------|--------------------|--------------|
| 1 | `[Total Employees]`                        | Total Employees    | `#3498DB`    |
| 2 | `[Attrition Rate %]`                       | Attrition Rate     | `#E74C3C`    |
| 3 | `[Avg Monthly Income]` + Format $#,0       | Avg Monthly Income | `#27AE60`    |
| 4 | `[OT Rate]` Format %                       | Overtime Rate      | `#E67E22`    |
| 5 | `[High Risk Count]`                        | High/Critical Risk | `#8E44AD`    |
| 6 | `[Avg Satisfaction Composite]` Format 0.00 | Avg Satisfaction   | `#F39C12`    |

For each card:
- Visual: **Card**
- Format → Data label: font size 32, bold, Segoe UI Semibold
- Format → Category label: font size 10, color `#8B949E`, ALL CAPS
- Format → Background: `#161B22`
- Format → Border: color `{Accent Color}`, width 2px, bottom only (use "Specific sides")

**3. Attrition by Department** — Clustered Bar Chart
- X: 20, Y: 195, W: 580, H: 260
- Fields: X-axis = `attrition_by_department[Department]`, Y-axis = `attrition_by_department[AttritionRate]`
- Format → Data colors: conditional — use gradient Red (`#E74C3C`) to Blue (`#3498DB`)
- Format → Data labels: ON, color `#F0F6FC`, font size 10
- Add **Constant Line**: value = `[Attrition Rate]`, label "Company Avg", color `#F39C12`, dashed
- Title: "Attrition Rate by Department"
- Background: `#161B22`, Border: `#30363D`

**4. Attrition by Job Role** — Horizontal Bar Chart
- X: 640, Y: 195, W: 620, H: 260
- Fields: Y-axis = `attrition_by_role[JobRole]`, X-axis = `attrition_by_role[AttritionRate]`
- Sort: Descending by AttritionRate
- Format → Data colors: color rule — value >= 0.25 = `#E74C3C`, 0.15–0.25 = `#E67E22`, < 0.15 = `#3498DB`
- Add **Constant Line**: value = `[Attrition Rate]`, color `#F39C12`, dashed
- Title: "Attrition Rate by Job Role  (sorted by risk)"

**5. Tenure Attrition Curve** — Area Chart
- X: 20, Y: 465, W: 1240, H: 235
- Fields: X-axis = `tenure_analysis[YearsAtCompany]`, Y-axis = `tenure_analysis[AttritionRate]`
- Format → Line color: `#E74C3C`, area fill: `#E74C3C` at 15% transparency
- Add **Reference band**: X = 1 to 3 (color `#E74C3C`, 8% fill), X = 5 to 8 (color `#E67E22`, 8% fill)
- Add **Constant Line**: `[Attrition Rate]`, color `#F39C12`, dashed, labeled "Company Avg"
- Title: "Attrition Rate by Tenure  —  The Dual-Crisis Curve (Year 1–3 & Year 5–8)"

---

### PAGE 2 — Workforce Risk Intelligence

**Purpose:** Flight risk register. Who is at risk, how many, and where.

#### Visuals

**1. Risk Band Donut** — Donut Chart
- X: 20, Y: 80, W: 320, H: 320
- Fields: Legend = `risk_scores[RiskBand]`, Values = count of `risk_scores[EmployeeNumber]`
- Colors: Low=`#27AE60`, Moderate=`#F39C12`, High=`#E67E22`, Critical=`#E74C3C`
- Inner radius: 55%, detail labels ON (show %, bold)
- Title: "Flight Risk Distribution"
- Center label: Add a Card visual on top showing `[High Risk Count]` with label "High/Critical"

**2. Risk KPI Cards** (horizontal row, Y:80, right of donut)

| Measure                          | Label              |
|----------------------------------|--------------------|
| `[High Risk Count]`              | High/Critical Risk |
| `[Critical Risk Count]`          | Critical Risk      |
| `[High Risk Rate]` Format %      | High Risk Rate     |
| `[OT Relative Risk]` Format 0.0x | OT Relative Risk   |

**3. Risk by Department Matrix** — Matrix visual
- X: 20, Y: 420, W: 450, H: 260
- Rows = `employee_data[Department]`, Columns = `risk_scores[RiskBand]`, Values = count EmployeeNumber
- Format → Conditional formatting on Values: color scale Low=`#27AE60` → High=`#E74C3C`
- Title: "Risk Band by Department"

**4. Flight Risk Register** — Table
- X: 500, Y: 80, W: 760, H: 600
- Columns: EmployeeNumber, JobRole, Department, MonthlyIncome, YearsAtCompany, FlightRiskScore, RiskBand
- Sort: FlightRiskScore descending
- Conditional formatting on **RiskBand**: Critical=`#E74C3C` bg, High=`#E67E22` bg, Moderate=`#F39C12` bg, Low=`#27AE60` bg
- Conditional formatting on **FlightRiskScore**: data bar, `#E74C3C`
- Format → Header: `#21262D` bg, bold white text
- Title: "Employee Flight Risk Register  (sorted by risk score)"
- Add slicer: `risk_scores[RiskBand]` — tile slicer, H:40, full width top of table area

---

### PAGE 3 — Attrition Drivers

**Purpose:** What causes attrition? Deep dive into the top behavioral drivers.

#### Visuals

**1. Overtime Impact** — Clustered Bar
- X: 20, Y: 80, W: 380, H: 300
- Fields: X-axis = `overtime_impact[OverTime]` (0/1 mapped as No/Yes), Y-axis = `overtime_impact[AttritionRate]`
- Colors: No=`#27AE60`, Yes=`#E74C3C`
- Data labels ON
- Title: "Attrition Rate: Overtime vs No Overtime"
- Add a Card below: `[OT Relative Risk]` with label "Relative Risk Multiplier"

**2. Overtime × Satisfaction Heatmap** — Matrix
- X: 420, Y: 80, W: 420, H: 300
- Rows = `overtime_impact[JobSatisfaction]`, Columns = `overtime_impact[OverTime]`, Values = `overtime_impact[AttritionRate]`
- Conditional formatting: gradient `#27AE60` (0%) → `#E74C3C` (50%+)
- Title: "The Overtime Trap  —  Attrition by Satisfaction × OT"

**3. Business Travel Attrition** — Clustered Bar
- X: 860, Y: 80, W: 400, H: 300
- Fields: X-axis = `employee_data[BusinessTravel]`, Y-axis = `[Attrition Rate]`
- Sort: Descending
- Colors: Non-Travel=`#27AE60`, Travel_Rarely=`#F39C12`, Travel_Frequently=`#E74C3C`
- Title: "Business Travel Burnout"

**4. Attrition by Distance Tier** — Funnel or Bar
- X: 20, Y: 400, W: 380, H: 280
- Fields: Y-axis = `employee_data[DistanceTier]`, X-axis = `[Attrition Rate]`
- Colors: gradient from `#27AE60` to `#E74C3C` by value
- Title: "The Distance Gradient"

**5. Attrition by Marital Status** — Donut or Clustered Bar
- X: 420, Y: 400, W: 380, H: 280
- Fields: X-axis = `employee_data[MaritalStatus]`, Y-axis = `[Attrition Rate]`
- Colors: Single=`#E74C3C`, Married=`#27AE60`, Divorced=`#F39C12`
- Title: "Single Employee Vulnerability"

**6. Stock Option Attrition** — Line + Bar combo
- X: 820, Y: 400, W: 440, H: 280
- Fields: X-axis = `employee_data[StockOptionLevel]`, Line Y = `[Attrition Rate]`, Bar Y = count
- Line color: `#E74C3C`, Bar color: `#3498DB` (low opacity)
- Title: "Stock Option Paradox  —  Level 1 retains best"

---

### PAGE 4 — Satisfaction & Engagement

**Purpose:** Measure the satisfaction landscape. Surface the Trinity pattern.

#### Visuals

**1. Four Satisfaction KPI Cards** (horizontal row, Y:80)

| Measure                                       | Label             | Icon hint |
|-----------------------------------------------|-------------------|-----------|
| `[Avg Env Satisfaction]` Format 0.00          | Environment       |           |
| `[Avg Job Satisfaction]` Format 0.00          | Job               |           |
| `[Avg Relationship Satisfaction]` Format 0.00 | Relationship      |           |
| `[Avg Work Life Balance]` Format 0.00         | Work-Life Balance |           |

Use **KPI visual** (not Card) so you can set target = 3.0 (healthy benchmark):
- Goal = 3 (acceptable threshold)
- Indicator = measure
- Format: good=`#27AE60`, bad=`#E74C3C`

**2. Satisfaction vs Attrition — All 4 Dimensions** — Line Chart
- X: 20, Y: 200, W: 780, H: 320
- Fields: X-axis = `satisfaction_analysis[Score]`, Y-axis = `satisfaction_analysis[AttritionRate]`
- Legend = `satisfaction_analysis[SatisfactionDimension]`
- Colors: environment=`#3498DB`, job=`#E74C3C`, relationship=`#27AE60`, WLB=`#F39C12`
- Add reference line at Y=0.161 (company avg), dashed `#8B949E`
- Title: "How Each Satisfaction Dimension Drives Attrition"

**3. Satisfaction Trinity Heatmap** — Matrix
- X: 820, Y: 200, W: 440, H: 320
- Rows = `employee_data[JobSatisfaction_Label]`, Columns = `employee_data[EnvironmentSatisfaction_Label]`
- Values = `[Attrition Rate]`
- Conditional formatting: Red-Green diverging
- Title: "The Satisfaction Trinity  —  Combined Effect"

**4. Composite Distribution** — Histogram (Clustered Bar by bin)
- X: 20, Y: 540, W: 580, H: 160
- Create a bin column in Power Query: `= Number.RoundDown([SatisfactionComposite], 0)` → renamed `SatisfactionBin`
- Fields: X=`SatisfactionBin`, Y=`[Attrition Rate]` + secondary bar=count
- Title: "Attrition Rate by Satisfaction Composite Score"

**5. Work-Life Balance Breakdown** — Bar
- X: 620, Y: 540, W: 640, H: 160
- Fields: X=`employee_data[WorkLifeBalance_Label]`, Y=`[Attrition Rate]`
- Sort: by score ascending (Bad → Best)
- Color gradient: `#E74C3C` → `#27AE60`
- Title: "Work-Life Balance vs Attrition"

---

### PAGE 5 — Compensation Intelligence

**Purpose:** Salary fairness, compression, and its impact on attrition.

#### Visuals

**1. Income by Job Level** — Box Plot (use Clustered Bar as approximation)
- X: 20, Y: 80, W: 580, H: 300
- Fields: X=`salary_analysis[JobLevel]`, Y=`salary_analysis[MedianIncome]`, Tooltips = Min/Max/Mean
- Format → Data colors: gradient by JobLevel (darker = higher)
- Add error bars: use Min and Max columns
- Title: "Monthly Income Distribution by Job Level"

**2. Salary Compression Matrix** — Matrix
- X: 620, Y: 80, W: 640, H: 300
- Rows = `salary_analysis[JobLevel]`, Columns = `salary_analysis[JobRole]`
- Values = `salary_analysis[AvgIncomeVsLevelMedian]` (formatted as %)
- Conditional formatting: diverging — Red (`#E74C3C`) below 0, Green (`#27AE60`) above 0, center = 0
- Title: "Salary Compression  —  Income vs Level Median (% deviation)"
- This reveals exactly which roles are systematically underpaid within their level

**3. Income vs Attrition Scatter** — Scatter chart
- X: 20, Y: 400, W: 580, H: 280
- X-axis = `salary_analysis[MeanIncome]`, Y-axis = `salary_analysis[AttritionRate]`
- Size = `salary_analysis[TotalEmployees]`, Legend = `salary_analysis[JobRole]`
- Add trend line (Power BI Analytics pane)
- Title: "Income vs Attrition Rate by Role  (bubble size = headcount)"

**4. Below-Median Attrition Card** — KPI Card
- X: 620, Y: 400, W: 300, H: 120
- Measure: `[Below Median Attrition Rate]` + label "Below-Median Income Attrition"
- Color: `#E74C3C`
- Add Card below: `[Below Median Income Count]` + label "Employees Below Level Median"

**5. Salary Hike vs Attrition** — Scatter
- X: 950, Y: 400, W: 310, H: 280
- X=`employee_data[PercentSalaryHike]`, Y=`[Attrition Rate]`, size=headcount
- Title: "Salary Hike % vs Attrition"

---

### PAGE 6 — Tenure & Career Trajectory

**Purpose:** Career lifecycle — when do people leave and why their careers stall.

#### Visuals

**1. The Dual-Crisis Curve** — Area + Line Combo
- X: 20, Y: 80, W: 800, H: 320
- Line: `tenure_analysis[YearsAtCompany]` vs `tenure_analysis[AttritionRate]`
- Line color: `#E74C3C`, line width: 2.5px
- Area fill: `#E74C3C` at 15% opacity
- Reference bands: Year 1–3 (Crisis 1, `#E74C3C` 10%), Year 5–8 (Crisis 2, `#E67E22` 10%)
- Constant line at company avg attrition
- Title: "The Dual-Crisis Tenure Curve  —  Two Separate Retention Problems"
- Annotations (Text boxes): "Onboarding Failure (Yr 1-3)" and "Career Plateau (Yr 5-8)"

**2. Promotion Stagnation** — Bar Chart
- X: 840, Y: 80, W: 420, H: 320
- X=`employee_data[YearsSinceLastPromotion]` (binned 0-2, 3-4, 5+)
- Y=`[Attrition Rate]`
- Color rule: YearsSince >= 4 = `#E74C3C`, else `#3498DB`
- Reference line at company avg
- Title: "Promotion Stagnation Effect  —  The 4-Year Cliff"

**3. Manager Tenure Impact** — Clustered Bar
- X: 20, Y: 420, W: 580, H: 260
- Create band column: Manager Tenure Ratio → Low (0-25%), Medium (25-50%), High (50-75%), Very High (75%+)
  - Power Query: `= if [ManagerTenureRatio] < 0.25 then "Low" else if [ManagerTenureRatio] < 0.5 then "Medium" else if [ManagerTenureRatio] < 0.75 then "High" else "Very High"`
- X = MgrBand, Y = `[Attrition Rate]`
- Colors: Low=`#E74C3C`, Medium=`#E67E22`, High=`#F39C12`, Very High=`#27AE60`
- Title: "Manager Loyalty Anchor  —  Stable Manager = Lower Attrition"

**4. Training vs Attrition** — Scatter
- X: 620, Y: 420, W: 640, H: 260
- X=`employee_data[TrainingTimesLastYear]`, Y=`[Attrition Rate]` (aggregated)
- Add trend line
- Title: "Training Investment vs Attrition  —  Does training retain?"

**5. Age Band Attrition** — Bar
- X: 620, Y: 420 — swap with training if preferred
- X=`employee_data[AgeBand]`, Y=`[Attrition Rate]`
- Sort by AgeBand ascending
- Color gradient young (`#E74C3C`) → older (`#27AE60`)
- Title: "Attrition by Age Band"

---

## 4. Navigation Rail

On every page, add a left-side navigation rail (W:60, full height, fill `#161B22`):

**Buttons** (Insert → Buttons → Blank):
- Each button: W:50, H:50, rounded corners
- Fill: `#21262D` (default), `#E74C3C` (hover), `#E74C3C 40%` (current page)
- Icon: Use emoji text boxes (▶ ▲ ⚡ ★ $ ↗) or Power BI icons
- Action: Page navigation

Navigation labels:
1. `⌂` → Page 1 (Overview)
2. `⚠` → Page 2 (Risk)
3. `↑` → Page 3 (Drivers)
4. `♡` → Page 4 (Satisfaction)
5. `$` → Page 5 (Compensation)
6. `↗` → Page 6 (Tenure)

---

## 5. Drillthrough Pages

### Drillthrough: Employee Detail
Create a hidden 7th page ("Employee Detail") with drillthrough field = `EmployeeNumber`:
- All KPIs for that single employee
- Their risk score and risk band
- Their satisfaction scores as gauges
- Their tenure and salary vs peer median
- Right-click any table with EmployeeNumber → Drillthrough → Employee Detail

---

## 6. Slicers (Global — on every page)

Sync these slicers across all pages (**View → Sync slicers**):

| Slicer     | Field                   | Style           |
|------------|-------------------------|-----------------|
| Department | `employee_data[Department]` | Dropdown        |
| Job Role   | `employee_data[JobRole]`    | Dropdown        |
| Attrition  | `employee_data[Attrition]`  | Tile (Yes / No) |
| Risk Band  | `risk_scores[RiskBand]`  | Tile            |

Place slicers in a collapsible filter panel triggered by a button (use bookmarks):
- Bookmark 1: "Filters Open" — slicers visible
- Bookmark 2: "Filters Closed" — slicers hidden
- Button: `Filter` icon, Action = Toggle bookmark

---

## 7. Conditional Formatting Rules Summary

| Visual                    | Column                 | Rule                                                             |
|---------------------------|------------------------|------------------------------------------------------------------|
| Risk Register Table       | RiskBand               | Critical=#E74C3C bg, High=#E67E22, Moderate=#F39C12, Low=#27AE60 |
| Risk Register Table       | FlightRiskScore        | Data bar, color #E74C3C                                          |
| Salary Compression Matrix | AvgIncomeVsLevelMedian | Diverging: <0 = Red, >0 = Green, 0 = white                       |
| Any Attrition Rate        | Value > 0.25           | Bold font + `#E74C3C` text color                                 |
| KPI Cards                 | Attrition Rate         | Target = 0.10; above = red, below = green                        |
| Satisfaction KPI          | Score < 2.5            | Red background indicator                                         |

---

## 8. Report-Level Formatting Checklist

- [ ] All page backgrounds set to `#0D1117`
- [ ] All visual backgrounds set to `#161B22`
- [ ] All visual borders set to `#30363D`, rounded corners 8px
- [ ] All visual titles: Segoe UI Semibold 12px, `#F0F6FC`, no background
- [ ] All axis labels: `#8B949E`, 10px
- [ ] All data labels: `#F0F6FC`, 10px
- [ ] Grid lines: `#21262D` (very subtle)
- [ ] Legend position: Top (never right, wastes space)
- [ ] Zero line on bar charts: `#30363D`
- [ ] Theme imported from `powerbi/theme.json`
- [ ] All measures in `_Measures` table
- [ ] Drillthrough page hidden (right-click page tab → Hide page)
- [ ] Bookmark panel working (filter open/close)
- [ ] Navigation buttons on every page
- [ ] File saved as `employee_attrition_report.pbix`

---

## 9. Advanced: Tooltip Pages

Create mini tooltip pages (Page Information → Allow use as tooltip: ON):

**Tooltip: Role Detail**
- Page size: 320 × 200
- Shows: Role name, attrition rate, avg salary, avg satisfaction
- Assign to: any visual showing JobRole

**Tooltip: Risk Detail**
- Shows: Employee risk score breakdown (OT flag, satisfaction, promotion lag)
- Assign to: Risk Register table
