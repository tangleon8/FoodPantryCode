import pandas as pd
import folium
from folium.plugins import MarkerCluster
import numpy as np

file_path = '/mnt/data/skunkworks_data_v6.csv'
data = pd.read_csv(file_path)
median_income_path = '/mnt/data/reorganized_median_income_data (1).csv'
median_income_data = pd.read_csv(median_income_path)

# Aggregating data by ZIP code
zip_agg = data.groupby('Zip').agg(
    total_donations=('Amount', 'sum'),
    donation_count=('Amount', 'count'),
    campaigns=('Campaign', lambda x: ', '.join(x.unique())),
    latitude=('Latitude', 'first'),
    longitude=('Longitude', 'first')
).reset_index()

# Ensure ZIP codes are integers for merging
zip_agg['Zip'] = zip_agg['Zip'].astype(int)
median_income_data['Zip'] = median_income_data['Zip'].astype(int)

# Merge on ZIP code to add median household income
zip_merged = pd.merge(zip_agg, median_income_data[['Zip', 'Median Household Income']], on='Zip', how='left')

# Creating the map centered on Wisconsin with real income data
m = folium.Map(location=[44.5, -89.5], zoom_start=7)
marker_cluster = MarkerCluster().add_to(m)

for _, row in zip_merged.iterrows():
    if not np.isnan(row['latitude']) and not np.isnan(row['longitude']):
        popup_text = (
            f"<b>ZIP Code</b>: {int(row['Zip'])}<br>"
            f"<ul>"
            f"<li><b>Total Donations</b>: ${row['total_donations']:.2f}</li>"
            f"<li><b>Donation Count</b>: {row['donation_count']}</li>"
            f"<li><b>Campaigns</b>: {row['campaigns']}</li>"
            f"<li><b>Median Household Income</b>: ${row['Median Household Income']:.2f}</li>"
            f"</ul>"
        )
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup_text
        ).add_to(marker_cluster)

real_income_map_path = "/mnt/data/wisconsin_donations_map_with_income.html"
m.save(real_income_map_path)

real_income_map_path
