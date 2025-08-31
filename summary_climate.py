import pandas as pd
import matplotlib.pyplot as plt

observation_sites = [71032, 71075, 72161, 83024, 83084, 83085, 85291]

df = pd.read_excel('2025 Allianz Datathon Dataset.xlsx', sheet_name='Climate Data')
visit_df = pd.read_excel('2025 Allianz Datathon Dataset.xlsx', sheet_name='Visitation Data')

df = df.rename(columns={
    'Bureau of Meteorology station number': 'station number'
})

# convert day, month and year into datetime format
df['date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])

# get season for seasonal graphing
def get_season(month):
    if month in [12,1,2]:
        return 'winter'
    elif month in [3,4,5]:
        return 'spring'
    elif month in [6,7,8]:
        return 'summer'
    else:
        return 'autumn'

df['season'] = df['date'].dt.month.apply(get_season)

# get week data
df['week'] = df['date'].dt.isocalendar().week

# summary = df.groupby('station number').agg(['mean', 'std', 'min', 'max'])
# print(summary)

# some missing data with max/min temperature, rainfall amount
df.info()

print(df.iloc[:, 4:-3].describe())

# get histogram of all climate data
# df.iloc[:, 4:-3].hist(bins=50, figsize=(20,15))
# plt.show()

# Variables
variables = ['Max Temp (°C)', 'Min Temp (°C)', 'Rainfall (mm)']

# Summary stats for each variable
summary_stats = {
    'Max Temp (°C)': {'min': -5.8, 'q1': 4.0, 'median': 9.7, 'q3': 15.5, 'max': 34.0},
    'Min Temp (°C)': {'min': -14.2, 'q1': -1.7, 'median': 2.0, 'q3': 7.0, 'max': 22.7},
    'Rainfall (mm)': {'min': 0.0, 'q1': 0.0, 'median': 0.0, 'q3': 3.6, 'max': 280.6}
}

# Convert to list of tuples for matplotlib
data = []
for var in variables:
    stats = summary_stats[var]
    data.append([stats['min'], stats['q1'], stats['median'], stats['q3'], stats['max']])

# Create figure
fig, ax = plt.subplots(figsize=(8, 5))

# Boxplot using stats (manually via bxp)
box_data = []
for i, var in enumerate(variables):
    stats = summary_stats[var]
    box_data.append({
        'label': var,
        'whislo': stats['min'],   # bottom whisker
        'q1': stats['q1'],        # Q1
        'med': stats['median'],   # Median
        'q3': stats['q3'],        # Q3
        'whishi': stats['max'],   # top whisker
        'fliers': []              # no outliers since we don't have them
    })

ax.bxp(box_data, showfliers=False)
ax.set_title("Box and Whisker Plot (from Summary Stats)")
ax.set_ylabel("Values")
plt.tight_layout()
plt.show()

# for site_num in observation_sites:
#     site_df = df[df['station number'] == site_num]
#     plt.plot(site_df['date'], site_df['Rainfall amount (millimetres)'], marker='o', label=f"site {site_num}")

# plt.figure(figsize=(12,6))
# plt.xlabel('Day')
# plt.ylabel('Rainfall (mm)')
# plt.title(f'Rainfall Over Time for sites')
# plt.xticks(rotation=45)  # rotate x-axis labels for readability
# plt.grid(True)
# plt.show()