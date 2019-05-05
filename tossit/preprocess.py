'''
Purpose:
    Provide engines with preprocessing module to simplify data prep and
    configuration.

Notes:
    Distance calculation functionality can be done as part of this process or
    it can also be externalized. Since the problem scope is limited to Philly
    and/or mid-ranged proximity, haversine calculation will suffice in-app.
'''
from math import radians, cos, sin, asin, sqrt
import numpy as np

def haversine(lon1, lat1, lon2, lat2):
    '''
    Purpose:
        Calculate the great circle distance between two points
        on the earth.
    '''
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def get_basic_geo_array():
    '''
    Purpose:
        First pass representation of a set of points to model. For simplicity
        I'll generate a list of coordinates that starts with one driver's
        location, followed by the rider's pickup location, then a series of
        litter locations, and finally the destination for the rider.

    TODO:
        This should scale to be generated after the *ideal* driver is processed.
        In the simplest form the closest driver would be selected. It should
        also accept *all* or at least a surplus of locations corresponding to
        litter to toss. Finally the rider should be able to pass the destination
        of their ride.
    '''
    lats = np.random.uniform(low=39.94, high=39.96, size=(50,))
    lons = np.random.uniform(low=-75.17, high=-75.14, size=(50,))
    return np.array([np.array(pair) for pair in zip(lats, lons)])

def build_distance_matrix(geo_array:list):
    '''
    Purpose:
        Take an array (or list) of geocodes [[lat, lon], ...] pre-ordered and
        return a matrix of all to all distances using haversine calculations.
        The order of the matrix corresponds to the order of the geo_array.

    Args:
        geo_array: list of lists representing location geocodes. Example:
        [[float, float], ...]
    '''
    # simple nested loop to generate all to all
    # TODO: may need to scale as app scales
    distance_matrix = []
    for location_a in geo_array:
        tmp_matrix = [] # build all to all by-location
        for location_b in geo_array:
            tmp_matrix.append(
                haversine(location_a[0], location_b[1], location_b[0], location_b[1])
            )
        distance_matrix.append(tmp_matrix)
    return np.round(np.array(distance_matrix) * 1000, 0) # Google OR will convert to int

def build_model_data(n:int):
    '''
    Purpose:
        UPDATE: improved complexity.

        For the codefest I'll need to simplify a bunch of the fundamental
        aspects to this software in order to have a chance at demoing
        *anything*. To simplify the upront problem of having a set of data
        to simulate the experience the software provides, I'll present a
        standard model the engine will optimize. Example: A rider requests
        to be picked up and dropped off at two locations (A -> D). The driver
        is dispatched from his location to both pickup the rider and drop him
        or her off at their ultimate destination. Along the way there is litter
        that is identified as objectives prior to the arriving at D. After this
        is modeled, I'll expand on complexity. Ideally the solver should
        provide optimization for both the rider and the driver (i.e. from
        a set of potential routes, which is best for me).

        Route: A -> B (litter 1) -> C (litter 2) -> D drop-off

    Args:
        n: int of number of locations
    '''
    return { # rider is depot
        'demands': np.append(
            np.array([0]),
            np.append(
                np.random.randint(low=1, high=10, size=n-2),
                np.array([0]),
                axis=0),
            axis=0),
        'vehicle_capacities': [12], # TODO: improve
        #'pickups_deliveries': [[0, 4]],
        'distance_matrix': [
        [0, 10, 16, 21, 40],
        [10, 0, 6, 11, 30],
        [16, 4, 0, 5, 24],
        [21, 11, 5, 0, 19],
        [40, 30, 24, 19,0]
        ], # All-to-all distance (very simple *almost* straight-line route)
        'num_vehicles': 1, # demo (eventually should be predicated on proximity/availablilty)
        #'depot': 0, # requires a return home (driver finishes where he or she started)
        'starts': [0],
        'ends': [n-1]
    }
