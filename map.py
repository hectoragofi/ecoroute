import csv
import searoute
import folium
import pandas as pd
from folium import Map, Marker, Popup, plugins

import emissions_calculator


def runProgram():
    # origin = [37.9414585, 23.6315684243961]
    # destination = [40.629157, -74.039137]
    global route_group
    # Create a map object
    map_center = [48.8566, 2.3522]
    zoom_level = 4

    #m = folium.Map(location=map_center, zoom_start=zoom_level, control_scale=True, zoom_control=False, min_zoom=2, max_zoom=12)
    # createLineRoute(origin,destination)
    m = folium.Map(
        location=map_center,
        zoom_start=zoom_level,
        control_scale=True,
        zoom_control=False,
        max_zoom=12,
        min_zoom=2,
        max_bounds=[[39.7833, -122.4500], [37.7433, -122.4167]] )

    # OpenStreetMap
    # folium.TileLayer('openstreetmap').add_to(m)
    # CartoDB Positron
    # folium.TileLayer('cartodbpositron', attr='Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL').add_to(m)

    # CartoDB Dark Matter
    # folium.TileLayer('cartodbdark_matter', attr='Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL').add_to(m)
    route_group = folium.FeatureGroup(name='Route').add_to(m)
    def createPortMarkers():
        def add_marker_to_cluster(location, port_name, index_number):
            marker = Marker(location=location,
                            popup=Popup(f"Port: {port_name} ({index_number})"),tooltip=port_name,icon=folium.Icon(color='blue', icon='anchor', prefix='fa'))
            marker.add_to(marker_cluster)

        # Load the CSV file in chunks
        csv_file_path = 'ports.csv'
        chunk_size = 1000
        map_center = None

        # Create a MarkerCluster to group markers when zoomed out
        marker_cluster = plugins.MarkerCluster().add_to(m)

        for chunk in pd.read_csv(csv_file_path, chunksize=chunk_size):
            # Optimize data types
            chunk['Latitude'] = chunk['Latitude'].astype(float)
            chunk['Longitude'] = chunk['Longitude'].astype(float)

            # Create a Folium map centered around the first port's coordinates
            if map_center is None:
                map_center = [chunk['Latitude'].iloc[0], chunk['Longitude'].iloc[0]]

            # Use vectorized operations
            chunk['location'] = list(zip(chunk['Latitude'], chunk['Longitude']))
            chunk.apply(
                lambda row: add_marker_to_cluster(row['location'], row['Main Port Name'],
                                                  row['World Port Index Number']),
                axis=1)

    createPortMarkers()

    # folium.LayerControl().add_to(m)
    # Save the map object as an HTML file
    m.save('templates/map.html')
    return m


def createLineRoute(origin, destination, m):
    global properties, route_group
    m = runProgram()
    origin1 = [origin[1], origin[0]]
    destination1 = [destination[1], destination[0]]

    # Instantiate the route object
    route = searoute.searoute(origin1, destination1, speed_knot=12.5, units="naut")

    # Obtain the route from the object
    coordinates = route['geometry']['coordinates']
    coordinates = [[coord[1], coord[0]] for coord in coordinates]

    # Increase the resolution by adding more points along the route
    high_resolution_coordinates = []
    for i in range(len(coordinates) - 1):
        high_resolution_coordinates.append(coordinates[i])
        resolution = 10
        for j in range(1, resolution):
            fraction = j / resolution
            lat = coordinates[i][0] + fraction * (coordinates[i + 1][0] - coordinates[i][0])
            lon = coordinates[i][1] + fraction * (coordinates[i + 1][1] - coordinates[i][1])
            high_resolution_coordinates.append([lat, lon])

    high_resolution_coordinates.append(coordinates[-1])

    # Add a marker for each coordinate
    #for coord in high_resolution_coordinates:
     #   folium.CircleMarker(location=coord, radius=1, fill_color='black', color='black').add_to(m)

    # Create a line between coordinates
    poly_line = folium.PolyLine(locations=high_resolution_coordinates, color='#0c25b0', weight=3)
    poly_line.add_to(route_group)

    # Calculate CO2 emissions using the most efficient ship and fuel type
    distance = route["properties"]["length"]  # Get distance from the route properties
    speed = 25  # Constant speed

    mostEfficientShipType, mostEfficientFuelType = emissions_calculator.findMostEfficientShipAndFuelType(distance, speed)
    emissions, emission_types = emissions_calculator.calculateEmissions(mostEfficientShipType, mostEfficientFuelType, distance, speed)

    # Add a marker in the middle of the line with CO2 information
    middle_index = len(high_resolution_coordinates) // 2
    middle_coordinate = high_resolution_coordinates[middle_index]

    co2_emission = emissions[0]  # CO2 emissions are at the first index
    co2_marker_text = f"Recommended ship type:{mostEfficientShipType}         CO2 Emissions: {co2_emission} kg"

    folium.Marker(location=middle_coordinate, popup=Popup(co2_marker_text),icon=folium.Icon(color='blue', icon='ship', prefix='fa')).add_to(m)

    properties = route["properties"]
    print(properties)
    print(properties['length'])
    m.save('templates/map.html')
    return m, route_group

def returnGroup():
    return route_group
def returnProperties():
    return properties


def findCoordinates(departure, arrival):
    # Read the CSV file into a DataFrame
    df = pd.read_csv('ports.csv')

    # Check if the departure and arrival ports are in the DataFrame
    if departure not in df['Main Port Name'].values or arrival not in df['Main Port Name'].values:
        # Ports not found, return a special value (None in this case)
        return None, None

    # Extract the coordinates for each port
    port1_coordinates = df[df['Main Port Name'] == departure][['Latitude', 'Longitude']].values[0]
    port2_coordinates = df[df['Main Port Name'] == arrival][['Latitude', 'Longitude']].values[0]

    # Return the coordinates as a tuple of two tuples
    return port1_coordinates, port2_coordinates

# webbrowser.open('map_high_resolution.html')
