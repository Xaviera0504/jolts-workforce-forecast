import sys, pandas as pd, numpy as np
src, out = sys.argv[1], sys.argv[2]
df = pd.read_csv(src, dtype={"industry_code": str}, parse_dates=["date"])
d = df[(df.type=="level_thousands") & df.measure_code.isin(["JO","HI"])]
H, NORIG = 6, 36
res = []
for code, name in [("000000","Total nonfarm"),("520000","Finance and insurance")]:
    w = d[d.industry_code==code].pivot(index="date", columns="measure_code", values="value")
    y = (w.HI/w.JO).dropna()
    n = len(y)
    origins = range(n-H-NORIG, n-H)           # last 36 origins with full 6-month horizon
    for o in origins:
        hist = y.iloc[:o+1]
        f_naive = hist.iloc[-1]
        f_avg12 = hist.iloc[-12:].mean()
        for h in range(1, H+1):
            a = y.iloc[o+h]
            res.append((name, y.index[o], h, a, f_naive, f_avg12))
r = pd.DataFrame(res, columns=["series","origin","h","actual","naive","avg12"])
r["err_naive"] = (r.naive-r.actual).abs(); r["err_avg12"] = (r.avg12-r.actual).abs()
r.to_csv(out, index=False)
s = r.groupby(["series","h"])[["err_naive","err_avg12"]].mean().round(3)
print(s.unstack(0).to_string())
print()
print(r.groupby("series")[["err_naive","err_avg12"]].mean().round(3))
print(r.groupby("series").origin.agg(["min","max"]))
print(r.groupby("series").actual.agg(["mean","min","max"]).round(2))
