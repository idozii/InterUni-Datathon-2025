import pandas as pd
import matplotlib.pyplot as plt

# --- Load visitation data ---
file_path = r"C:\Users\tisha\OneDrive\Desktop\DATATHON2025\2025 Allianz Datathon Dataset.xlsx"
df = pd.read_excel(file_path, sheet_name="Visitation Data")

# --- Compute correlation matrix (only resort columns) ---
resorts = df.columns[2:]  # skip Year, Week
corr = df[resorts].corr()

# --- Plot heatmap ---
plt.figure(figsize=(10, 8))
im = plt.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)

# Colorbar
cbar = plt.colorbar(im)
cbar.set_label("Correlation", rotation=270, labelpad=15)

# Axis ticks & labels
plt.xticks(range(len(resorts)), resorts, rotation=45, ha="right")
plt.yticks(range(len(resorts)), resorts)

# Annotate values inside cells
for i in range(len(resorts)):
    for j in range(len(resorts)):
        val = corr.iloc[i, j]
        plt.text(j, i, f"{val:.2f}", ha="center", va="center", color="black")

plt.title("Correlation Heatmap of Resort Visitations")
plt.tight_layout()
plt.show()
