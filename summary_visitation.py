import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_excel('2025 Allianz Datathon Dataset.xlsx', sheet_name='Visitation Data')

temp_df = df.drop(columns=['Year', 'Week'])

temp_df.describe().to_csv('visit_summary.csv', index=False)
# print(temp_df.describe())


# Summary stats for each site
sites = ['Mt. Baw Baw','Mt. Stirling','Mt. Hotham','Falls Creek',
         'Mt. Buller','Selwyn','Thredbo','Perisher','Charlotte Pass']

summary_stats = {
    'Mt. Baw Baw': {'min':0,'q1':1757,'median':5565,'q3':8513,'max':18031},
    'Mt. Stirling': {'min':0,'q1':98,'median':480,'q3':962,'max':2097},
    'Mt. Hotham': {'min':0,'q1':8368,'median':21856,'q3':30944,'max':44648},
    'Falls Creek': {'min':0,'q1':8741,'median':28099,'q3':36692,'max':49697},
    'Mt. Buller': {'min':0,'q1':12397,'median':33328,'q3':44315,'max':66326},
    'Selwyn': {'min':0,'q1':2180,'median':6454,'q3':8530,'max':12863},
    'Thredbo': {'min':0,'q1':11543,'median':34676,'q3':46015,'max':70634},
    'Perisher': {'min':0,'q1':15236,'median':46265,'q3':60788,'max':93226},
    'Charlotte Pass': {'min':0,'q1':842,'median':2542,'q3':3344,'max':5033}
}

# Create boxplot
box_data = []
for site in sites:
    stats = summary_stats[site]
    box_data.append({
        'label': site,
        'whislo': stats['min'],
        'q1': stats['q1'],
        'med': stats['median'],
        'q3': stats['q3'],
        'whishi': stats['max'],
        'fliers': []
    })

fig, ax = plt.subplots(figsize=(12,6))
ax.bxp(box_data, showfliers=False)  # <-- use ax.bxp instead of plt.bxp
ax.set_ylabel('Value')
ax.set_title('Box and Whisker Plot for Visitation of Sites')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()