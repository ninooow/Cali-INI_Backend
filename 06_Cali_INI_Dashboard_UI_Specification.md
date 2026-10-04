# Cali-INI — Detailed Dashboard UI Specification

## 1. Dashboard Purpose

The Dashboard is the **first-glance monitoring screen** used to answer five questions in sequence:

1. Is there anything that requires attention?
2. How is the currently monitored scope performing right now?
3. What is the operational context?
4. Which assets explain the current condition?
5. How are the indicators changing over time?

The Dashboard should function as an **operational monitoring screen**, not as a technical-analysis page.

The most important information must appear first. Technical details such as provenance, model metrics, RCA evidence, and detailed historical information must remain secondary to the operational monitoring task.

---

# 2. Overall Dashboard Structure

Use one vertically structured page with the following hierarchy:

```text
┌──────────────────────────────────────────────────────────────┐
│ HEADER                                                       │
│ Cali-INI                                                     │
│ Intelligent Manufacturing Decision Support                  │
│ Scope | Analysis Reference Time | Data Status                │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 1. ATTENTION REQUIRED                                        │
│                                                              │
│ 3 items require attention                                    │
│ P1 1       P2 1       P3 1                                  │
│                                                              │
│ [Problem Card]                                               │
│ [Problem Card]                                               │
│ [Problem Card]                                               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 2. CURRENT PLANT CONDITION                                   │
│ Scope: All assets                                            │
│                                                              │
│ [ Asset Health ] [ Operating Performance ] [ Reliability ]   │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 3. OPERATIONAL CONTEXT                                       │
│                                                              │
│ [ Load ] [ Production ] [ Downtime ] [ Emission Proxy ]     │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 4. ASSET STATUS                                               │
│                                                              │
│ Asset | Condition | Health | Priority | Forecast             │
│ ------------------------------------------------------------ │
│ ...                                                          │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 5. TREND ANALYSIS                                             │
│                                                              │
│ Trend group: [ Condition & Reliability | Operations ]        │
│ Indicator:   [ Asset Health Score ▼ ]                        │
│                                                              │
│                 LINE CHART                                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Vertical Priority

```text
MOST IMPORTANT
     ↓
Attention Required
     ↓
Current Plant Condition
     ↓
Operational Context
     ↓
Asset Status
     ↓
Trend Analysis
     ↓
LESS IMMEDIATE
```

---

# 3. Header

## 3.1 Purpose

The Header provides **monitoring context**, not analytical detail.

The user must immediately know:

- what application they are using;
- which scope they are viewing;
- the analysis reference time;
- whether the data quality gate passed.

## 3.2 Visual Structure

```text
┌──────────────────────────────────────────────────────────────┐
│ Cali-INI                                                     │
│ Intelligent Manufacturing Decision Support                  │
│                                                              │
│ Scope: All assets       As of: 03 Oct 2026, 12:00            │
│ Data status: PASS                                            │
└──────────────────────────────────────────────────────────────┘
```

## 3.3 Layout

### Level 1 — Product Identity

```text
Cali-INI
Intelligent Manufacturing Decision Support
```

### Level 2 — Monitoring Context

```text
Scope: All assets
|
As of: 03 Oct 2026, 12:00
|
Data status: PASS
```

### Do Not Place in the Header

Do not place the following in the primary header:

- MAE;
- RMSE;
- model name;
- source workbook;
- RCA details;
- forecast details;
- provenance;
- engine diagnostics.

These are technical or audit information and should not compete with operational information.

---

# 4. Section 1 — ATTENTION REQUIRED

## 4.1 Purpose

This section is the **exception monitoring area**.

It answers:

> **"Is there anything I need to pay attention to?"**

It is the first operational focal point of the Dashboard.

Only attention-requiring problem items should appear here. Routine NORMAL assets should not appear in this section.

---

# 5. Attention Section Header

Use:

```text
ATTENTION REQUIRED
3 items require attention
```

### Visual Hierarchy

```text
ATTENTION REQUIRED
18–20 px / semibold

