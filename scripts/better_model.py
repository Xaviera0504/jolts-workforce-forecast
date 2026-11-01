import sys, warnings, pandas as pd, numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
warnings.filterwarnings("ignore")
src, base, out = sys.argv[1], sys.argv[2], sys.argv[3]
df = pd.read_csv(src, dtype={"industry_code": str}, parse_dates=["date"])
d = df[(df.type=="level_thousands") & df.measure_code.isin(["JO","HI"])]
H, NORIG = 6, 36

def fc(s, smooth):
    s = np.log(s)
    if smooth: s = s.rolling(3, min_periods=1).median()
    m = ExponentialSmoothing(s.values, trend="add", damped_trend=True).fit()
    return np.exp(m.forecast(H))

rows = []
for code, name in [("000000","Total nonfarm"),("520000","Finance and insurance")]:
    w = d[d.industry_code==code].pivot(index="date", columns="measure_code", values="value").dropna()
    y = w.HI/w.JO; n = len(y)
    for o in range(n-H-NORIG, n-H):
        hi, jo = w.HI.iloc[:o+1], w.JO.iloc[:o+1]
        for tag, sm in [("ets", False), ("ets_smooth", True)]:
            f = fc(hi, sm)/fc(jo, sm)
            for h in range(1, H+1):
                rows.append((name, y.index[o], h, tag, f[h-1], y.iloc[o+h]))
r = pd.DataFrame(rows, columns=["series","origin","h","model","forecast","actual"])
r["err"] = (r.forecast-r.actual).abs()
r.to_csv(out, index=False)
b = pd.read_csv(base)
tab = r.groupby(["series","model"]).err.mean().unstack()
bt = b.groupby("series")[["err_naive","err_avg12"]].mean()
print(pd.concat([bt, tab], axis=1).round(3))
print()
print(r.groupby(["series","model","h"]).err.mean().unstack("h").round(3))
