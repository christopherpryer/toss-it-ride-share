import tossit as ts
import numpy as np

def get_ouput_sequence_sets(app):
    location_sets = []
    for vehicle in range(app.model_data['num_vehicles']):
        locations = set()
        i = app.output['routing'].Start(vehicle)
        locations.add(i)
        while not app.output['routing'].IsEnd(i):
            node_i = app.output['manager'].IndexToNode(i)
            prev_node_i = node_i
            i = app.output['assignment'].Value(app.output['routing'].NextVar(i))
            locations.add(i)
        location_sets.append(locations)
    return location_sets

def init_app():
    # psuedo route instruction params TODO: integrate
    pickup_location = np.array([39.961507, -75.175803])
    destination_location = np.array([39.945727, -75.152058])

    # init
    app = ts.Main()
    app.initialize_rider(
        name='Chris Pryer',
        pickup=pickup_location,
        destination=destination_location
    )

    return app

def test_rider(app):
    print('TESTING:>>Rider Created: ({})\n'.format(app.rider))

def test_routing(app):
    # could externalize the modeling of the problem:
    # TODO: use rider programmed data
    locations = ts.preprocess.get_basic_geo_array()
    locations = np.append(np.array([app.rider['origin']]), locations, axis=0)
    locations = np.append(locations, np.array([app.rider['destination']]), axis=0)
    data = ts.preprocess.build_model_data(len(locations))
    data['distance_matrix'] = ts.preprocess.build_distance_matrix(locations)
    app.initialize_routes(data)
    app.model_data['locations'] = locations

    # Print solution on console.
    print('TESTING:>>Routes Created:')
    if app.output['assignment']:
        ts.postprocess.print_solution(
            app.output['data'],
            app.output['manager'],
            app.output['routing'],
            app.output['assignment'])

    print('\nDEBUG:\norigin:\t\t{}'.format(app.model_data['locations'][0]))
    print('destination:\t{}'.format(app.model_data['locations'][-1]))
    indexes = get_ouput_sequence_sets(app)[0] # use one?
    print(sorted(indexes), len(app.model_data['demands']))
    demands = list(map(list(app.model_data['demands']).__getitem__, sorted(indexes)))
    print('points:\t\t{}'.format(demands))
    print('total pts:\t{}'.format(sum(demands)))

def test_display(app):
    locations = get_ouput_sequence_sets(app)[0] # use one
    app.display_route(sorted(list(locations)))


if __name__ == '__main__':
    app = init_app()

    # tests
    test_rider(app)
    test_routing(app)
    test_display(app)
