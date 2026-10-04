# Cali-INI — Design System, Color Palette & Logo Guide

> **Purpose:** visual reference for redesigning the existing Cali-INI interface without changing the analytical logic.
>
> **Source references:** the provided Selection Process visual and Chandra Asri logo.

---

## 1. Design Direction

Cali-INI should feel like an **industrial monitoring and decision-support application**: professional, calm, technical, trustworthy, and easy to scan.

The visual language should combine:

- **Deep corporate blue** for structure, headings, navigation, and trust.
- **Medium blue** for interactive elements and analytical emphasis.
- **Turquoise/cyan** for active states, positive emphasis, and visual continuity.
- **Very light blue-gray** for the application background.
- **White** for cards and content surfaces.

The interface should avoid looking like a generic SaaS dashboard. It should feel closer to an **industrial control / engineering decision-support interface**, while remaining clean and approachable.

---

# 2. Brand / Logo Reference

The supplied logo is the **Chandra Asri** logo.

The logo consists of:

1. A spherical icon made from layered curved bands.
2. The Chandra Asri wordmark.
3. A three-color blue/cyan visual identity.

### Logo colors observed

| Color | Hex | RGB | Recommended role |
|---|---|---|---|
| Deep Blue | `#243F7A` | 36, 63, 122 | Primary brand / logo |
| Medium Blue | `#2477B9` | 36, 119, 185 | Secondary brand |
| Cyan | `#4BC0D5` | 75, 192, 213 | Accent / highlight |

### Logo usage

**Preferred:**
- Use the full Chandra Asri logo in the application header or login/landing area.
- Keep sufficient whitespace around the logo.
- Preserve the original proportions.
- Use the supplied logo asset rather than redrawing it.

**Avoid:**
- Stretching horizontally or vertically.
- Recoloring the logo.
- Placing it over visually noisy backgrounds.
- Using very small sizes where the sphere details become unreadable.

### Recommended placement

For the main application:

```text
┌──────────────────────────────────────────────────────┐
│ [Chandra Asri logo]        Cali-INI                  │
│                           Intelligent Manufacturing   │
│                           Decision Support            │
└──────────────────────────────────────────────────────┘
```

The Chandra Asri logo should communicate the corporate context; **Cali-INI** should remain the product/application name.

---

# 3. Primary UI Color Palette

The supplied Selection Process visual provides the strongest reference for the UI palette.

## Primary colors

| Token | Hex | Usage |
|---|---|---|
| `--primary-dark` | `#0C2F7A` | Main headings, major navigation, primary text emphasis |
| `--primary-blue` | `#1A5CC8` | Buttons, links, selected states, active navigation |
| `--primary-navy` | `#1A3A6E` | Secondary headings, supporting dark text |
| `--accent-turquoise` | `#4DD4C8` | Accent, selected step, positive/active visual cue |
| `--brand-blue` | `#2477B9` | Secondary brand treatment |
| `--brand-cyan` | `#4BC0D5` | Brand accent / decorative highlight |

## Neutral colors

| Token | Hex | Usage |
|---|---|---|
| `--background` | `#F0F4F9` | Main application background |
| `--surface` | `#FFFFFF` | Cards, panels, tables |
| `--border` | `#D9E1EA` | Card borders, separators |
| `--text-primary` | `#17345F` | Main body text |
| `--text-secondary` | `#5F6F85` | Supporting text |
| `--text-muted` | `#8A94A3` | Metadata, timestamps, helper text |

### General rule

Use the palette with this approximate hierarchy:

```text
60%  Light background / white surfaces
25%  Deep + medium blues
10%  Secondary blue
5%   Turquoise accent
```

Do not turn the interface into a rainbow dashboard. Status colors should be reserved for operational meaning.

---

# 4. Status Colors

Status colors are **semantic**, not decorative.

The existing Cali-INI logic distinguishes equipment condition from ticket state and action status. The visual system should preserve this distinction.

## Equipment condition

| Condition | Visual treatment | Meaning |
|---|---|---|
| NORMAL | Green semantic status | Condition is within normal range |
| WATCH | Amber semantic status | Early deviation / needs monitoring |
| ALARM | Red semantic status | Abnormal condition requiring attention |
| TRIP | Dark red / critical semantic status | Trip-level condition |
| DATA GAP | Gray / neutral | Condition cannot be reliably assessed from available data |
| NOT OBSERVABLE | Gray / neutral | Required condition cannot be directly observed |

### Important

Do **not** use the primary brand turquoise as the only meaning for “normal”. Turquoise is a brand accent; operational status should remain semantically recognizable.

---

# 5. Priority Colors

Priority and condition should be visually distinct.

