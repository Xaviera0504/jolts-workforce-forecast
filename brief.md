# Are job openings turning into hires? A 6-month view

**For:** a recruiting or workforce-planning lead. **Data:** BLS JOLTS, seasonally adjusted, through Aug 2026 (downloaded Nov 1, 2026; BLS revises past months).

## The question
For every job opening, how many hires does the market produce, and where is that headed over the next 6 months?

## The answer
- **Total nonfarm: stable and low.** 0.73 hires per opening today, versus a 2000–2019 average of 1.17. The forecast for the next 6 months is about 0.72.
- **Finance and insurance: lower and much less certain.** 0.31 today, versus a 2000–2019 average of 0.67. The forecast is about 0.37, with a wide range (0.26 to 0.48).

## What it means for a hiring plan
A hypothetical company needs 100 hires a month. The open roles it must carry:

| Scenario | Total nonfarm | Finance and insurance |
|---|---|---|
| Model forecast | 138 | 269 |
| Forecast, low end of range | 144 | 378 |
| Forecast, high end of range | 133 | 209 |
| Stress (lowest ratio in 2022–23) | 186 | 469 |

Planning rule: for total nonfarm, plan on about 140 open roles per 100 hires. For finance and insurance, plan to the low end of the range, about 380, and review monthly. At an assumed $10,000 per open role per month, the spread in finance and insurance (209 to 378 roles) is about $1.7 million a month. The $10,000 is an assumption, not data.

## How reliable is the forecast?
I tested every method by hiding the last 36 months and forecasting 6 months ahead each time. Average error, in hires per opening:

| Series | "Same as now" | 12-month average | Time-series model |
|---|---|---|---|
| Total nonfarm | 0.032 | 0.040 | 0.030 |
| Finance and insurance | 0.132 | 0.107 | 0.107 |

The model barely beats the simple rules. For total nonfarm the forecast is off by about 4% of the level; for finance and insurance, about 24%. History alone does not predict this ratio well, so treat the ranges as the finding.

## Limits
- National and industry-level data. It has no employer-level information, and the company above is hypothetical.
- A low ratio means openings are not turning into hires. It does not prove roles are hard to fill, because some openings are never filled.
- Finance and insurance monthly figures are noisy (for example, Dec 2025 shows 129k openings against roughly 300k in neighboring months).
- The same test window was used to compare two model variants, so small gaps between methods should not be over-read.

*All numbers come from the code in this repo. This brief was written from those outputs.*