3 items require attention
12–13 px / secondary text
```

Do not use a long explanatory paragraph.

---

# 6. Attention Summary

After the section title, show a compact P1/P2/P3 summary.

## 6.1 Recommended Structure

```text
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ P1           │ │ P2           │ │ P3           │
│              │ │              │ │              │
│      1       │ │      1       │ │      1       │
└──────────────┘ └──────────────┘ └──────────────┘
```

A more compact version is also acceptable:

```text
P1  1        P2  1        P3  1
```

## 6.2 Priority Visual Treatment

| Priority | Visual Treatment |
|---|---|
| P1 | Strong red emphasis |
| P2 | Amber/orange emphasis |
| P3 | Blue emphasis |
| P4 | Gray/neutral emphasis |

Priority styling must be visually distinct from equipment-condition styling.

Priority communicates **urgency**, while Condition communicates **equipment state**.

---

# 7. Attention Problem Card

Display up to **three problem cards** by default.

Do not use a dense full-width problem table as the primary representation in this section.

One card represents one problem.

## 7.1 Basic Structure

```text
┌──────────────────────────────────────────────────────────────┐
│ P1                                      PU-2101B             │
│                                                              │
│ High discharge pressure deviation                            │
│                                                              │
│ 🔴 ALARM             Ticket: OPEN                            │
│                                                              │
│ Next action                                                  │
│ Inspect discharge pressure / control condition               │
│                                                              │
│                              [ View problem ]                │
└──────────────────────────────────────────────────────────────┘
```

## 7.2 Required Card Information

Each card must contain only these seven elements:

### 1. Priority

Example:

```text
P1
```

### 2. Asset

Example:

```text
PU-2101B
```

### 3. Problem / Trigger

Example:

```text
High discharge pressure deviation
```

### 4. Condition Severity

Example:

```text
🔴 ALARM
```

### 5. Ticket State

Example:

```text
Ticket: OPEN
```

### 6. Recommended Next Action

Example:

```text
Inspect discharge pressure / control condition
```

### 7. Navigation Action

```text
[ View problem ]
```

---

# 8. Attention Card — Exact Layout

The preferred internal layout is horizontal:

```text
┌───────────────────────────────────────────────────────────────────┐
│                                                                   │
│  P1               PU-2101B                                       │
│                                                                   │
│                   High discharge pressure deviation               │
│                                                                   │
│                   🔴 ALARM     Ticket: OPEN                      │
│                                                                   │
│                   NEXT ACTION                                     │
│                   Inspect discharge pressure                      │
│                                                                   │
│                                                [ View problem ]   │
└───────────────────────────────────────────────────────────────────┘
```

### Recommended Relative Width

```text
Priority      10–15%
Asset/Issue   45–50%
Action        25–30%
CTA           15%
```

The problem/trigger must remain the most prominent text in the card after the priority/asset anchor.

---

# 9. Attention Card Visual Treatment

Each attention card should use:

- white background;
- thin neutral border;
- small-to-medium corner radius;
- subtle shadow;
- sufficient internal padding;
- a semantic left border or other restrained attention cue;
- blue as the primary interaction color;
- semantic status colors only for operational meaning.

Do not use:

- full red card backgrounds;
- heavy shadows;
- large warning icons that dominate the problem text;
- gradients;
- excessive decorative elements.

Preferred conceptual form:

```text
┌│────────────────────────────────────────────────────────────┐
││ P1 · PU-2101B                                             │
││ High discharge pressure deviation                         │
││ 🔴 ALARM · Ticket: OPEN                                   │
││                                                            │
││ Next action                                                │
││ Inspect discharge pressure / control condition             │
││                                         [ View problem ]    │
└│────────────────────────────────────────────────────────────┘
```

---

# 10. Attention Item Ordering

Order attention items according to the analytical priority hierarchy:

```text
P1
↓
P2
↓
P3
```

Within the same priority class, preserve the analytical result ordering.

Do not reorder items solely for visual reasons.

## Number of Visible Items

Default:

```text
Maximum visible items = 3
```

If more than three items exist, explicitly communicate continuation:

```text
Showing 3 of 8 active problems
[ View all problems ]
```

The user should never assume that the three displayed items are the complete set if more items exist.

---

# 11. Empty Attention State

When no attention item matches the current filters, use a compact message:

```text
┌──────────────────────────────────────────────────────────────┐
│ ✓  No active problem matches the current filters.             │
└──────────────────────────────────────────────────────────────┘
```

The empty state must not make the whole Dashboard appear unavailable or broken.

The subsequent Dashboard sections must still be displayed.

---

# 12. Section 2 — CURRENT PLANT CONDITION

## 12.1 Purpose

This section answers:

> **"How is the currently selected scope performing right now?"**

Always make the scope explicit.

Examples:

```text
CURRENT PLANT CONDITION
Scope: All assets
```

or:

```text
CURRENT PLANT CONDITION
Scope: PU-2101B
```

---

# 13. Current Plant Condition Layout

Use three primary KPI cards:

```text
┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
│ Asset Health  ⓘ   │ │ Operating     ⓘ   │ │ Reliability   ⓘ   │
│ Score             │ │ Performance        │ │ & Consequence     │
│                   │ │                    │ │                   │
│     82.4          │ │      94.8          │ │      88.2         │
│     / 100         │ │      / 100         │ │      / 100        │
│                   │ │                    │ │                   │
│ Current asset     │ │ Healthy baseline   │ │ Reliability       │
│ condition         │ │ reference          │ │ context           │
└───────────────────┘ └───────────────────┘ └───────────────────┘
```

These three indicators form the primary condition/decision layer of the Dashboard.

---

# 14. KPI Card — Asset Health Score

## Exact Content

```text
Asset Health Score                 ⓘ