| Priority | Recommended treatment |
|---|---|
| P1 | Strong red emphasis |
| P2 | Orange/amber emphasis |
| P3 | Blue emphasis |
| P4 | Gray/neutral emphasis |

The exact shades may be tuned during implementation, but the visual hierarchy must clearly communicate that **P1 is more urgent than P4** without making the entire dashboard visually aggressive.

---

# 6. Typography

The supplied visual uses a bold modern sans-serif style.

Recommended typography:

### Headings
- Bold / semibold sans-serif
- Strong visual hierarchy
- Dark blue rather than pure black

### Body
- Regular sans-serif
- Comfortable line height
- Dark navy/blue-gray rather than black

### KPI values
- Large
- Semibold
- Minimal decoration

### Suggested scale

| Element | Suggested size |
|---|---:|
| App title | 24–30 px |
| Page title | 24–28 px |
| Section heading | 18–21 px |
| Card title | 14–16 px |
| Body text | 14–16 px |
| Helper text | 12–13 px |
| KPI number | 28–40 px |

---

# 7. UI Component Language

## Cards

Use:
- White surface
- Thin light border
- Small corner radius
- Very subtle shadow
- Generous internal padding

Avoid:
- Heavy shadows
- Excessive gradients
- Highly rounded “marketing SaaS” cards
- Bright colored backgrounds for every KPI

### Example

```text
┌──────────────────────────────┐
│ Asset Health Score       ⓘ   │
│                              │
│ 82.4 / 100                   │
│ Current asset condition      │
└──────────────────────────────┘
```

---

# 8. Dashboard KPI Hierarchy

Do not make every metric look equally important.

## Tier 1 — Core condition / decision indicators

- Asset Health Score
- Operating Performance
- Reliability & Consequence

These can use the strongest card treatment.

## Tier 2 — Operational context

- Load Index
- Production Index
- Downtime
- Emission Intensity Proxy

These should be visually lighter and more compact.

### Principle

```text
CORE CONDITION
        ↓
OPERATIONAL CONTEXT
```

This distinction prevents the user from interpreting every index as another version of “equipment health”.

---

# 9. Dashboard Layout Direction

Recommended top-to-bottom hierarchy:

```text
HEADER
│
├── Scope + Analysis Reference Time + Data Status
│
├── ATTENTION REQUIRED
│
├── CURRENT PLANT CONDITION
│
├── OPERATIONAL CONTEXT
│
├── ASSET STATUS
│
└── TREND ANALYSIS
```

The most important information should appear before supporting technical details.

---

# 10. Sidebar Style

The sidebar should feel like a **control panel**, not a second dashboard.

Recommended groups:

```text
VIEW
  Asset scope

PROBLEM FILTERS
  Priority
  Ticket status
  Show only items requiring attention

──────────────

ADVANCED
  Source workbook
  Refresh analysis

HELP
  Terminology
```

### Visual rules

- Keep section labels small and uppercase/semibold.
- Use the primary blue for selected controls.
- Do not use multiple accent colors inside the sidebar.
- Hide technical configuration under Advanced when possible.

---

# 11. Problem UI

The Problem page is an operational worklist.

Prioritize:

1. What happened?
2. Where?
3. How severe?
4. What is the likely cause?
5. What should be done?
6. Who is responsible?
7. What is the current action status?

### Recommended visual order

```text
PROBLEM
  ↓
CONDITION + PRIORITY
  ↓
WHY WAS IT RAISED?
  ↓
LIKELY CAUSE
  ↓
EVIDENCE STRENGTH
  ↓
RECOMMENDED ACTION
  ↓
OWNER + SLA
  ↓
FOLLOW-UP
  ↓
HISTORY
```

Detailed RCA evidence such as historical cases, Four-P, Four-M, CAPA, and provenance should use collapsible/secondary sections.

---

# 12. Asset UI

The Asset page is for investigation.

Recommended hierarchy:

```text
ASSET SUMMARY
│
├── Current condition
├── Health score
├── Priority
└── Latest data
│
PARAMETERS
│
├── Current value
├── Condition
└── Unit
│
TREND & FORECAST
│
├── Historical values
├── Current point
├── Forecast
├── Uncertainty range
└── Alarm / Trip limits
│
4-WEEK OUTLOOK
```

Full technical provenance, model details, validation metrics, and lineage should be available but visually secondary.

---

# 13. Chart Style

Charts should be clean and analytical.

### Historical trend

- Solid line for measured values.
- Clearly marked current/reference point.
- Reconstructed values, when present, should use a differentiated line pattern.
- Forecast should use a visually different line pattern.
- Forecast uncertainty should use a translucent range/band.
- Alarm and trip limits should be clearly distinguishable.

