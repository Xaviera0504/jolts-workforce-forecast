import sys, csv, os
d, out = sys.argv[1], sys.argv[2]

def tsv(path):
    with open(path, encoding="utf-8", newline="") as f:
        rows = [l.rstrip("\r\n").split("\t") for l in f]
    hdr = [h.strip() for h in rows[0]]
    return [dict(zip(hdr, [c.strip() for c in r])) for r in rows[1:] if r and any(c.strip() for c in r)]

data_path = next(os.path.join(d, n) for n in ("jt.data.1.AllItems","jt_data_1.AllItems") if os.path.exists(os.path.join(d, n)))
series = {r["series_id"]: r for r in tsv(os.path.join(d, "jt.series"))}
de = {"HI":"Hires","JO":"Job openings","LD":"Layoffs and discharges","OS":"Other separations","QU":"Quits","TS":"Total separations","UO":"Unemployed per opening"}
ind = {"000000":"Total nonfarm","100000":"Total private","520000":"Finance and insurance","510099":"Financial activities","540099":"Professional and business services","620000":"Health care and social assistance"}
keep_ind = set(ind)
keep_de = {"JO","HI","TS","QU","LD","OS"}

n = 0
with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["series_id","date","year","month","industry_code","industry","measure_code","measure","type","seasonal","value"])
    for r in tsv(data_path):
        s = series.get(r["series_id"])
        if not s: continue
        if s["state_code"]!="00" or s["area_code"]!="00000" or s["sizeclass_code"]!="00": continue
        if s["seasonal"]!="S" or s["industry_code"] not in keep_ind or s["dataelement_code"] not in keep_de: continue
        p = r["period"]
        if not p.startswith("M") or p=="M13": continue
        m = int(p[1:])
        if not r["value"] or r["value"]=="-": continue
        w.writerow([r["series_id"], f"{r['year']}-{m:02d}-01", r["year"], m, s["industry_code"], ind[s["industry_code"]],
                    s["dataelement_code"], de[s["dataelement_code"]],
                    "level_thousands" if s["ratelevel_code"]=="L" else "rate_percent", "SA", r["value"]])
        n += 1
print("rows", n)
