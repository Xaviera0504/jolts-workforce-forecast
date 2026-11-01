import sys, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
src, out = sys.argv[1], sys.argv[2]
df = pd.read_csv(src, parse_dates=["date"])
d = df[(df.industry_code==0) & (df.type=="level_thousands") & df.measure_code.isin(["JO","HI","QU"])] if df.industry_code.dtype!=object else df[(df.industry_code=="000000") & (df.type=="level_thousands") & df.measure_code.isin(["JO","HI","QU"])]
w = d.pivot(index="date", columns="measure_code", values="value")/1000
spec = [("JO","Job openings","#2a78d6"),("HI","Hires","#eb6834"),("QU","Quits","#1baf7a")]
INK, SEC, GRID, BG = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
fig, ax = plt.subplots(figsize=(10,5.2), dpi=160, facecolor=BG)
ax.set_facecolor(BG)
ax.axvspan(pd.Timestamp("2020-02-01"), pd.Timestamp("2020-04-30"), color="#e6e5e1", alpha=.6, lw=0)
for c,l,col in spec:
    ax.plot(w.index, w[c], color=col, lw=2, label=l)
    ax.text(w.index[-1]+pd.Timedelta(days=60), w[c].iloc[-1], f"{l}\n{w[c].iloc[-1]:.1f}M", color=INK, fontsize=9, va="center")
ax.set_ylim(0, 13); ax.set_xlim(w.index[0], w.index[-1]+pd.Timedelta(days=900))
ax.set_xticks([pd.Timestamp(f"{y}-01-01") for y in range(2000, 2027, 4)] + [pd.Timestamp("2026-01-01")]); ax.set_xticklabels([str(y) for y in range(2000, 2027, 4)] + ["2026"])
ax.grid(axis="y", color=GRID, lw=.8); ax.set_axisbelow(True)
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(colors=SEC, length=0, labelsize=9)
ax.set_ylabel("Millions per month", color=SEC, fontsize=9)
ax.set_title("US total nonfarm: openings, hires and quits, 2000-2026", loc="left", color=INK, fontsize=12, fontweight="bold")
ax.legend(frameon=False, loc="upper left", labelcolor=SEC, fontsize=9, ncol=3)
fig.text(0.01, 0.01, "Source: BLS JOLTS, seasonally adjusted, levels. Shaded: Mar-Apr 2020.", color=SEC, fontsize=8)
fig.tight_layout(rect=(0,0.03,1,1))
fig.savefig(out, facecolor=BG)
print(w.tail(1).round(3).to_string()); print(w.loc["2020-03":"2020-05"].round(2).to_string()); print(w.max().round(2).to_string(), w.idxmax().to_string())