### Avoid

- 3D charts
- decorative gradients
- excessive markers
- unnecessary legends
- too many simultaneous series

---

# 14. Icons

Recommended style:

- Simple outline icons
- Consistent stroke width
- Blue/gray base
- Semantic colors only for status

Examples:

| Function | Icon concept |
|---|---|
| Dashboard | Grid / dashboard |
| Problems | Alert triangle / notification |
| Assets | Gear / equipment |
| Forecast | Line chart / trend |
| Settings | Gear |
| Help | Circle with question mark |
| Technical details | Sliders / database |

Do not mix filled and outlined icon families randomly.

---

# 15. Buttons

### Primary action

Use `--primary-blue`.

Examples:
- View problem
- View asset
- Save update

### Secondary action

White background + blue border.

Examples:
- View evidence
- View technical details
- View history

### Destructive / critical action

Use semantic red only when the action itself is consequential.

Do not use red just because the page contains an alarm.

---

# 16. Labels & Language

Prefer user-oriented wording.

| Current wording | Recommended |
|---|---|
| Plant-wide decision indicators | Current Plant Condition |
| Thirty-day decision-index trends | Trend Analysis |
| Active Problem Tank | Attention Required |
| Asset Condition Overview | Asset Status |
| Energy-related Load Outlook | Forecast / Operational Outlook |
| Root-cause analysis indication | Likely Cause |
| How these indicators are calculated... | Methodology / How this is calculated |
| Data and Model Quality | Technical Details / Data Quality |

The terminology should tell the user **what they can learn or do**, rather than how the backend is structured.

---

# 17. Tooltip Rules

Use tooltips for terms that need precision but do not deserve a permanent paragraph.

Good tooltip examples:

### Asset Health Score
> Composite indicator derived from current equipment condition. Higher values indicate healthier current condition.

### Production Index
> Current production relative to the measured healthy-running baseline. 100 represents the baseline.

### Emission Intensity Proxy
> Relative electricity-related emission indicator derived from available data. This is not a direct emissions measurement.

### Ticket State
> Lifecycle status of the problem ticket.

### Action Status
> Progress of the follow-up action.

Keep tooltips to **1–2 concise sentences**.

---

# 18. Data / Technical Details

Technical information should use progressive disclosure.

### Default view

```text
Forecast quality: ✓ Backtested
Data source: Measured
Data age: 1 h
```

### Expand for details

```text
Model
MAE
RMSE
Validation method
Provenance
Source
Data-quality findings
```

This preserves transparency without overwhelming the primary workflow.

---

# 19. Recommended Visual Personality

The overall personality should be:

**Professional**
- structured
- precise
- restrained

**Industrial**
- strong hierarchy
- operational states clearly visible
- engineering information easy to scan

**Modern**
- clean cards
- generous whitespace
- simple charts
- minimal visual noise

**Trustworthy**
- clear source/quality cues
- no fake precision
- explicit “proxy” labels where appropriate
- clear distinction between measured, estimated, reconstructed, and forecast values

---

# 20. Logo + Product Naming

Use:

### Primary
**Cali-INI**

### Descriptor
**Intelligent Manufacturing Decision Support**

### Corporate context
**Chandra Asri**

Suggested header arrangement:

```text
[ Chandra Asri logo ]

Cali-INI
Intelligent Manufacturing Decision Support
```

The application name should remain visually dominant on the product interface while the corporate logo establishes organizational context.

---

# 21. Design Tokens — Copy/Paste Reference

```css
:root {
  /* Brand / primary */
  --primary-dark: #0C2F7A;
  --primary-blue: #1A5CC8;
  --primary-navy: #1A3A6E;

  /* Brand secondary */
  --brand-blue: #2477B9;
  --brand-cyan: #4BC0D5;
  --accent-turquoise: #4DD4C8;

  /* Surfaces */
  --background: #F0F4F9;
  --surface: #FFFFFF;
  --border: #D9E1EA;

  /* Typography */
  --text-primary: #17345F;
  --text-secondary: #5F6F85;
  --text-muted: #8A94A3;
}
```

---

# 22. Visual Assets

The provided source images are preserved alongside this specification:

- `Cali_INI_logo_reference.png` — supplied Chandra Asri logo.
- `Cali_INI_visual_reference.png` — supplied Selection Process visual used as the main UI color/style reference.

Use these assets as visual references during implementation.

---

# 23. Final Design Principle

Cali-INI should follow:

> **Dashboard tells the user WHAT matters.**
>
> **Problem / Asset pages explain WHY.**
>
> **Technical details show HOW.**

The interface should always prioritize the user's operational question over the underlying data structure.

