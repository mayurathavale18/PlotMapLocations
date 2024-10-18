import folium
import pandas as pd

def plot_coordinates(csv_file, output_html="map.html"):
    # Load the data from the CSV file
    data = pd.read_csv(csv_file)

    # Create a base map centered at the average latitude and longitude
    avg_lat = data['Latitude'].mean()
    avg_lng = data['Longitude'].mean()
    map_obj = folium.Map(location=[avg_lat, avg_lng], zoom_start=12)

    # Add points to the map
    for _, row in data.iterrows():
        lat = row['Latitude']
        lng = row['Longitude']
        image_url = row['image_url']

        # Skip rows where coordinates are missing
        if pd.notnull(lat) and pd.notnull(lng):
            folium.Marker(
                location=[lat, lng],
                popup=f"<a href='{image_url}' target='_blank'>View Image</a>",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(map_obj)

    # Save the map to an HTML file, embedding the necessary resources
    map_html = map_obj.get_root().render()

        # Save the HTML content to a file
    with open(output_html, "w", encoding="utf-8") as file:
        file.write(map_html)

# Example usage
plot_coordinates("images.csv")
