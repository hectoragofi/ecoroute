import csv

import searoute
import folium
import pandas as pd
from folium import Map, Marker, Popup, plugins


def runProgram():
    # origin = [37.9414585, 23.6315684243961]
    # destination = [40.629157, -74.039137]
    global route_group
    # Create a map object
    map_center = [48.8566, 2.3522]
    zoom_level = 4

    m = folium.Map(location=map_center, zoom_start=zoom_level)

    # createLineRoute(origin,destination)

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
                            popup=Popup(f"Port: {port_name} ({index_number})"),
                            icon=None)
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
    global properties
    m = runProgram()
    # Change (latitude, longitude) to (longitude, latitude)
    # origin[0], origin[1] = origin[1], origin[0]
    # destination[0], destination[1] = destination[1], destination[0]
    # origin[0], origin[1] = 23.65, 37.933333
    # destination[0], destination[1] = 23.65, 39.883333
    origin1 = [origin[1], origin[0]]
    destination1 = [destination[1], destination[0]]
    # Instantiate the route object
    route = searoute.searoute(origin1, destination1, speed_knot=12.5, units="naut")

    # Obtain the route from the object
    coordinates = route['geometry']['coordinates']

    # Change (longitude, latitude) to (latitude, longitude)
    coordinates = [[coord[1], coord[0]] for coord in coordinates]

    # Increase the resolution by adding more points along the route
    high_resolution_coordinates = []
    for i in range(len(coordinates) - 1):
        # Add the current point
        high_resolution_coordinates.append(coordinates[i])

        # Add additional points between the current and next point
        resolution = 10
        for j in range(1, resolution):  # You can adjust the number of additional points as needed
            fraction = j / resolution
            lat = coordinates[i][0] + fraction * (coordinates[i + 1][0] - coordinates[i][0])
            lon = coordinates[i][1] + fraction * (coordinates[i + 1][1] - coordinates[i][1])
            high_resolution_coordinates.append([lat, lon])

    # Add the last point
    high_resolution_coordinates.append(coordinates[-1])

    # Add a marker for each coordinate
   # for coord in high_resolution_coordinates:
    #    folium.CircleMarker(location=coord, radius=1, fill_color='black', color='black').add_to(m)

    # Create a line between coordinates
    #folium.PolyLine(locations=high_resolution_coordinates, color='#f0914d', weight=3).add_to(m)
    # Create a line between coordinates
    poly_line = folium.PolyLine(locations=high_resolution_coordinates, color='#f0914d', weight=3)

    # Clear existing PolyLines in the FeatureGroup
    #route_group.clear_layers()
    # Add the new PolyLine to the FeatureGroup
    poly_line.add_to(route_group)

    # ship_icon = folium.Icon(icon='ship', prefix='fa', color='blue')
    # folium.Marker([high_resolution_coordinates[0][0], high_resolution_coordinates[0][1]],
    #              icon=ship_icon, popup=f"Ship\n{origin}").add_to(m)

    # Obtain the distance and time required for passage
    properties = route["properties"]

    print(properties)
    print(properties['length'])
    m.save('templates/map.html')
    return m, route_group

def returnGroup():
    return route_group
def returnProperties():
    return properties


def findCoordinates(departure, arrival):  # Read the CSV file into a DataFrame
    df = pd.read_csv('ports.csv')
    # print(departure)
    # print(arrival)
    # Extract the coordinates for each port
    port1_coordinates = df[df['Main Port Name'] == departure][['Latitude', 'Longitude']].values[0]
    port2_coordinates = df[df['Main Port Name'] == arrival][['Latitude', 'Longitude']].values[0]

    # Return the coordinates as a tuple of two tuples
    return port1_coordinates, port2_coordinates

# webbrowser.open('map_high_resolution.html')
