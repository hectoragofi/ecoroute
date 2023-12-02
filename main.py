from flask import *

import emissions_calculator
import map


app = Flask(__name__)

mapp = map.runProgram()


@app.route('/map')
def show_map():
    return render_template('map.html')

@app.route('/')
def index():
    return render_template('index.html', show_recommended_info=False)

@app.route('/show_data', methods=['POST'])
def show_data():
    if request.method == 'POST':
        departure_port = str(request.form.get('inputField1').title())
        arrival_port = str(request.form.get('inputField2').title())
        departureCoordinates, arrivalCoordinates = map.findCoordinates(departure_port, arrival_port)

        map.createLineRoute(departureCoordinates, arrivalCoordinates, mapp)

        distance = map.returnProperties()['length']
        speed = 25  # Update with your actual speed
        mostEfficientShipType, mostEfficientFuelType = emissions_calculator.findMostEfficientShipAndFuelType(distance, speed)

        # Calculate carbon emissions
        carbon_emissions, emission_types = emissions_calculator.calculateEmissions(mostEfficientShipType, mostEfficientFuelType, distance, speed)


        cars = 4.6  # metric tons of CO2 per year
        iphone15 = 66  # kg
        plasticBottles = 0.0850486  # kg per plastic bottle 500ml
        walking = 0.021  # kg per km
        theofficeepisode = 0.018  # kgCO2

        # Additional fun facts
        fun_facts = {
            "Cars": round(carbon_emissions[0] / (cars * 1000),2),  # Convert metric tons to kg
            "iPhone15": round(carbon_emissions[0] / iphone15),
            "Plastic Bottles": round(carbon_emissions[0] / plasticBottles),
            "Walking": round(carbon_emissions[0] / walking),
            "The Office Episode": round(carbon_emissions[0] / theofficeepisode)
        }

        # Render the template with the recommended ship, fuel, and emissions information
        return render_template(
            'index.html',
            show_recommended_info=True,
            ship_type=mostEfficientShipType,
            fuel_type=mostEfficientFuelType,
            emissions=carbon_emissions,
            emission_types=emission_types,
            fun_facts=fun_facts
        )

    # Handle other cases or errors
    return render_template('index.html', show_recommended_info=False)
if __name__ == '__main__':
    app.run(debug=True)