82.4 / 100

Current asset condition
```

## Required Elements

1. KPI label;
2. information icon;
3. KPI value;
4. score range/unit;
5. short interpretation.

## Tooltip

```text
Composite condition score derived from current equipment condition.
Higher values represent healthier current condition.
```

## Label Restrictions

Do not add technical terms such as:

```text
DSS
Decision Index
Probability of Failure
```

to the main KPI label unless they are explicitly required by the analytical definition.

---

# 15. KPI Card — Operating Performance

## Exact Content

```text
Operating Performance            ⓘ

94.8 / 100

Relative to healthy baseline
```

## Tooltip

```text
Normalized operating-performance indicator relative to the asset's healthy baseline.
```

## Visual Behavior

The card remains visually neutral.

When the metric requires attention, add a small semantic cue instead of changing the entire card background.

Example:

```text
94.8 / 100
● Below reference
```

---

# 16. KPI Card — Reliability & Consequence

## Exact Content

```text
Reliability & Consequence        ⓘ

88.2 / 100

Current reliability context
```

## Tooltip

```text
Decision indicator combining current reliability context
and historical consequence information.
```

---

# 17. KPI Number Rules

Primary KPI values should:

- use large, semibold typography;
- use consistent numeric precision;
- use one decimal where one decimal is meaningful and supported;
- show `/ 100` for score/index metrics based on a 0–100 scale;
- avoid unnecessary precision.

Recommended:

```text
82.4 / 100
```

Avoid:

```text
82.423817 / 100
```

The Dashboard is for rapid interpretation rather than raw numerical auditing.

---

# 18. Section 3 — OPERATIONAL CONTEXT

## 18.1 Purpose

This section provides the operational context surrounding the core condition indicators.

It contains:

1. Load Index;
2. Production Index;
3. Downtime — Last 30 Days;
4. Emission Intensity Proxy.

These metrics should be visually lighter than the primary condition cards.

---

# 19. Operational Context Layout

```text
OPERATIONAL CONTEXT

┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ Load Index ⓘ  │ │ Production ⓘ  │ │ Downtime  ⓘ   │ │ Emission     ⓘ │
│               │ │ Index         │ │ Last 30 Days  │ │ Intensity     │
│               │ │               │ │               │ │ Proxy         │
│    118.9      │ │      98.9     │ │      8.0 h    │ │     120.2     │
│               │ │               │ │               │ │               │
│ Relative load │ │ Ref. = 100    │ │ Observed      │ │ Relative proxy │
└───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘
```

---

# 20. Operational Context Card — Load Index

```text
Load Index                     ⓘ

118.9

