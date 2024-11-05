import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

file_path = '/Users/leontang/Downloads/skunkworks_data_v5_full.csv'
data = pd.read_csv(file_path)

zip_codes = data['Zip'].dropna().astype(int).unique()

geolocator = Nominatim(user_agent="zip_code_locator")

def get_lat_lon(zip_code):
    try:
        location = geolocator.geocode({"postalcode": zip_code, "country": "US"})
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        time.sleep(1)
        return get_lat_lon(zip_code)
    return None, None

zip_coordinates = {zip_code: get_lat_lon(zip_code) for zip_code in zip_codes}

zip_coordinates_df = pd.DataFrame(
    [(zip_code, lat, lon) for zip_code, (lat, lon) in zip_coordinates.items() if (lat is not None and lon is not None)],
    columns=["Zip", "Latitude", "Longitude"]
)

data = data.merge(zip_coordinates_df, how="left", left_on="Zip", right_on="Zip")

output_path = '/Users/leontang/Downloads/skunkworks_data_v6_full.csv'
data.to_csv(output_path, index=False)

print(f"Data with latitude and longitude saved to: {output_path}")
