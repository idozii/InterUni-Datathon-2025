import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === 1) Load visitation data ===
file_path = r"C:\Users\tisha\OneDrive\Desktop\DATATHON2025\2025 Allianz Datathon Dataset.xlsx"
df = pd.read_excel(file_path, sheet_name="Visitation Data")

# Resort columns (skip Year, Week)
resorts = df.columns[2:]

# === 2) Correlation Heatmap ===
corr = df[resorts].corr()

plt.figure(figsize=(10, 8))
im = plt.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
cbar = plt.colorbar(im)
cbar.set_label("Correlation", rotation=270, labelpad=15)

plt.xticks(range(len(resorts)), resorts, rotation=45, ha="right")
plt.yticks(range(len(resorts)), resorts)

# Annotate correlation values
for i in range(len(resorts)):
    for j in range(len(resorts)):
        val = corr.iloc[i, j]
        plt.text(j, i, f"{val:.2f}", ha="center", va="center", color="black")

plt.title("Correlation Heatmap of Resort Visitations")
plt.tight_layout()
plt.show()

# === 3) Outlier Detection: yearly totals ===
yearly = df.groupby("Year")[resorts].sum()

outliers = {}

for resort in resorts:
    vals = yearly[resort]
    mean, std = vals.mean(), vals.std()
    z = (vals - mean) / std
    flagged = z[abs(z) > 2]   # threshold = 2 std devs
    if not flagged.empty:
        outliers[resort] = flagged

# Print results
print("=== Outliers in Yearly Visitations (z > 2 or z < -2) ===")
for resort, flagged in outliers.items():
    print(f"\n{resort}:")
    for year, val in flagged.items():
        print(f"  Year {year}: {val} visitors")

# === 4) Plot yearly visitation with outliers flagged ===
for resort in resorts:
    vals = yearly[resort]
    mean, std = vals.mean(), vals.std()
    z = (vals - mean) / std
    
    plt.figure(figsize=(8, 4))
    plt.plot(vals.index, vals.values, marker="o", label=resort)
    plt.axhline(mean, color="green", linestyle="--", label="mean")
    
    # highlight outliers
    plt.scatter(z[abs(z) > 2].index,
                vals[z[abs(z) > 2].index],
                color="red", s=100, zorder=5, label="outliers")
    
    plt.title(f"Yearly visitation for {resort}")
    plt.xlabel("Year")
    plt.ylabel("Visitors")
    
    # ✅ Legend in top-right
    plt.legend(loc="lower right")
    
    plt.tight_layout()
    plt.show()

