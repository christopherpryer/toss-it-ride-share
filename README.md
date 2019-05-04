# toss-it-ride-share
Ride share with like-minded anti-litter Philadelphians.

## the idea
From the ground up this repo will be built around the VRP problem applied to
pickup and deliveries, where pickups and deliveries are both fellow ride-share
participants and identified public litter to be disposed.

## the functions
1. geo-tagged pickups and deliveries.
2. point to point route and litter clean up optimization.
3. ranking system.

## the vision
Ideally the functionality developed will be exposed to users through both mobile
and browser-based interfaces. Geographic location functionality should be
computed and managed under the hood. All the users should do is say they are
looking for a driver or a ride. Once the ride is established the team will both
complete the objective of bringing both the driver (optional) and the rider to
their respective destinations and rack up points by hitting either hotspots for
litter or identified items to be disposed.

# more detail
My goal is to learn how to use Google OR Tools. In the spirit of the competition
and it's theme (see [philly codefest](https://2019-philly-codefest.devpost.com/)),
this technology will be leveraged to initiate a *clean up program* to alleviate
the city and all its citizens of the growing pollution concern.

The theme of the hackathon is economic inequality. Performing some brain
gymnastics, this idea will bring together all levels of economic class for a
common goal. But gynastics aside, the competition lists that environmental
saftey is in fact a category of focus. So this falls under there.

#### Geo-tagged pickups and deliveries
This could be broken down into participants (seeking rides) and destinations.
Destinations can be further broken down into requested drop-offs and litter
pickups. Litter pickup *destinations* can be associated with either known
litter hotspots or geo-tagged items. *"Wait! If you're going to go out of
your way to tag litter, why not just pick it up?"* Well A. the *tagging* is
extremely scalable. So while at the start of this software's development the
*tagging* is very rudimentary and requires manual data entry, ideally this will
evolve into more passive *tagging*, making the argument that "it takes time to
*tag* so why not just clean up" less effective. B. some people just won't do
anything, and that's their nature. You're more likely to get them involved by
providing this alternative than changing their personality and such.

#### Point-to-point optimization
Google OR allows for you to program your custom VRP (vehicle routing problem)
and apply it in whatever fashion you'd like. In this case I'll be engineering
a [VRP with pickups and deliveries](https://developers.google.com/optimization/routing/pickup_delivery)
and theoretically *negative* [penalties and dropping visits](https://developers.google.com/optimization/routing/penalties) for this software. The idea is to maximize the amount of
litter you can toss out and minimize the route complication for the driver and
rider.

#### Ranking system
Another cool functionality would be to created a ranking and scoring system for
users. This could be built off of logic surrounding features such as litter
tossed, ride-time, participation, use frequency, etc.
