'''
Purpose:
    Provide engines with preprocessing module to simplify data prep and
    configuration.
'''
def build_model_data():
    '''
    Purpose:
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
        a set of potential routes, which is best for me.)

        Route: A -> B (litter 1) -> C (litter 2) -> D drop-off
    '''
    return {
        'pickups_deliveries': [[1, 2], [2, 3], [3, 4]], # A->B->C->D
        'distance_matrix': [
        [0, 10, 16, 21, 40],
        [10, 0, 6, 11, 30],
        [16, 4, 0, 5, 24]
        ], # All-to-all distance (very simple *almost* straight-line route)
        'num_vehicles': 1, # demo (eventually should be predicated on proximity/availablilty)
        'depot': 0 # requires a return home (driver finishes where he or she started)
    }
