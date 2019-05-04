'''
Purpose:
    Google OR Tools *middle-ware* for optimization engine of tossit.

Notes:
    Starting simple, then integrating and adjusting.
'''
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
