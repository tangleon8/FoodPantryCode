import folium
from folium.plugins import MarkerCluster
import numpy as np
import pandas as pd


# Aggregating data by ZIP code
zip_agg = data.groupby('Zip').agg(
    total_donations=('Amount', 'sum'),
    donation_count=('Amount', 'count'),
    campaigns=('Campaign', lambda x: ', '.join(x.unique())),
    latitude=('Latitude', 'first'),
    longitude=('Longitude', 'first')
).reset_index()

# Ensure ZIP codes are integers for consistency
zip_agg['Zip'] = zip_agg['Zip'].astype(int)

# Filter top 10 ZIP codes by total donation amount
top_zip_codes = zip_agg.nlargest(10, 'total_donations')
top_zip_codes['average_donation'] = top_zip_codes['total_donations'] / top_zip_codes['donation_count']

# Create a new map centered on Wisconsin
m_refined = folium.Map(location=[44.5, -89.5], zoom_start=7)
marker_cluster_refined = MarkerCluster().add_to(m_refined)

# Draw arrows for visualization from most to least donating ZIP codes
for i in range(len(top_zip_codes) - 1):
    start = (top_zip_codes.iloc[i]['latitude'], top_zip_codes.iloc[i]['longitude'])
    end = (top_zip_codes.iloc[i + 1]['latitude'], top_zip_codes.iloc[i + 1]['longitude'])
    folium.PolyLine(
        locations=[start, end],
        color='blue',
        weight=2,
        dash_array='5, 5',
        tooltip=f"From ZIP {int(top_zip_codes.iloc[i]['Zip'])} to {int(top_zip_codes.iloc[i + 1]['Zip'])}"
    ).add_to(m_refined)

# Add markers for the top 10 ZIP codes
for _, row in top_zip_codes.iterrows():
    if not np.isnan(row['latitude']) and not np.isnan(row['longitude']):
        popup_text = (
            f"<b>ZIP Code</b>: {int(row['Zip'])}<br>"
            f"<ul>"
            f"<li><b>Total Donations</b>: ${row['total_donations']:.2f}</li>"
            f"<li><b>Donation Count</b>: {row['donation_count']}</li>"
            f"<li><b>Average Donation</b>: ${row['average_donation']:.2f}</li>"
            f"</ul>"
        )
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=row['total_donations'] / max(top_zip_codes['total_donations']) * 10,  # Scaled circle size
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.6,
            popup=popup_text
        ).add_to(marker_cluster_refined)

refined_map_path = "/mnt/data/top_10_zip_codes_donations_refined_map.html"
m_refined.save(refined_map_path)

print("Map saved successfully!")
