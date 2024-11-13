import pandas as pd
import folium
from folium.plugins import HeatMap

file_path = '/mnt/data/skunkworks_data_v6.csv'
data_v6 = pd.read_csv(file_path)

# Filter data for Wisconsin based on latitude and longitude
wisconsin_data = data_v6[(data_v6['Latitude'].between(42.5, 47)) & 
                         (data_v6['Longitude'].between(-93, -86))]

# Group by Zip code to sum the donations
donations_by_zip = wisconsin_data.groupby(['Zip', 'Latitude', 'Longitude']).agg({'Amount': 'sum'}).reset_index()

# Create a folium map centered on Wisconsin
wisconsin_center = [44.5, -89.5]
wisconsin_map = folium.Map(location=wisconsin_center, zoom_start=7)

# Prepare data for the heatmap
heat_data = [[row['Latitude'], row['Longitude'], row['Amount']] for _, row in donations_by_zip.iterrows()]

# Add heatmap layer to the map
HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(wisconsin_map)

# Save the generated map to an HTML file
output_map_path = '/mnt/data/wisconsin_donations_heatmap.html'
wisconsin_map.save(output_map_path)

print(f"Heatmap saved to: {output_map_path}")
