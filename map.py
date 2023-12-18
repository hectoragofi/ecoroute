import sqlite3
import searoute
import folium
import pandas as pd
from folium import Map, Marker, Popup, plugins

import emissions_calculator


def runProgram():
    global route_group
    map_center = [48.8566, 2.3522]
    zoom_level = 4

    m = folium.Map(
        location=map_center,
        zoom_start=zoom_level,
        control_scale=True,
        zoom_control=False,
        max_zoom=12,
        min_zoom=2,
        max_bounds=[[39.7833, -122.4500], [37.7433, -122.4167]]
    )

    route_group = folium.FeatureGroup(name='Route').add_to(m)

    def createPortMarkers(connection):
        def add_marker_to_cluster(location, port_name, index_number):
            marker = Marker(location=location,
                            popup=Popup(f"Port: {port_name} ({index_number})"),
                            tooltip=port_name,
                            icon=folium.Icon(color='blue', icon='anchor', prefix='fa'))
            marker.add_to(marker_cluster)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ports")
        ports_data = cursor.fetchall()

        marker_cluster = plugins.MarkerCluster().add_to(m)

        for row in ports_data:
            latitude, longitude, port_name, index_number = row[1], row[2], row[3], row[0]
            location = (latitude, longitude)
            add_marker_to_cluster(location, port_name, index_number)

    # Connect to the SQLite database
    db_connection = sqlite3.connect('ports.db')

    createPortMarkers(db_connection)

    db_connection.close()

    m.save('templates/map.html')
    return m


def createLineRoute(origin, destination):
    global properties, route_group
    m = runProgram()
    origin1 = [origin[1], origin[0]]
    destination1 = [destination[1], destination[0]]

    route = searoute.searoute(origin1, destination1, speed_knot=12.5, units="naut")
    coordinates = route['geometry']['coordinates']
    coordinates = [[coord[1], coord[0]] for coord in coordinates]

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

    poly_line = folium.PolyLine(locations=high_resolution_coordinates, color='#0c25b0', weight=3)
    poly_line.add_to(route_group)

    distance = route["properties"]["length"]
    speed = 25

    mostEfficientShipType, mostEfficientFuelType = emissions_calculator.findMostEfficientShipAndFuelType(distance,
                                                                                                         speed)
    emissions, emission_types = emissions_calculator.calculateEmissions(mostEfficientShipType, mostEfficientFuelType,
                                                                        distance, speed)

    middle_index = len(high_resolution_coordinates) // 2
    middle_coordinate = high_resolution_coordinates[middle_index]

    co2_emission = emissions[0]
    co2_marker_text = f"Recommended ship type:{mostEfficientShipType}         CO2 Emissions: {co2_emission} kg"

    folium.Marker(location=middle_coordinate, popup=Popup(co2_marker_text),
                  icon=folium.Icon(color='blue', icon='ship', prefix='fa')).add_to(m)

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
    db_connection = sqlite3.connect('ports.db')
    cursor = db_connection.cursor()

    cursor.execute("SELECT * FROM ports WHERE \"Main Port Name\" = ?", (departure,))
    port1_data = cursor.fetchone()

    cursor.execute("SELECT * FROM ports WHERE \"Main Port Name\" = ?", (arrival,))
    port2_data = cursor.fetchone()

    db_connection.close()

    if not port1_data or not port2_data:
        return None, None

    port1_coordinates = (port1_data[1], port1_data[2])
    port2_coordinates = (port2_data[1], port2_data[2])

    return port1_coordinates, port2_coordinates