Relative operating load
```

## Tooltip

```text
Relative operating-load indicator.
A value near 100 represents the reference load level.
```

The card must not visually imply that Load Index is another form of asset health score.

---

# 21. Operational Context Card — Production Index

```text
Production Index                ⓘ

98.9

100 = healthy-running baseline
```

## Tooltip

```text
Current production relative to the measured healthy-running baseline.
A value near 100 represents the reference production level.
```

The baseline explanation is important because the number must be interpretable without requiring the user to already know the metric definition.

---

# 22. Operational Context Card — Downtime

```text
Downtime — Last 30 Days         ⓘ

8.0 h

Observed downtime
```

## Tooltip

```text
Downtime calculated from observed running-status data
in the 30-day window.
```

The unit `h` must always remain visible.

Do not display only:

```text
8.0
```

because the user needs to understand that this is a duration.

---

# 23. Operational Context Card — Emission Intensity Proxy

```text
Emission Intensity Proxy        ⓘ

120.2

Relative electricity-related proxy
```

## Tooltip

```text
Relative electricity-related emission-intensity proxy.
This is not a direct emissions measurement.
```

The word **Proxy** must remain in the primary label.

Do not relabel it as:

```text
CO₂ Emission
Actual Emission
kg CO₂e
```

unless the analytical source explicitly supports such an interpretation.

---

# 24. Section 4 — ASSET STATUS

## 24.1 Purpose

This section answers:

> **"Which assets are currently in what condition?"**

The primary representation should be a **compact comparison table** because the task is to compare multiple assets using exact values and discrete states.

---

# 25. Asset Status Table

## Title

```text
ASSET STATUS
Quick comparison of current condition, health, priority, and forecast risk by asset.
```

## Table

| Asset | Condition | Health | Priority | Forecast |
|---|---|---:|---|---|
| PU-2101B | 🔴 ALARM | 16 | P1 | Attention |
| KO-3201 | 🟡 WATCH | 54 | P2 | Attention |
| PM-4405B | 🟢 NORMAL | 87 | P4 | — |

This table is intentionally compact and decision-oriented.

---

# 26. Asset Status Table — Column Specification

## Column 1 — Asset

Example values:

```text
PU-2101B
KO-3201
PM-4405B
```

### Behavior

The asset identifier should have a clear selection/click affordance.

Conceptual interaction:

```text
PU-2101B
    ↓
Open asset investigation
```

Do not fill the cell with descriptive text unless that description is essential to identify the asset.

---

## Column 2 — Condition

Use a semantic status badge.

Examples:

```text
🔴 ALARM
🟡 WATCH
🟢 NORMAL
⛔ TRIP
⚪ DATA GAP
```

Condition should always include:

- status text;
- semantic icon/cue;
- semantic color.

Do not communicate condition through color alone.

## Condition Vocabulary

| State | Meaning |
|---|---|
| NORMAL | Condition is within normal range |
| WATCH | Early deviation / requires monitoring |
| ALARM | Abnormal condition requiring attention |
| TRIP | Trip-level condition |
| DATA GAP | Condition cannot be reliably assessed from available data |
| NOT OBSERVABLE | Required condition cannot be directly observed |

---

## Column 3 — Health

Recommended format:

```text
16
54
87
```

Use the header:

```text
Health
```

The table should remain compact, so `/ 100` does not need to be repeated in every cell if the header/tooltip defines the scale.

### Header Tooltip

```text
Current Asset Health Score.
Higher values indicate healthier current condition.
```

Do not use large progress bars in this table. Exact numerical comparison is more useful for a multi-asset comparison.

---

## Column 4 — Priority

Use a compact priority badge:

```text
P1
P2
P3
P4
```

Priority styling must be distinct from Condition styling.

Example:

```text
Condition    🔴 ALARM
Priority     [ P1 ]
```

Do not make the two concepts visually identical.

---

## Column 5 — Forecast

Use a concise forecast-risk/status label:

```text
Attention
```

or:

```text
—
```

Example:

| Asset | Condition | Health | Priority | Forecast |
|---|---|---:|---|---|
| PU-2101B | 🔴 ALARM | 16 | P1 | Attention |
| PM-4405B | 🟢 NORMAL | 87 | P4 | — |

Do not place the complete forecast time series inside a table cell.

The detailed forecast belongs in asset investigation.

---

# 27. Asset Status Table — Fields Excluded from the Primary Table

Do not add these columns to the default Asset Status table:

```text
Load
Downtime
Observed Coverage
Source
Model
Provenance
```

These fields are secondary or technical information and would significantly increase scanning effort.

The default table should remain:

```text
Asset | Condition | Health | Priority | Forecast
```

---

# 28. Asset Status — Interaction

When an asset is selected from the table, preserve the asset context when opening the detailed asset investigation.

Conceptually:

```text
Asset Status
     ↓
