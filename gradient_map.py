import pandas as pd
import folium
from folium.plugins import HeatMap

file_path = '/mnt/data/skunkworks_data_v6.csv'
data_v6 = pd.read_csv(file_path)

# Filter data for Wisconsin based on latitude and longitude ranges
wisconsin_data = data_v6[(data_v6['Latitude'].between(42.5, 47)) & 
                         (data_v6['Longitude'].between(-93, -86))]

# Group data by Zip, Latitude, and Longitude, summing up the donations
donations_by_zip = wisconsin_data.groupby(['Zip', 'Latitude', 'Longitude']).agg({'Amount': 'sum'}).reset_index()

# Create a folium map centered on Wisconsin for the heatmap
wisconsin_center = [44.5, -89.5]
wisconsin_map = folium.Map(location=wisconsin_center, zoom_start=7)

# Prepare data for the heatmap
heat_data = [[row['Latitude'], row['Longitude'], row['Amount']] for _, row in donations_by_zip.iterrows()]

# Add a heat map layer to the map
HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(wisconsin_map)

# Save the heatmap to an HTML file
output_map_path = '/mnt/data/wisconsin_donations_heatmap.html'
wisconsin_map.save(output_map_path)

# Create a new folium map centered on Wisconsin for the gradient path map
gradient_map = folium.Map(location=wisconsin_center, zoom_start=7)

# Filter the top 10 donation points to create a gradient path
top_donations = donations_by_zip.sort_values(by='Amount', ascending=False).head(10)

# Create a list of coordinates for the gradient path
coordinates = list(zip(top_donations['Latitude'], top_donations['Longitude']))

# Add a polyline with a gradient color effect to the map
folium.PolyLine(
    coordinates,
    color='blue',
    weight=3,
    opacity=0.6,
    tooltip='Path between Top Donation Areas'
).add_to(gradient_map)

gradient_map_path = '/mnt/data/wisconsin_donations_gradient_path_map.html'
gradient_map.save(gradient_map_path)

print("Heatmap saved to:", output_map_path)
print("Gradient path map saved to:", gradient_map_path)
