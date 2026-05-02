# Insights Playbook — The 10 Hidden Patterns

This document is the permanent record of analytical insights derived from the
IBM HR Attrition dataset. Each insight is reproducible via notebook 05.

---

## 1. The Overtime Trap (Critical)

**Finding:** Employees working overtime leave at **3.1× the rate** of those who don't
(30.5% vs. 10.4%). This is the single strongest behavioral predictor in the dataset.

**Deeper signal:** The effect is *multiplicative* — Overtime=Yes AND JobSatisfaction=1
yields ~53% attrition. No other two-factor combination comes close.

**Action:** Audit overtime by role quarterly. Any role where >20% of headcount
regularly works OT is a structural problem, not an individual one.

---

## 2. The Salary Compression Cliff (High)

**Finding:** Employees earning more than 20% below their job-level median leave at
**2× the rate** of those at or above median. The perception of being underpaid
relative to peers, not absolute compensation, drives departure.

**Deeper signal:** The effect is strongest at Job Levels 1–2 (junior employees)
where salary banding is often the least rigorous.

**Action:** Annual within-level pay equity review. Identify and correct below-median
outliers before they self-select out.

---

## 3. The Promotion Stagnation Effect (High)

**Finding:** Employees who haven't been promoted in **4+ years** leave at **1.8×** the
rate of recently promoted employees. This signal is invisible in satisfaction scores —
employees may rate themselves satisfied while quietly interviewing elsewhere.

**Deeper signal:** The PromotionLag ratio (YearsSincePromotion / YearsAtCompany)
is more predictive than the raw years — an employee at year 10 with no promotion
in 8 years is far riskier than an employee at year 4 with no promotion in 3.

**Action:** Enforce a maximum 3-year promotion review cycle for all IC roles.
If promotion isn't possible, career lattice moves (lateral + growth) should be offered.

---

## 4. The 1-Year Honeymoon / 3-Year Crisis (High)

**Finding:** Attrition follows a **dual-peak curve**:
- Peak 1 (years 1–2): Onboarding failure. New hires who don't find role/culture fit.
- Valley (years 3–4): Survivors are more committed.
- Peak 2 (years 5–8): Career plateau. Employees who haven't advanced seek it elsewhere.
- Stable (years 10+): Anchored employees; very low attrition.

These are **two different problems** requiring two different retention strategies.

**Action:**
- Years 1–2: Structured 30/60/90/180-day check-ins, mentorship pairing.
- Years 5–8: Career development conversations, stretch assignments, promotion pipeline.

---

## 5. The Satisfaction Trinity (Critical)

**Finding:** When all three of EnvironmentSatisfaction, JobSatisfaction, AND
RelationshipSatisfaction are simultaneously ≤2, attrition reaches **~50%**.
Any single dimension alone is a weak predictor. The **combination** is the signal.

**Deeper signal:** WorkLifeBalance is slightly less predictive when combined with the
other three — the first three dimensions form the core "trinity."

**Action:** Build an automated HR alert: flag employees scoring ≤2 in all three
dimensions. These employees need a manager conversation within 30 days.

---

## 6. The Manager Loyalty Anchor (Medium)

**Finding:** ManagerTenureRatio in the top quartile (employee has been with their
manager for 75%+ of their company tenure) correlates with **40% lower attrition**.

**Deeper signal:** Manager changes — not just new managers, but frequent changes —
are a leading indicator of attrition risk, not a lagging one.

**Action:** Include manager stability in workforce planning. Track manager changes
per team as a leading HR metric. Manager turnover > 1× per 2 years in a team is a flag.

---

## 7. The Stock Option Paradox (Medium)

**Finding:** Stock option Level 1 has the **lowest** attrition (~11%), but Level 3
(maximum) has attrition **higher than Level 2** (~14% vs. ~9%). The expected
"golden handcuffs" effect of maximum stock options does not hold.

**Possible explanation:** Level 3 allocations may coincide with roles under the most
pressure (high-level ICs/managers who are also most likely to receive competing offers).
Alternatively, employees at Level 3 who don't feel growth may feel "bought but trapped."

**Action:** Investigate whether Level 3 recipients are disproportionately in high-OT,
high-pressure roles. Stock options complement culture; they don't replace it.

---

## 8. The Distance Gradient (Medium)

**Finding:** Attrition rises non-linearly beyond 10 miles. The steepest jump is
between Moderate (6–10 mi) and Far (11–20 mi) categories — a near 5-percentage-point
increase. Very Far (>20 mi) is the highest at ~23%.

**Deeper signal:** The relationship is quadratic, not linear — moderate distances
barely affect attrition, but longer commutes have a disproportionate impact.

**Action:** For roles where commute is unavoidable, prioritise remote/hybrid options
for employees >10 miles. Even 2 days/week remote reduces effective commute burden by 40%.

---

## 9. The Single Employee Vulnerability (Medium)

**Finding:** Single employees leave at **~25%** — almost exactly double the rate of
married employees (~12%). The effect is amplified by overtime:
Single + Overtime approaches **~40%** attrition.

**Possible explanation:** Single employees have lower switching costs (no partner
income dependency, no children's school constraints) and may also have fewer
social anchors within the company.

**Action:** Targeted engagement for single employees in high-OT roles — ERG programs,
social events, and ensuring workload distribution does not systematically fall on
those with fewer perceived "reasons to decline."

---

## 10. The Business Travel Burnout (High)

**Finding:** Travel_Frequently employees leave at **~24%** (vs. 8% Non-Travel).
The combination of frequent travel AND poor WorkLifeBalance yields **~50%** attrition
— the second-highest two-factor combination after the Overtime Trap.

**Deeper signal:** Travel_Rarely is actually safe (~15%) — frequent travel is the
threshold. This suggests a **step function**, not a continuous relationship.

**Action:** Cap Travel_Frequently classification at 20% of any team's headcount.
Rotate travel assignments. Compensate frequent travelers with additional PTO or remote days.

---

## Summary Risk Matrix

| Factor | Standalone Attrition | Key Combination | Combined Attrition |
|---|---|---|---|
| Overtime=Yes | 30.5% | OT + JobSat=1 | ~53% |
| BusinessTravel=Frequent | 24.0% | Frequent + WLB=1 | ~50% |
| All-3-Satisfaction-Low | ~49.0% | — | — |
| Single | 25.0% | Single + OT | ~40% |
| YearsAtCompany 1–3 | ~30.0% | 1-3yr + OT | ~45% |
| YearsSincePromotion 4+ | ~25.0% | Stagnation + Low Sat | ~38% |