PU-2101B
     ↓
Asset Investigation
```

The user should not have to re-select the same asset unnecessarily.

---

# 29. Section 5 — TREND ANALYSIS

## 29.1 Purpose

Trend Analysis answers:

> **"How are the indicators changing over time?"**

The primary representation is a line chart.

The Dashboard should use the chart to communicate patterns and direction rather than force users to inspect a large numerical table.

---

# 30. Trend Analysis Control Area

Use two control levels.

## Control 1 — Trend Group

```text
Trend group

(●) Condition & Reliability    (○) Operations
```

## Control 2 — Indicator

```text
Indicator

[ Asset Health Score ▼ ]
```

These controls should sit directly above the chart.

---

# 31. Trend Group — Condition & Reliability

Available metrics:

```text
Asset Health Score
Operating Performance Index
Reliability & Consequence Index
```

Recommended Y-axis:

```text
Index (0–100)
```

Conceptual layout:

```text
┌──────────────────────────────────────────────────────────────┐
│ TREND ANALYSIS                                               │
│                                                              │
│ Trend group                                                  │
│ [● Condition & Reliability] [ Operations ]                   │
│                                                              │
│ Indicator                                                    │
│ [ Asset Health Score ▼ ]                                     │
│                                                              │
│ 100 ┤                                                       │
│  90 ┤      ╭────╮                   ╭────                   │
│  80 ┤──────╯    ╰──────╮────────────╯                       │
│  70 ┤                  ╰────                                 │
│  60 ┤                                                       │
│     └─────────────────────────────────────────────────────  │
│       01 Sep     08 Sep     15 Sep     22 Sep     29 Sep   │
└──────────────────────────────────────────────────────────────┘
```

---

# 32. Trend Group — Operations

Available metrics:

```text
Load Proxy Index
Production Index
Relative Energy Intensity
```

Recommended Y-axis:

```text
Relative index
```

Do not mix these metrics with condition metrics on the same semantic axis.

---

# 33. Trend Time Representation

The chart must use a clear date/time axis.

Conceptually:

```text
Historical                Current
───────────────|────────────────────
               ↑
       analysis reference time
```

The user must be able to distinguish:

- historical values;
- current/reference point;
- forecast information, where included.

Forecast information should not visually mimic measured historical observations.

---

# 34. Trend Chart — Scope Behavior

## When Scope = All Assets

The chart may contain multiple asset lines:

```text
PU-2101B ───────────
KO-3201  ───────────
PM-4405B ───────────
```

Requirements:

- each asset must be clearly identifiable;
- legend labels must use exact asset identifiers;
- the chart must remain readable;
- the user must be able to focus on a selected asset where supported.

## When Scope = Single Asset

Example:

```text
Scope: PU-2101B
```

The chart should display only the selected asset's series.

A large legend is unnecessary when only one series exists.

---

# 35. Trend Chart — Data Density

For Dashboard-level trend visualization, use a readable aggregation level rather than displaying excessive raw observations.

Recommended conceptual flow:

```text
Raw observations
      ↓
Daily aggregation
      ↓
