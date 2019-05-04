from . import optimize
from . import postprocess
from . import preprocess
__version__ = 'v0.1'


class Main:
    '''
    Purpose:
        Object representing software top-down. Main will house the management
        of everything from preprocess analytics and engineering to postprocess
        results and pipelines. More architectural complexity is outside the
        scope of this competition.

    Note:
        To simplify the demo, this code will manage a problem from the
        perspective of a rider. A rider will request a ride and that route will
        be created using Google's Operations Research tools. To simulate the
        platform appropriately I'll need to bump up the optimization complexity
        to involve a surplus of *pickups* and *deliveries* and not just run
        an expected route.

    TODO:
        A. Initialize rider. Get route. Calculate score. (first pass objective)
        B. Initialize rider within a set of potential drivers. Generate
        selective route. Calculate score.
        C. Initialize rider within a set of potential drivers and a surplus
        of *pickups* and *deliveries* (meaning that there will need to be
        optimization to maximize litter tossed and minimize distance). Generate
        selective route based off of a set of user-profile paramaters. Calculate
        score.
    '''
    def __init__(self):
        pass

    def initialize_rider(self, name:str, pickup:list, destination:list):
        '''
        Purpose:
            Create the rider.
        Args:
            name: string of the name of a user (TODO: user-id).
            pickup: list of [lat:float, lon:lon] where the rider requests to be
            picked up.
            destination : list of [lat:float, lon:float] where rider would like
            to be dropped off.
        '''
        self.rider = {
            'name': name,
            'origin': pickup,
            'destination': destination
        }

    def initialize_routes(self, model:dict):
        '''
        Purpose:
            Create the route.

        Args:
            model: model dict that is processed in the following format:
            Example: {
            'distance_matrix': [[int], ...], all to all with index-based location
            identification
            'pickups_deliveries': [[int], ...], route segment pool to optimize within
            'num_vehicles': int, must be generated in preprocessing module
            functionality (proximity/availablilty derrived number to provide
            potential routes)
            'depot': 0 for initial development all drivers will return home.
            }
        TODO:
            A. Simple, no arguments.
            B. Basic, maybe allow for proximity args.
            C. Advanced, allow for proximity args and 3rd-party peer-to-peer
            social media profile data.
        '''
        #model = preprocess.build_model_data() # TODO: expand on this
        self.routes = optimize.route(model)
        #self.route = optimize.route_from_scratch(model)

    def display_route(self):
        '''
        Purpose:
            Get data about route for visualization and manage its display.

        TODO:
            Plotly? How and where is this visualized?
        '''
        pass

    def describe_route(self):
        '''
        Purpose:
            Analyze the data about the route to represent its potential with
            respect to the platform's rankings.

        Notes:
            The idea with this function is to allow for a soft-touch on
            route configuration (i.e. if its not hitting enough litter -- tweak)
        '''
        pass
