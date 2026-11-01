import sys, warnings, pandas as pd, numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
warnings.filterwarnings("ignore")
src, out = sys.argv[1], sys.argv[2]
df = pd.read_csv(src, dtype={"industry_code": str}, parse_dates=["date"])
d = df[(df.type=="level_thousands") & df.measure_code.isin(["JO","HI"])]
def fc(s, smooth):
    s = np.log(s)
    if smooth: s = s.rolling(3, min_periods=1).median()
    return np.exp(ExponentialSmoothing(s.values, trend="add", damped_trend=True).fit().forecast(6))
rows = []
for code, name, sm in [("000000","Total nonfarm",False),("520000","Finance and insurance",True)]:
    w = d[d.industry_code==code].pivot(index="date", columns="measure_code", values="value").dropna()
    hi, jo = fc(w.HI, sm), fc(w.JO, sm)
    last = w.index[-1]
    for h in range(6):
        m = (last + pd.DateOffset(months=h+1)).strftime("%Y-%m")
        rows.append((name, m, h+1, round(hi[h]), round(jo[h]), round(hi[h]/jo[h], 3), last.strftime("%Y-%m")))
t = pd.DataFrame(rows, columns=["series","month","horizon","hires_forecast_k","openings_forecast_k","hires_per_opening_forecast","data_through"])
t.to_csv(out, index=False); print(t.to_string(index=False))