Trend line
```

The Dashboard is intended to reveal direction and pattern, not to function as a raw-data browser.

---

# 36. Trend Chart — Required Interactions

## Change Metric

The user must be able to select the indicator from the appropriate metric group.

Example:

```text
[ Asset Health Score ▼ ]
```

Options for Condition & Reliability:

```text
Asset Health Score
Operating Performance Index
Reliability & Consequence Index
```

Options for Operations:

```text
Load Proxy Index
Production Index
Relative Energy Intensity
```

## Inspect Exact Point

Hovering over the chart should provide exact point information.

Example:

```text
Date: 29 Sep 2026
Asset: PU-2101B
Asset Health Score: 82.4
```

This allows exact-value lookup without filling the default Dashboard with another large table.

---

# 37. Trend Chart — Visual Rules

Use the following distinctions:

| Data Type | Visual Treatment |
|---|---|
| Measured values | Solid line |
| Current/reference point | Clearly marked point/reference marker |
| Reconstructed values | Differentiated line pattern |
| Forecast | Visually different line pattern |
| Forecast uncertainty | Translucent uncertainty band, when available |
| Alarm limit | Clearly identifiable reference line |
| Trip limit | Clearly identifiable reference line |

Do not rely on color alone to distinguish these states.

---

# 38. Trend Chart — Unnecessary Controls

The chart should not be dominated by a large number of toolbar controls.

Keep only interactions that support routine monitoring and basic inspection, such as:

```text
Hover
Zoom
Reset View
```

Avoid exposing irrelevant controls that compete with the actual data visualization.

---

# 39. Dashboard Spacing

Use clear separation between semantic groups.

Recommended conceptual spacing:

```text
HEADER
↓ 24 px

ATTENTION REQUIRED
↓ 28 px

CURRENT PLANT CONDITION
↓ 28 px

OPERATIONAL CONTEXT
↓ 28 px

ASSET STATUS
↓ 28 px

TREND ANALYSIS
```

The exact CSS spacing may be tuned during implementation, but each section must remain visually distinct.

---

# 40. Dashboard Visual Hierarchy

Not every component should have equal visual weight.

## Primary Layer

```text
Attention Required

Asset Health Score
Operating Performance
Reliability & Consequence
```

These components should receive the strongest emphasis.

## Secondary Layer

```text
Load Index
Production Index
Downtime
Emission Intensity Proxy
```

These should be more compact and visually restrained.

## Comparison Layer

```text
Asset Status
```

This should prioritize scanability over decoration.

## Analytical Context Layer

```text
Trend Analysis
```

This should focus on trend readability rather than decorative chart design.

---

# 41. Dashboard Information Visibility

## Always Visible

The Dashboard should always show:

```text
Scope
Analysis reference time
Data status
Attention items
Core condition KPIs
Operational context
Asset status
Trend analysis
```

## Tooltip / On-Demand Information

Use tooltips for:

```text
KPI definitions
Baseline explanations
Proxy definitions
Metric interpretation
```

## Not Displayed Directly on the Dashboard

Keep these out of the primary Dashboard content:

```text
MAE
RMSE
Model details
Provenance
Four-P
Four-M
CAPA
Detailed RCA evidence
Historical incident evidence
Detailed follow-up history
Engine execution diagnostics
```

---

# 42. Dashboard Filter Consistency

Any dashboard-level filter must apply consistently across all sections.

Relevant filters:

```text
Asset scope
Priority
Ticket status
Attention-only filter
```

The filtered context must remain synchronized across:

```text
Attention Required
        ↓
Current Plant Condition
        ↓
Operational Context
        ↓
Asset Status
        ↓
