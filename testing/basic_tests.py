import tossit as ts
import numpy as np

def test_rider():
    app = ts.Main()

    # psuedo route instruction params
    pickup_location = np.array([39.9571002,-75.1790366])
    travel_delta = np.array([0.40, 0.10]) # create arbitrary route destination
    destination_location = (pickup_location + travel_delta)

    app.initialize_rider(
        name='Chris Pryer',
        pickup=pickup_location,
        destination=destination_location
    )
    print('TESTING:>>Rider Created: ({})\n'.format(app.rider))

def test_routing():
    app = ts.Main()

    # psuedo route instruction params
    pickup_location = np.array([39.9571002,-75.1790366])
    travel_delta = np.array([0.40, 0.10]) # create arbitrary route destination
    destination_location = (pickup_location + travel_delta)

    app.initialize_rider(
        name='Chris Pryer',
        pickup=pickup_location,
        destination=destination_location
    )

    # could externalize the modeling of the problem:
    # TODO: use rider programmed data
    locations = ts.preprocess.build_basic_geo_array()
    data = ts.preprocess.build_model_data()
    data['distance_matrix'] = ts.preprocess.build_distance_matrix(locations)
    app.initialize_routes(data)

    # Print solution on console.
    print('TESTING:>>Routes Created:')
    if app.output['assignment']:
        ts.postprocess.print_solution(
            app.output['data'],
            app.output['manager'],
            app.output['routing'],
            app.output['assignment'])

if __name__ == '__main__':
    test_rider()
    test_routing()
