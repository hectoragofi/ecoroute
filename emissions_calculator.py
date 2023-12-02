# Define the emission factors for each ship type and fuel type
emissionFactors = {
    "Tanker": {
        "HFO": [650, 18, 15, 2, 0.2],
        "MGO": [620, 1.5, 2.5, 0.5, 0.05],
        "LNG": [500, 0.001, 0.5, 0.1, 0.01]
    },
    "Bulk Carrier": {
        "HFO": [650, 15, 15, 2, 0.2],
        "MGO": [620, 1.5, 2.5, 0.5, 0.05],
        "LNG": [500, 0.001, 0.5, 0.1, 0.01]
    },
    "Container Ship": {
        "HFO": [650, 18, 15, 2, 0.2],
        "MGO": [620, 1.5, 2.5, 0.5, 0.05],
        "LNG": [500, 0.001, 0.5, 0.1, 0.01]
    },
    "General Cargo Ship": {
        "HFO": [650, 18, 15, 2, 0.2],
        "MGO": [620, 1.5, 2.5, 0.5, 0.05],
        "LNG": [500, 0.001, 0.5, 0.1, 0.01]
    }
}

# Define the specific energy content of each fuel type in kWh/kg
specificEnergyContent = {
    "HFO": 11.63,
    "MGO": 11.95,
    "LNG": 13.7
}

# Fuel Consumption rates for each ship type
fuelConsumptionRates = {
    "Tanker": {
        "HFO": 100,
        "MGO": 80,
        "LNG": 50
    },
    "Bulk Carrier": {
        "HFO": 90,
        "MGO": 70,
        "LNG": 40
    },
    "Container Ship": {
        "HFO": 110,
        "MGO": 90,
        "LNG": 60
    },
    "General Cargo Ship": {
        "HFO": 100,
        "MGO": 80,
        "LNG": 50
    }
}

def calculateEmissions(shipType, fuelType, distance, speed):
    fuelConsumption = distance * speed * fuelConsumptionRates[shipType][fuelType]
    energyConsumption = fuelConsumption * specificEnergyContent[fuelType]  # Convert to kWh

    emissionFactorsFunction = emissionFactors[shipType][fuelType]
    emissions = [energyConsumption * factor / 1000000 for factor in emissionFactorsFunction]  # Calculate emissions in kg
    emissionTypes = ["CO2", "CH4", "N2O", "SOx", "PM"]

    for i, value in enumerate(emissions):
        emissions[i] = round(value,2)

    return emissions, emissionTypes

def findMostEfficientShipAndFuelType(distance, speed):
    # Initialize variables to track the most efficient ship type and fuel type
    mostEfficientShipType = ''
    mostEfficientFuelType = ''
    minimumTotalEmissions = float('inf')

    # Iterate through all ship types and fuel types
    for ship_type in emissionFactors.keys():
        for fuel_type in emissionFactors[ship_type].keys():
            emissions, emission_types = calculateEmissions(ship_type, fuel_type, distance, speed)

            # Calculate the total emissions
            totalEmissions = sum(emissions)

            # Check if the current combination is more efficient than the previous best
            if totalEmissions < minimumTotalEmissions:
                mostEfficientShipType = ship_type
                mostEfficientFuelType = fuel_type
                minimumTotalEmissions = totalEmissions

    return mostEfficientShipType, mostEfficientFuelType


'''distance = 9171  # km
speed = 25.928  # km/h

mostEfficientShipType, mostEfficientFuelType = findMostEfficientShipAndFuelType(distance, speed)

print(f"Most efficient ship type: {mostEfficientShipType}")
print(f"Most efficient fuel type: {mostEfficientFuelType}")
print(f"Most efficient ship type: {calculateEmissions(mostEfficientShipType,mostEfficientFuelType,distance,speed)}")
'''