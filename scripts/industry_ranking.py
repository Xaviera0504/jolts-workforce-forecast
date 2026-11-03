import sys, pandas as pd
d = sys.argv[1]
def tsv(p):
    t = pd.read_csv(p, sep="\t", dtype=str, encoding="utf-8").apply(lambda c: c.str.strip())
    t.columns = [c.strip() for c in t.columns]; return t
s = tsv(d + "/jt.series")
import os
v = tsv(next(d + "/" + n for n in ("jt.data.1.AllItems","jt_data_1.AllItems") if os.path.exists(d + "/" + n)))
s = s[(s.seasonal=="S")&(s.state_code=="00")&(s.area_code=="00000")&(s.sizeclass_code=="00")&(s.ratelevel_code=="L")&s.dataelement_code.isin(["JO","HI"])]
v = v.merge(s[["series_id","industry_code","dataelement_code"]], on="series_id")
v = v[v.period.str.match(r"M(0[1-9]|1[0-2])")].copy()
v["date"] = pd.to_datetime(v.year + "-" + v.period.str[1:] + "-01"); v["value"] = v.value.astype(float)
w = v.pivot_table(index=["industry_code","date"], columns="dataelement_code", values="value").dropna().reset_index()
names = {"110099":"Mining and logging","230000":"Construction","320000":"Durable goods manufacturing","340000":"Nondurable goods manufacturing","420000":"Wholesale trade","440000":"Retail trade","480099":"Transportation, warehousing, utilities","510000":"Information","520000":"Finance and insurance","530000":"Real estate, rental, leasing","540099":"Professional and business services","610000":"Private educational services","620000":"Health care and social assistance","710000":"Arts, entertainment, recreation","720000":"Accommodation and food services","810000":"Other services","910000":"Federal government","923000":"State and local education","929000":"State and local, excl. education"}
rows = []
for c, n in names.items():
    x = w[w.industry_code==c].sort_values("date")
    r12 = x.HI.tail(12).sum()/x.JO.tail(12).sum()
    r3 = x.HI.tail(3).sum()/x.JO.tail(3).sum()
    pre = x[x.date<="2019-12-01"]; rp = pre.HI.sum()/pre.JO.sum()
    rows.append((n, x.date.max().strftime("%Y-%m"), round(r12,2), round(r3,2), round(rp,2), round(r12/rp-1,2), round(x.JO.tail(12).mean())))
t = pd.DataFrame(rows, columns=["industry","last_month","ratio_12mo","ratio_3mo","ratio_2000_19","vs_pre2020","avg_openings_k"]).sort_values("ratio_12mo")
print(t.to_string(index=False)); t.to_csv(sys.argv[2], index=False)
