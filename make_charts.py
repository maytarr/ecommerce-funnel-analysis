"""Build the README/site charts from the CSV results in results/."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).parent
RES = HERE / "results"
OUT = HERE / "images"
OUT.mkdir(exist_ok=True)

SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT2 = "#52514e"
GRID = "#e4e3df"
BLUE = "#2a78d6"
GREY = "#b8b7b1"

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": TEXT2, "text.color": TEXT,
    "xtick.color": TEXT2, "ytick.color": TEXT2, "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
})


def title(ax, main, sub):
    ax.set_title(main, loc="left", fontsize=14, fontweight="bold", color=TEXT, pad=26)
    ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=10.5, color=TEXT2)


# 1. Funnel -------------------------------------------------------------------
f = pd.read_csv(RES / "01_overall_funnel.csv")
labels = {"session_start": "Visited the shop", "view_item": "Viewed a product",
          "add_to_cart": "Added to cart", "begin_checkout": "Started checkout",
          "add_payment_info": "Entered payment details", "purchase": "Bought"}
f["step"] = f["event_name"].map(labels)
fig, ax = plt.subplots(figsize=(9, 4.6))
y = range(len(f))[::-1]
ax.barh(list(y), f["users"], color=BLUE, height=0.62)
ax.set_yticks(list(y), f["step"])
ax.tick_params(axis="y", length=0)
ax.set_xticks([])
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
prev = None
for yi, (u, s) in zip(y, zip(f["users"], f["step"])):
    note = f"{u:,}" if prev is None else f"{u:,}   ({u / prev:.0%} of previous step)"
    ax.text(u + 3000, yi, note, va="center", fontsize=10, color=TEXT)
    prev = u
ax.set_xlim(0, f["users"].max() * 1.45)
title(ax, "Most visitors leave before they reach the cart",
      "Distinct visitors reaching each step, Google Merchandise Store, Nov 2020 – Jan 2021")
fig.tight_layout()
fig.savefig(OUT / "01_funnel.png", dpi=160)
plt.close(fig)

# 2. Purchase rate by traffic source ------------------------------------------
t = pd.read_csv(RES / "03_funnel_by_traffic_source.csv")
names = {"referral": "Link from another site", "(none)": "Typed address directly",
         "organic": "Google search (unpaid)", "cpc": "Paid ads",
         "<Other>": "Anonymised: <Other>", "(data deleted)": "Anonymised: data deleted"}
t["rate"] = t["purchased"] / t["visited"]
t["anon"] = t["medium"].isin(["<Other>", "(data deleted)"])
t = pd.concat([t[~t["anon"]].sort_values("rate", ascending=False),
               t[t["anon"]].sort_values("rate", ascending=False)]).reset_index(drop=True)
fig, ax = plt.subplots(figsize=(9, 4.6))
y = list(range(len(t)))[::-1]
ax.barh(y, t["rate"] * 100, color=[GREY if a else BLUE for a in t["anon"]], height=0.62)
ax.set_yticks(y, t["medium"].map(names))
ax.tick_params(axis="y", length=0)
ax.set_xticks([])
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
for yi, r, n in zip(y, t["rate"], t["visited"]):
    ax.text(r * 100 + 0.05, yi, f"{r:.2%}   ({n:,} visitors)", va="center", fontsize=10)
ax.set_xlim(0, t["rate"].max() * 100 * 1.6)
title(ax, "Paid-ad visitors buy about half as often as referred visitors",
      "Share of visitors who bought, by how they first arrived (grey = anonymised by Google)")
fig.tight_layout()
fig.savefig(OUT / "02_purchase_rate_by_source.png", dpi=160)
plt.close(fig)

# 3. Weekly trend: two stacked panels, one axis each ---------------------------
w = pd.read_csv(RES / "04_weekly_trend.csv", parse_dates=["week_start"])
w = w[w["week_start"] >= "2020-11-02"].reset_index(drop=True)  # drop the 1-day partial week
w["rate"] = w["buyers"] / w["visitors"] * 100
fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 6.6), sharex=True,
                             gridspec_kw={"height_ratios": [1, 1], "hspace": 0.45})
a1.plot(w["week_start"], w["rate"], color=BLUE, lw=2, marker="o", ms=5)
a1.set_ylim(0, 3.2)
a1.set_ylabel("Purchase rate (%)")
a1.grid(axis="y", color=GRID, lw=0.8)
for d, txt, dx, ha in [("2020-11-23", "Black Friday week", -4, "right"),
                       ("2020-12-07", "Peak: last week before\nChristmas shipping", 4, "left")]:
    r = w.loc[w["week_start"] == d, "rate"].iloc[0]
    a1.annotate(txt, (pd.Timestamp(d), r), xytext=(dx, 10), textcoords="offset points",
                ha=ha, va="bottom", fontsize=9, color=TEXT2)
low = w.loc[w["week_start"] == "2021-01-04"]
a1.annotate("Busy but few buyers", (low["week_start"].iloc[0], low["rate"].iloc[0]),
            xytext=(0, -18), textcoords="offset points", ha="center", fontsize=9, color=TEXT2)
title(a1, "Buying peaked in early December, not on Black Friday",
      "Weekly share of visitors who bought (top) and revenue (bottom)")

ok = w["week_start"] < "2021-01-25"
a2.bar(w.loc[ok, "week_start"], w.loc[ok, "revenue_usd"] / 1000, width=5, color=BLUE)
a2.bar(w.loc[~ok, "week_start"], w.loc[~ok, "revenue_usd"] / 1000, width=5, color=GREY)
a2.annotate("Revenue tracking gap:\nmost purchases logged as $0", (pd.Timestamp("2021-01-25"), 7),
            xytext=(pd.Timestamp("2021-01-28"), 42), ha="right", fontsize=9, color=TEXT2,
            arrowprops=dict(arrowstyle="-", color=TEXT2, lw=0.8))
a2.set_ylabel("Revenue (USD thousands)")
a2.grid(axis="y", color=GRID, lw=0.8)
a2.set_axisbelow(True)
a2.tick_params(axis="x", labelsize=9.5)
import matplotlib.dates as mdates
a2.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
fig.savefig(OUT / "03_weekly_trend.png", dpi=160, bbox_inches="tight")
plt.close(fig)
print("charts written to", OUT)