Trend Analysis
```

The user must not see conflicting scopes between sections.

---

# 43. Single-Asset Scope Behavior

When the selected scope is:

```text
Scope: PU-2101B
```

the Dashboard should become asset-focused.

## Attention Required

Show only attention items associated with `PU-2101B`.

## Current Plant Condition

Show the KPI values for `PU-2101B`.

## Operational Context

Show the available operational context for `PU-2101B`.

## Asset Status

Show the row for `PU-2101B`.

## Trend Analysis

Show the trend for `PU-2101B`.

The Dashboard must not silently show plant-level values while the interface says a single asset is selected.

---

# 44. All-Asset Scope Behavior

When the selected scope is:

```text
Scope: All assets
```

the Dashboard should show:

### Current Plant Condition

Aggregated scope-level KPI values according to the analytical output.

### Operational Context

Aggregated/selected-scope operational metrics according to the analytical output.

### Asset Status

All assets in the selected scope.

### Trend Analysis

The user may compare multiple assets where supported.

The scope label must remain visible so the user knows whether a value is plant-level or asset-level.

---

# 45. Data Quality State Handling

The Dashboard must provide clear handling for the data-quality states supported by the analytical output.

Examples:

```text
● Data status: PASS
```

```text
⚠ Data status: CHECK
```

```text
✕ Data status: FAIL
```

If a particular metric cannot reliably be shown, do not present a fabricated zero.

Prefer:

```text
—
```

or, where useful:

```text
Data unavailable
```

The visual treatment must communicate that the value is unavailable rather than numerically zero.

---

# 46. Status Accessibility

Critical states must not rely on color alone.

Correct:

```text
🔴 ALARM
```

Incorrect:

```text
[red background only]
```

Priority must also be text-based:

```text
P1
```

rather than relying only on a red border/background.

Measured, reconstructed, and forecast information should also differ through line style/pattern or other non-color cues where practical.

---

# 47. Visual Design System

## Background

```text
#F0F4F9
```

## Surface / Cards

```text
#FFFFFF
```

## Border

```text
#D9E1EA
```

## Main Dark Blue

```text
#0C2F7A
```

## Primary Blue

```text
#1A5CC8
```

## Accent Turquoise

```text
#4DD4C8
```

Use status colors only for semantic operational meaning.

---

# 48. Typography

Recommended scale:

| Element | Size |
|---|---:|
| Page title | 24–28 px |
| Section heading | 18–21 px |
| Card title | 14–16 px |
| Body text | 14–16 px |
| Helper text | 12–13 px |
| KPI value | 28–40 px |

### Typography Hierarchy

```text
Page Title
    ↓
Section Heading
    ↓
Card Title
    ↓
KPI Value / Main Content
    ↓
Supporting Text
```

Use semibold/bold only where hierarchy requires it. Avoid excessive bolding.

---

# 49. Card Design Rules

All Dashboard cards should use a consistent component language:

- white surface;
- thin border;
- small-to-medium radius;
- subtle shadow;
- sufficient internal padding;
- consistent heading placement;
- consistent icon placement;
- consistent status treatment.

Avoid:

- large gradients;
- excessive rounded "marketing SaaS" styling;
- multiple decorative icons per card;
- bright backgrounds for every KPI;
- heavy drop shadows.

---

# 50. Complete Dashboard Wireframe

The overall screen should conceptually look like this:

```text
┌──────────────────────────────────────────────────────────────────────┐
│ CALI-INI                                                             │
│ Intelligent Manufacturing Decision Support                           │
│                                                                      │
│ Scope: All assets     As of: 03 Oct 2026, 12:00     ● Data PASS     │
└──────────────────────────────────────────────────────────────────────┘


ATTENTION REQUIRED
3 items require attention

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ P1           │  │ P2           │  │ P3           │
│      1       │  │      1       │  │      1       │
└──────────────┘  └──────────────┘  └──────────────┘


┌──────────────────────────────────────────────────────────────────────┐
│ P1 · PU-2101B                                                        │
│                                                                      │
│ High discharge pressure deviation                                   │
│ 🔴 ALARM    Ticket: OPEN                                            │
│                                                                      │
│ NEXT ACTION                                                          │
│ Inspect discharge pressure / control condition                       │
│                                                    [ View problem ]  │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ P2 · KO-3201                                                         │
│                                                                      │
│ Abnormal operating condition                                        │
│ 🟡 WATCH    Ticket: OPEN                                            │
│                                                                      │
│ NEXT ACTION                                                          │
│ Monitor parameter trend                                              │
│                                                    [ View problem ]  │
└──────────────────────────────────────────────────────────────────────┘


CURRENT PLANT CONDITION
Scope: All assets

┌──────────────────────┐ ┌──────────────────────┐ ┌───────────────────┐
│ Asset Health Score ⓘ │ │ Operating Perf.  ⓘ │ │ Reliability &  ⓘ │
│                      │ │                      │ │ Consequence       │
│      82.4 / 100      │ │      94.8 / 100      │ │     88.2 / 100    │
│ Current condition    │ │ Healthy baseline     │ │ Reliability ctx.  │
└──────────────────────┘ └──────────────────────┘ └───────────────────┘


OPERATIONAL CONTEXT

┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ Load Index  ⓘ  │ │ Production ⓘ   │ │ Downtime  ⓘ   │ │ Emission     ⓘ │
│                │ │                │ │                │ │ Proxy           │
│    118.9       │ │     98.9       │ │      8.0 h     │ │     120.2       │
│ Relative load  │ │ Ref. = 100     │ │ Last 30 days   │ │ Relative proxy  │
└────────────────┘ └────────────────┘ └────────────────┘ └────────────────┘


ASSET STATUS
Quick comparison of current condition, health, priority, and forecast risk by asset.

┌──────────┬────────────┬────────┬──────────┬──────────┐
│ Asset    │ Condition  │ Health │ Priority │ Forecast │
├──────────┼────────────┼────────┼──────────┼──────────┤
│ PU-2101B │ 🔴 ALARM   │ 16     │ P1       │ Attention│
│ KO-3201  │ 🟡 WATCH   │ 54     │ P2       │ Attention│
│ PM-4405B │ 🟢 NORMAL  │ 87     │ P4       │ —        │
└──────────┴────────────┴────────┴──────────┴──────────┘


TREND ANALYSIS

Trend group
[ ● Condition & Reliability ] [ Operations ]

Indicator
[ Asset Health Score ▼ ]

┌──────────────────────────────────────────────────────────────────────┐
│ 100 ┤                                                               │
│  90 ┤      ╭────╮                   ╭────                           │
│  80 ┤──────╯    ╰──────╮────────────╯                               │
│  70 ┤                  ╰────                                         │
│  60 ┤                                                               │
│    └───────────────────────────────────────────────────────────────   │
│      01 Sep     08 Sep     15 Sep     22 Sep     29 Sep             │
│                                                                      │
│                         Time →                                       │
└──────────────────────────────────────────────────────────────────────┘
```

---

# 51. Dashboard Component Inventory

The Dashboard consists of the following components only:

```text
1. Header / Snapshot Bar

2. Attention Summary
   ├── P1 Count
   ├── P2 Count
   └── P3 Count

3. Attention Problem Card
   ├── Priority
   ├── Asset
   ├── Problem / Trigger
   ├── Condition
   ├── Ticket
   ├── Next Action
   └── View Problem

4. Current Plant Condition
   ├── Asset Health Score
   ├── Operating Performance
   └── Reliability & Consequence

5. Operational Context
   ├── Load Index
   ├── Production Index
   ├── Downtime — Last 30 Days
   └── Emission Intensity Proxy

6. Asset Status Table
   ├── Asset
   ├── Condition
   ├── Health
   ├── Priority
   └── Forecast

7. Trend Analysis
   ├── Trend Group Selector
   ├── Indicator Selector
   └── Line Chart
```

---

# 52. Dashboard Decision Logic

The Dashboard should produce the following user-understanding sequence:

```text
SEE ANOMALY
      ↓
IDENTIFY AFFECTED ASSET
      ↓
SEE CURRENT CONDITION
      ↓
UNDERSTAND OPERATIONAL CONTEXT
      ↓
COMPARE ASSETS
      ↓
CHECK TREND
      ↓
DECIDE WHETHER TO INVESTIGATE
```

The Dashboard therefore functions as:

```text
WHAT MATTERS NOW?
        ↓
WHERE?
        ↓
HOW SEVERE?
        ↓
HOW IS IT CHANGING?
        ↓
WHAT SHOULD I OPEN NEXT?
```

Detailed investigation should begin only after the user chooses an issue or asset to investigate.

---

# 53. Final Dashboard Design Principle

The Dashboard should remain a **decision-first operational snapshot**.

It should show enough information for the user to identify what matters, understand the immediate context, compare assets, and recognize trends — while keeping technical detail available without overwhelming the first-glance experience.

The final visual hierarchy is:

```text
ATTENTION REQUIRED
        ↓
CURRENT PLANT CONDITION
        ↓
OPERATIONAL CONTEXT
        ↓
ASSET STATUS
        ↓
TREND ANALYSIS
```

The key design rule is:

> **Make the important information immediately detectable, keep related information physically close, use the appropriate representation for each task, and expose technical detail only when it is needed.**
