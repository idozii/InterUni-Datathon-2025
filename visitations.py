import pandas as pd
import matplotlib.pyplot as plt


file_path = r"C:\Users\tisha\OneDrive\Desktop\DATATHON2025\2025 Allianz Datathon Dataset.xlsx"

# Load only the "Visitation Data" sheet
df = pd.read_excel(file_path, sheet_name="Visitation Data")

#sum across resorts for each year
resort_cols = df.columns[2:]
yearly_totals = df.groupby("Year")[resort_cols].sum()

#plot total vistors
yearly_totals.sum(axis=1).plot(kind="bar", figsize=(10, 6))
plt.title("Total Visitors Across All Resorts by Year")
plt.xlabel("Year")
plt.ylabel("Total Visitors")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

#plot each resort seperately
yearly_totals.plot(kind="bar", figsize=(12, 6))
plt.title("Resort Visitors by Year")
plt.xlabel("Year")
plt.ylabel("Number of Visitors")
plt.xticks(rotation=0)
plt.legend(title="Resorts", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()