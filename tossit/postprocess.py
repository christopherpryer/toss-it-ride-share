'''
Purpose:
    Provide engines with postprocess module to handle analytics and ranking
    system.
TODO:
    Abstract into data models and pipelines.
'''
from __future__ import print_function
import math, numpy as np

# Google OR-tools template function
def print_solution(data, manager, routing, assignment):
    """Prints assignment on console."""
    # Display dropped nodes.
    dropped_nodes = []
    dropped_nodes_msg = 'Total dropped nodes: {}'
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        if assignment.Value(routing.NextVar(node)) == node:
            dropped_nodes.append(manager.IndexToNode(node))
    print(dropped_nodes_msg.format(len(dropped_nodes)))
    # Display routes
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Points({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Points({1})\n'.format(
            manager.IndexToNode(index), route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance/100)
        plan_output += 'Points of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total Distance of all routes: {}m'.format(total_distance/100))
    print('Total Points of all routes: {}'.format(total_load))

class Map(object):
    '''
    Purpose:
        First pass map visual from the ground up using Google Maps and
        geocode smoothing.

    Credit:
        Adam Votava (https://blog.alookanalytics.com/2017/02/05/how-to-plot-
        your-own-bikejogging-route-using-python-and-google-maps-api/)
        and subsequent stack overflow (etc.) developers.
    '''
    def __init__(self):
        self._points = []

    def add_point(self, coordinates):
        """
        Adds coordinates to map
        :param coordinates: latitude, longitude
        :return:
        """

        # add only points with existing coordinates
        if not ((math.isnan(coordinates[0])) or (math.isnan(coordinates[1]))):
            self._points.append(coordinates)

    @staticmethod
    def _lat_rad(lat):
        """
        Helper function for _get_zoom()
        :param lat:
        :return:
        """
        sinus = math.sin(math.radians(lat + math.pi / 180))
        rad_2 = math.log((1 + sinus) / (1 - sinus)) / 2
        return max(min(rad_2, math.pi), -math.pi) / 2

    def _get_zoom(self, map_height_pix=900, map_width_pix=1900, zoom_max=21):
        """
        Algorithm to derive zoom from the activity route. For details please see
         - https://developers.google.com/maps/documentation/javascript/maptypes#WorldCoordinates
         - http://stackoverflow.com/questions/6048975/google-maps-v3-how-to-calculate-the-zoom-level-for-a-given-bounds
        :param zoom_max: maximal zoom level based on Google Map API
        :return:
        """

        # at zoom level 0 the entire world can be displayed in an area that is 256 x 256 pixels
        world_heigth_pix = 256
        world_width_pix = 256

        # get boundaries of the activity route
        max_lat = max(x[0] for x in self._points)
        min_lat = min(x[0] for x in self._points)
        max_lon = max(x[1] for x in self._points)
        min_lon = min(x[1] for x in self._points)

        # calculate longitude fraction
        diff_lon = max_lon - min_lon
        if diff_lon < 0:
            fraction_lon = (diff_lon + 360) / 360
        else:
            fraction_lon = diff_lon / 360

        # calculate latitude fraction
        fraction_lat = (self._lat_rad(max_lat) - self._lat_rad(min_lat)) / math.pi

        # get zoom for both latitude and longitude
        zoom_lat = math.floor(math.log(map_height_pix / world_heigth_pix / fraction_lat) / math.log(2))
        zoom_lon = math.floor(math.log(map_width_pix / world_width_pix / fraction_lon) / math.log(2))

        return min(zoom_lat, zoom_lon, zoom_max)

    def __str__(self):
        """
        A Python wrapper around Google Map Api v3; see
         - https://developers.google.com/maps/documentation/javascript/
         - https://developers.google.com/maps/documentation/javascript/examples/polyline-simple
         - http://stackoverflow.com/questions/22342097/is-it-possible-to-create-a-google-map-from-python
        :return: string to be stored as html and opened in a web browser
        """
        # center of the activity route
        center_lat = (max((x[0] for x in self._points)) + min((x[0] for x in self._points))) / 2
        center_lon = (max((x[1] for x in self._points)) + min((x[1] for x in self._points))) / 2

        # get zoom needed for the route
        zoom = self._get_zoom()

        # string with points for the google.maps.Polyline
        activity_coordinates = ",\n".join(
            ["{{lat: {lat}, lng: {lon}}}".format(lat=x[0], lon=x[1]) for x in self._points])

        return """
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
            <div id="map-canvas" style="height: 100%; width: 100%"></div>
            <script type="text/javascript">
                var map;
                function show_map() {{
                    map = new google.maps.Map(document.getElementById("map-canvas"), {{
                        zoom: {zoom},
                        center: new google.maps.LatLng({center_lat}, {center_lon}),
                        mapTypeId: 'terrain'
                    }});

                    var activity_coordinates = [{activity_coordinates}]

                    var activity_route = new google.maps.Polyline({{
                        path: activity_coordinates,
                        geodesic: true,
                        strokeColor: '#FF0000',
                        strokeOpacity: 1.0,
                        strokeWeight: 2
                        }});

                        activity_route.setMap(map);
                }}
                google.maps.event.addDomListener(window, 'load', show_map);
            </script>
        """.format(zoom=zoom, center_lat=center_lat, center_lon=center_lon, activity_coordinates=activity_coordinates)
