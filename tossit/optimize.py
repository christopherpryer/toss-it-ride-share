'''
Purpose:
    Google OR Tools *middle-ware* for optimization engine of tossit.

Notes:
    Starting simple, then integrating and adjusting.
'''
from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

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
        len(data['distance_matrix']),
        data['num_vehicles'],
        data['starts'],
        data['ends'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Allow to drop nodes.
    penalty = 1000
    for node in range(1, len(data['distance_matrix'])-1):
        routing.AddDisjunction([manager.NodeToIndex(node)], penalty)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    return {
        'data': data,
        'manager': manager,
        'routing': routing,
        'assignment': assignment
    }


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
