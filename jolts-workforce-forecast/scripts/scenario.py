import sys, warnings, pandas as pd, numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
warnings.filterwarnings("ignore")
src, out = sys.argv[1], sys.argv[2]
HIRES, COST = 100, 10000            # ASSUMPTIONS: hires needed per month; cost per open role per month
df = pd.read_csv(src, dtype={"industry_code": str}, parse_dates=["date"])
d = df[(df.type=="level_thousands") & df.measure_code.isin(["JO","HI"])]
def fc(s, smooth):
    s = np.log(s)
    if smooth: s = s.rolling(3, min_periods=1).median()
    return np.exp(ExponentialSmoothing(s.values, trend="add", damped_trend=True).fit().forecast(6))
rows = []
for code, name, sm, band in [("000000","Total nonfarm",False,0.030),("520000","Finance and insurance",True,0.107)]:
    w = d[d.industry_code==code].pivot(index="date", columns="measure_code", values="value").dropna()
    y = w.HI/w.JO
    f = (fc(w.HI,sm)/fc(w.JO,sm)).mean()
    sc = {"Now (Aug 2026)": y.iloc[-1], "Model forecast, next 6 mo avg": f,
          "Forecast minus backtest error": f-band, "Forecast plus backtest error": f+band,
          "Stress: 2022 low": y["2022-01":"2023-12"].min(), "Pre-2020 average": y[:"2019-12"].mean()}
    for k, r in sc.items():
        roles = HIRES/r
        rows.append((name, k, round(r,2), round(roles), round(roles*COST)))
t = pd.DataFrame(rows, columns=["series","scenario","hires_per_opening","open_roles_needed","monthly_vacancy_cost_usd"])
t.to_csv(out, index=False); print(t.to_string(index=False))
