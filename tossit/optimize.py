'''
Purpose:
    Google OR Tools *middle-ware* for optimization engine of tossit.

Notes:
    Starting simple, then integrating and adjusting.
'''
from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


# Google OR-tools template function
def print_solution(data, manager, routing, assignment):
    """Prints assignment on console."""
    total_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        total_distance += route_distance
    print('Total Distance of all routes: {}m'.format(total_distance))

def route(data:dict):
    '''
    Purpose:
        Generate route using model data.

    Args:
        data: preprocessed data representing subject model to optimize.
        Example: {
        'distance_matrix': [[int], ...], all to all with index-based location
        identification
        'pickups_deliveries': [[int], ...], route segment pool to optimize within
        'num_vehicles': int, must be generated in preprocessing module
        functionality (proximity/availablilty derrived number to provide
        potential routes)
        'depot': 0 for initial development all drivers will return home.
        }

    Notes:
        Starting with Google OR tools template code.
    '''
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Define cost of each arc.
    def distance_callback(from_index, to_index):
        """Returns the manhattan distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Define Transportation Requests.
    for request in data['pickups_deliveries']:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(
            routing.VehicleVar(pickup_index) == routing.VehicleVar(
                delivery_index))
        routing.solver().Add(
            distance_dimension.CumulVar(pickup_index) <=
            distance_dimension.CumulVar(delivery_index))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        print_solution(data, manager, routing, assignment)

    return None # TODO: define and return object for program utilization.


def route_from_scratch(data:dict):
    '''
    Purpose:
        Codefest's WiFi is slow, so it's taking a while to download
        dependancies. In case I can't utilize Google OR Tools in time, I'll
        use this function as a sandbox for pure MIP code (python/numpy-based
        VRP optimization from scratch).

    Args:
        data: preprocessed data representing subject model to optimize.
        Example: {
        'distance_matrix': [[int], ...], all to all with index-based location
        identification
        'pickups_deliveries': [[int], ...], route segment pool to optimize within
        'num_vehicles': int, must be generated in preprocessing module
        functionality (proximity/availablilty derrived number to provide
        potential routes)
        'depot': 0 for initial development all drivers will return home.
        }

    Note:
        Because of scope issues the optimization focuses on providing drivers
        with an optimized route. Riders choose from rider-friendly routes.
        Ideally optimization is more mutual, but I don't believe I'll be able to
        develop this before the conclusion of the hackathon.
    '''
    return None
