# Power BI M Queries — All 10 Tables

Copy and paste each block into the Advanced Editor for the matching query.
All paths use `EmployeeAttrition` (no space) to avoid line-break issues.

---

## employee_data

```
let
    Source = Csv.Document(File.Contents("C:\Documents\GitHubRepos\PowerBIProject\EmployeeAttrition\data\exports\employee_data.csv"),[Delimiter=",", Columns=48, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Age", Int64.Type}, {"Attrition", type text}, {"BusinessTravel", type text}, {"DailyRate", Int64.Type}, {"Department", type text}, {"DistanceFromHome", Int64.Type}, {"Education", Int64.Type}, {"EducationField", type text}, {"EmployeeNumber", Int64.Type}, {"EnvironmentSatisfaction", Int64.Type}, {"HourlyRate", Int64.Type}, {"JobInvolvement", Int64.Type}, {"JobLevel", Int64.Type}, {"JobRole", type text}, {"JobSatisfaction", Int64.Type}, {"MaritalStatus", type text}, {"MonthlyIncome", Int64.Type}, {"MonthlyRate", Int64.Type}, {"NumCompaniesWorked", Int64.Type}, {"OverTime", type text}, {"PercentSalaryHike", Int64.Type}, {"PerformanceRating", Int64.Type}, {"RelationshipSatisfaction", Int64.Type}, {"StockOptionLevel", Int64.Type}, {"TotalWorkingYears", Int64.Type}, {"TrainingTimesLastYear", Int64.Type}, {"WorkLifeBalance", Int64.Type}, {"YearsAtCompany", Int64.Type}, {"YearsInCurrentRole", Int64.Type}, {"YearsSinceLastPromotion", Int64.Type}, {"YearsWithCurrManager", Int64.Type}, {"Education_Label", type text}, {"EnvironmentSatisfaction_Label", type text}, {"JobInvolvement_Label", type text}, {"JobSatisfaction_Label", type text}, {"PerformanceRating_Label", type text}, {"RelationshipSatisfaction_Label", type text}, {"WorkLifeBalance_Label", type text}, {"SatisfactionComposite", type number}, {"YearsPerCompany", type number}, {"IncomeVsLevelMedian", type number}, {"PromotionLag", type number}, {"ManagerTenureRatio", type number}, {"DistanceTier", type text}, {"AgeBand", type text}, {"GenderLabel", type text}, {"RiskBand", type text}, {"FlightRiskScore", type number}})
in
    #"Changed Type"
```

---

## risk_scores

```
let
    Source = Csv.Document(File.Contents("C:\Documents\GitHubRepos\PowerBIProject\EmployeeAttrition\data\exports\risk_scores.csv"),[Delimiter=",", Columns=8, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"EmployeeNumber", Int64.Type}, {"JobRole", type text}, {"Department", type text}, {"MonthlyIncome", Int64.Type}, {"YearsAtCompany", Int64.Type}, {"FlightRiskScore", type number}, {"RiskBand", type text}, {"Attrition", Int64.Type}})
in
    #"Changed Type"
```

---

## attrition_by_department

```
let
    Source = Csv.Document(File.Contents("C:\Documents\GitHubRepos\PowerBIProject\EmployeeAttrition\data\exports\attrition_by_department.csv"),[Delimiter=",", Columns=8, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Department", type text}, {"TotalEmployees", Int64.Type}, {"AttritionCount", Int64.Type}, {"AttritionRate", type number}, {"AvgMonthlyIncome", type number}, {"AvgJobSatisfaction", type number}, {"AvgYearsAtCompany", type number}, {"OvertimeRate", type number}})
in
    #"Changed Type"
```

---

## attrition_by_role

```
let
    Source = Csv.Document(File.Contents("C:\Documents\GitHubRepos\PowerBIProject\EmployeeAttrition\data\exports\attrition_by_role.csv"),[Delimiter=",", Columns=8, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Department", type text}, {"JobRole", type text}, {"TotalEmployees", Int64.Type}, {"AttritionCount", Int64.Type}, {"AttritionRate", type number}, {"AvgMonthlyIncome", type number}, {"AvgJobLevel", type number}, {"AvgSatisfactionComposite", type number}})
in
    #"Changed Type"
```

---

## attrition_by_demographics

```
let
    Source = Csv.Document(File.Contents("C:\Documents\GitHubRepos\PowerBIProject\EmployeeAttrition\data\exports\attrition_by_demographics.csv"),[Delimiter=",", Columns=5, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"DimensionValue", type text}, {"TotalEmployees", Int64.Type}, {"AttritionCount", Int64.Type}, {"AttritionRate", type number}, {"Dimension", type text}})
in
    #"Changed Type"
```

---

## satisfaction_analysis

```
let
    Source = Csv.Document(File.Contents("C:\Documents\GitHubRepos\PowerBIProject\EmployeeAttrition\data\exports\satisfaction_analysis.csv"),[Delimiter=",", Columns=4, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Score", Int64.Type}, {"TotalEmployees", Int64.Type}, {"AttritionRate", type number}, {"SatisfactionDimension", type text}})
in
    #"Changed Type"
```

---

## salary_analysis

```
let
    Source = Csv.Document(File.Contents("C:\Documents\GitHubRepos\PowerBIProject\EmployeeAttrition\data\exports\salary_analysis.csv"),[Delimiter=",", Columns=9, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"JobLevel", Int64.Type}, {"JobRole", type text}, {"TotalEmployees", Int64.Type}, {"MinIncome", Int64.Type}, {"MedianIncome", type number}, {"MeanIncome", type number}, {"MaxIncome", Int64.Type}, {"AttritionRate", type number}, {"AvgIncomeVsLevelMedian", type number}})
in
    #"Changed Type"
```

---

## tenure_analysis

```
let
    Source = Csv.Document(File.Contents("C:\Documents\GitHubRepos\PowerBIProject\EmployeeAttrition\data\exports\tenure_analysis.csv"),[Delimiter=",", Columns=6, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"YearsAtCompany", Int64.Type}, {"TotalEmployees", Int64.Type}, {"AttritionCount", Int64.Type}, {"AttritionRate", type number}, {"AvgYearsSincePromotion", type number}, {"AvgManagerTenureRatio", type number}})
in
    #"Changed Type"
```

---

## overtime_impact

```
let
    Source = Csv.Document(File.Contents("C:\Documents\GitHubRepos\PowerBIProject\EmployeeAttrition\data\exports\overtime_impact.csv"),[Delimiter=",", Columns=5, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"OverTime", type text}, {"JobSatisfaction", Int64.Type}, {"TotalEmployees", Int64.Type}, {"AttritionRate", type number}, {"AvgMonthlyIncome", type number}})
in
    #"Changed Type"
```

---

## executive_summary

```
let
    Source = Csv.Document(File.Contents("C:\Documents\GitHubRepos\PowerBIProject\EmployeeAttrition\data\exports\executive_summary.csv"),[Delimiter=",", Columns=2, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Metric", type text}, {"Value", type number}})
in
    #"Changed Type"
```
