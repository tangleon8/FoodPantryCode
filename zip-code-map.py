import pandas as pd
import folium
import branca.colormap as cm

# Load the data
file_path = '/Users/leontang/Downloads/skunkworks_data_v6.csv'  # Update path as needed
data_v6 = pd.read_csv(file_path)

# Filter data to include only Wisconsin locations based on latitude and longitude bounds
wisconsin_data = data_v6[(data_v6['Latitude'].between(42.5, 47)) & 
                         (data_v6['Longitude'].between(-93, -86))]

# Aggregate total donations per zip code
donations_by_zip = wisconsin_data.groupby(['Zip', 'Latitude', 'Longitude']).agg({'Amount': 'sum'}).reset_index()

# Center of Wisconsin for map centering
wisconsin_center = [44.5, -89.5]

# Initialize the folium map centered on Wisconsin
wisconsin_map = folium.Map(location=wisconsin_center, zoom_start=7)

# Define a color scale for donations
donation_scale = cm.linear.YlGnBu_09.scale(donations_by_zip['Amount'].min(), donations_by_zip['Amount'].max())

# Add each zip code location to the map with color shading based on donation amount
for _, row in donations_by_zip.iterrows():
    folium.CircleMarker(
        location=(row['Latitude'], row['Longitude']),
        radius=6,  # Fixed radius for better color visualization
        color=donation_scale(row['Amount']),
        fill=True,
        fill_color=donation_scale(row['Amount']),
        fill_opacity=0.7,
        popup=f"Zip: {int(row['Zip'])} - Donations: ${row['Amount']:,.2f}"
    ).add_to(wisconsin_map)

donation_scale.caption = 'Total Donations per Zip Code in Wisconsin'
donation_scale.add_to(wisconsin_map)

output_map_path = '/Users/leontang/Downloads/wisconsin_donations_filled_map.html'  
wisconsin_map.save(output_map_path)

print(f"Map saved to {output_map_path}")
