# ski_analysis.py
# Charts + "best week" scoring for Australian ski resorts

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import matplotlib.dates as mdates

# ----------------------------
# 1) Data from your screenshot
# ----------------------------
# resort, rating_5, difficulty_3, lifts, adult_price, youth_price, child_price,
# accom_level, access, elevation, season_text
data = [
    ("BawBaw",     2.5, 1.3,           7,   89,  68,  54, "avg",        "car",               "1450m - 1560m", "mid june - late sep"),
    ("Hotham",     3.7, 2.2,          14,  243, 134,   0, "above avg",  "car, train, plane", "1450m - 1845m", "early june - late sep"),
    ("Falls Creek",3.6, 2.040816327,  15,  243, 134,   0, "above avg",  "car, train, plane", "1500m - 1780m", "early june - late sep"),
    ("Buller",     3.7, 2.149473684,  20,  243, 140, 140, "above avg",  "car, train, plane", "1380m - 1780m", "early june - early oct"),
    ("Selwyn",     2.6, 1.2,           8,  119,  95,  35, "avg",        "car",               "1492m - 1614m", "mid june - early sep"),
    ("Thredbo",    3.8, 1.942307692,  15,  240, 129, 140, "above avg",  "car, train, plane", "1365m - 2037m", "early june - late sep"),
    ("Perisher",   3.7, 1.769230769,  47,  264, 145,   0, "above avg",  "car, train, plane", "1605m - 2034m", "mid june - early oct"),
    ("Charlotte",  2.6, 2.0,           4,  175,   0, 114, "avg",        "car, train, plane", "1765m - 1954m", "mid june - late sep"),
]

df = pd.DataFrame(
    data,
    columns=[
        "resort","rating_5","difficulty_3","lifts","adult_price","youth_price",
        "child_price","accom_level","access","elevation","season_text"
    ],
)

def blended_price(row):
    prices = [p for p in [row["adult_price"], row["youth_price"], row["child_price"]] if p and p > 0]
    return float(np.mean(prices)) if prices else np.nan

df["ticket_price"] = df.apply(blended_price, axis=1)

# ----------------------------
# 2) Parse season strings → dates
# ----------------------------
def parse_season(text, year=2025):
    start_txt, end_txt = [p.strip() for p in text.split("-")]

    def parse_part(s):
        when = s.split()[0].lower()
        month = s.split()[1].lower()[:3]  # 'jun','jul','aug','sep','oct'
        month_map = {"jun":6, "jul":7, "aug":8, "sep":9, "oct":10}
        m = month_map[month]
        day = {"early":7, "mid":15, "late":25}.get(when, 15)
        return date(year, m, day)

    return parse_part(start_txt), parse_part(end_txt)

df[["season_start","season_end"]] = df["season_text"].apply(lambda s: pd.Series(parse_season(s)))

# ----------------------------
# 3) Weekly scoring (“best week”)
# ----------------------------
W_RATING, W_DIFF_INV, W_PRICE_INV, W_LIFTS = 0.35, 0.25, 0.25, 0.15

season_start, season_end = date(2025,6,1), date(2025,10,15)

weeks = []
d = season_start
while d <= season_end:
    week_start, week_end = d, d + timedelta(days=6)
    open_mask = (df["season_start"] <= week_end) & (df["season_end"] >= week_start)
    sub = df[open_mask].copy()
    n_open = len(sub)

    if n_open > 0:
        def norm_col(col, invert=False):
            c = sub[col].astype(float)
            if c.max() == c.min():
                n = pd.Series(1.0, index=c.index)
            else:
                n = (c - c.min()) / (c.max() - c.min())
            return 1 - n if invert else n

        score = (
            W_RATING   * norm_col("rating_5") +
            W_DIFF_INV * norm_col("difficulty_3", invert=True) +
            W_PRICE_INV* norm_col("ticket_price", invert=True) +
            W_LIFTS    * norm_col("lifts")
        )
        week_score = float(score.mean())
        top_resort = str(sub.iloc[score.values.argmax()]["resort"])
    else:
        week_score, top_resort = 0.0, None

    weeks.append({
        "week_start": week_start,
        "week_end": week_end,
        "open_resorts": n_open,
        "mean_week_score": week_score,
        "top_resort": top_resort
    })
    d += timedelta(days=7)

weeks_df = pd.DataFrame(weeks)

best_week = weeks_df.sort_values(
    by=["open_resorts","mean_week_score","week_start"],
    ascending=[False, False, True]
).iloc[0]
print("\n=== Suggested Best Week ===")
print(best_week, "\n")

# ----------------------------
# 4) Charts
# ----------------------------

# A) Ratings by resort
plt.figure(figsize=(10,5))
df.sort_values("rating_5", ascending=False).plot(
    x="resort", y="rating_5", kind="bar", legend=False
)
plt.title("Resort Ratings (out of 5)")
plt.ylabel("Rating")
plt.xlabel("Resort")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# B) Difficulty vs Price (bubble = #lifts)
plt.figure(figsize=(8,6))
sizes = (df["lifts"] / df["lifts"].max()) * 1200 + 50
plt.scatter(df["difficulty_3"], df["ticket_price"], s=sizes, alpha=0.6)
for _, r in df.iterrows():
    plt.annotate(r["resort"], (r["difficulty_3"], r["ticket_price"]),
                 xytext=(5,5), textcoords="offset points")
plt.title("Difficulty vs Ticket Price (bubble = lifts)")
plt.xlabel("Difficulty (0–3, higher = harder)")
plt.ylabel("Typical Ticket Price (blended)")
plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()

# C) Ticket price breakdown (stacked bars)
plt.figure(figsize=(10,6))
price_df = df[["resort","adult_price","youth_price","child_price"]].set_index("resort")
price_df.plot(kind="bar", stacked=True)
plt.title("Ticket Price Breakdown by Resort")
plt.xlabel("Resort")
plt.ylabel("Price ($)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# D) Season ranges (Gantt-style)
plt.figure(figsize=(10,6))
ypos = np.arange(len(df))
plt.hlines(y=ypos, xmin=df["season_start"], xmax=df["season_end"], linewidth=10)
plt.yticks(ypos, df["resort"])
plt.title("Season Ranges by Resort (2025)")
plt.xlabel("Date")
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.show()

# E1) Number of open resorts by week
plt.figure(figsize=(10,5))
plt.plot(weeks_df["week_start"], weeks_df["open_resorts"], marker="o")
plt.title("Number of Open Resorts by Week (2025)")
plt.xlabel("Week Start")
plt.ylabel("# Open Resorts")
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.show()

# E2) Mean week score (coverage+value+difficulty)
plt.figure(figsize=(10,5))
plt.plot(weeks_df["week_start"], weeks_df["mean_week_score"], marker="o")
plt.title("Mean Week Score (coverage + value + difficulty balance)")
plt.xlabel("Week Start")
plt.ylabel("Score (0–1)")
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.show()
