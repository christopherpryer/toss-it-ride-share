import tossit as ts
import numpy as np

def test_rider(app):
    app.initialize_rider(
        name='Chris Pryer',
        pickup=pickup_location,
        destination=destination_location
    )
    print('TESTING:>>Rider Created: ({})\n'.format(app.rider))

def test_routing(app):
    # could externalize the modeling of the problem:
    # TODO: use rider programmed data
    locations = ts.preprocess.get_basic_geo_array()
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

def test_display(app):
    locations = set()
    i = app.output['routing'].Start(0)
    locations.add(i)
    while not app.output['routing'].IsEnd(i):
        node_i = app.output['manager'].IndexToNode(i)
        prev_node_i = node_i
        i = app.output['assignment'].Value(
            app.output['routing'].NextVar(prev_node_i)
        )
        locations.add(i)
    app.display_route(list(locations))



if __name__ == '__main__':
    app = ts.Main()

    # psuedo route instruction params TODO: integrate
    pickup_location = np.array([39.9571002,-75.1790366])
    #travel_delta = np.array([0.40, 0.10]) # create arbitrary route destination
    destination_location = np.array([39.948919, -75.160389])

    # tests
    test_rider(app)
    test_routing(app)
    test_display(app)
