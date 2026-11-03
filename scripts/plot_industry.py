import sys, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
src, out, hi = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv)>3 else None)
t = pd.read_csv(src).sort_values("ratio_12mo", ascending=False).reset_index(drop=True)
INK, SEC, GRID, BG, GREY = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb", "#9a9a94"
fig, ax = plt.subplots(figsize=(10,6.4), dpi=160, facecolor=BG); ax.set_facecolor(BG)
n = len(t)
for i, r in t.iterrows():
    y = n-1-i
    col = "#eb6834" if (hi and r.industry==hi) else "#2a78d6"
    ax.plot([r.ratio_12mo, r.ratio_2000_19], [y,y], color=GRID, lw=3, zorder=1, solid_capstyle="round")
    ax.scatter(r.ratio_2000_19, y, s=42, color=GREY, zorder=2)
    ax.scatter(r.ratio_12mo, y, s=62, color=col, zorder=3)
    ax.text(r.ratio_12mo-0.04 if r.ratio_12mo<r.ratio_2000_19 else r.ratio_12mo+0.04, y, f"{r.ratio_12mo:.2f}", color=INK, fontsize=8.5, va="center", ha="right" if r.ratio_12mo<r.ratio_2000_19 else "left")
ax.set_yticks(range(n)); ax.set_yticklabels(list(t.industry)[::-1], fontsize=9, color=INK)
ax.set_xlim(0, 2.8); ax.set_ylim(-.7, n-.3)
ax.grid(axis="x", color=GRID, lw=.8); ax.set_axisbelow(True)
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.tick_params(colors=SEC, length=0, labelsize=9)
ax.set_xlabel("Hires per job opening", color=SEC, fontsize=9)
ax.scatter([],[],s=62,color="#2a78d6",label="Last 12 months"); ax.scatter([],[],s=42,color=GREY,label="2000-2019 average")
ax.legend(frameon=False, loc="lower right", labelcolor=SEC, fontsize=9)
ax.set_title("Hires per job opening by industry: today vs. its own history", loc="left", color=INK, fontsize=12, fontweight="bold")
fig.text(0.01, 0.01, f"Source: BLS JOLTS, seasonally adjusted. Last 12 months through {t.last_month.iloc[0]}. Hires divided by openings.", color=SEC, fontsize=8)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig(out, facecolor=BG)
