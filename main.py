#!/usr/bin/env python
##
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


# TODO: change
__author__  = 'Constantin Kostenko with templates by Rodrigo Augosto'
__website__ = 'www.JoinHour.com'

import os, sys
# Third party libraries path must be fixed before importing webapp2
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'boilerplate/external'))

import webapp2

import routes
from boilerplate import routes as boilerplate_routes
from admin import routes as admin_routes
from boilerplate import config as boilerplate_config
from src.joinhour.models.building import Building
from google.appengine.ext import ndb
# Added for Stat
#from web import routes as stat_routes
#from web import routes as routes
import routes as routes

import config
from boilerplate.lib.basehandler import handle_error

webapp2_config = boilerplate_config.config
webapp2_config.update(config.config)

app = webapp2.WSGIApplication(debug = os.environ['SERVER_SOFTWARE'].startswith('Dev'), config=webapp2_config)
# uncomment the line below and comment the line above for the deployment to Prod. Don't check-in the prod change into GitHub
#app = webapp2.WSGIApplication(debug = os.environ['SERVER_SOFTWARE'].startswith('Google'), config=webapp2_config)

for status_int in app.config['error_templates']:
    app.error_handlers[status_int] = handle_error

routes.add_routes(app)
boilerplate_routes.add_routes(app)
admin_routes.add_routes(app)

buildings = ["River Place North",
             "River Place South",
             "River Place West",
             "River Place East",
             "Crystal Towers",
             "Meridian at Courthouse Commons (Phase I)",
             "Oakwood Falls Church",
             "Courtland Towers",
             "Arlington Courthouse Place",
             "The Belvedere",
             "Randolph Towers",
             "Post Pentagon Row",
             "Crystal House I and 2",
             "The Eclipse on Center Park",
             "Meridian At Ballston",
             "Clarendon 1021",
             "The Continental",
             "Potomac Towers",
             "Windsor at Shirlington Village",
             "Wildwood Park",
             "Gramercy at Metropolitan Park",
             "Archstone Courthouse Plaza",
             "Lenox Club",
             "Meridian at Pentagon City",
             "Crystal Square",
             "Rosslyn Heights",
             "Dolley Madison Towers",
             "Water Park Towers",
             "Richmond Square",
             "Quincy Plaza",
             "The Atrium",
             "Bennington, The",
             "Avalon at Ballston - Washington Towers",
             "1401 Joyce on Pentagon Row",
             "Metropolitan At Pentagon City The",
             "Hyde Park Condominiums",
             "Dominion Plaza",
             "Archstone Rosslyn",
             "Station Square at Clarendon",
             "The Odyssey",
             "Residences At The Market Common, The",
             "Archstone Pentagon City",
             "Horizon House",
             "Alta Vista Condominiums",
             "Prime at Arlington Courthouse, The",
             "Halstead Arlington, The",
             "The Williamsburg",
             "Courtland Park",
             "Palatine apartments",
             "Tower Villas",
             "Turnberry Tower",
             "IO Piazza by Windsor",
             "IO Piazza",
             "Parc Rosslyn",
             "Madison at Ballston Station, The",
             "The Residences at Liberty Center I",
             "Archstone Virginia Square",
             "Liberty Tower",
             "Virginia Square Plaza",
             "1001 EastView",
             "South Hampton",
             "2201 Wilson Blvd",
             "Whitmore, The",
             "Twenty400",
             "Barton House",
             "Crescent",
             "Lofts 590, The",
             "The Park at Courthouse",
             "The Representative",
             "Bella Vista",
             "Gables 12 Twenty One",
             "1020 N. Quincy St.",
             "Lexington Square Condominiums 1 & 2",
             "Park Adams",
             "The Cavendish",
             "The Phoenix at Clarendon Metro",
             "Waterview - Condo",
             "Windsor Plaza",
             "Crystal Place",
             "Crystal Park Condominiums",
             "Virginia Square Condominiums",
             "Crystal Gateway Condominiums",
             "Summerwalk",
             "Shirlington Crest",
             "Woodbury Heights Condominiums",
             "The Charleston",
             "Lexington Square Condominiums 3 & 4",
             "Falls Station",
             "1800 Wilson Blvd.",
             "Shirlington Village Condominiums",
             "Ballston Park",
             "The Hawthorn",
             "1001 WestView",
             "Wildwood Towers",
             "Courthouse Hill",
             "The Westlee",
             "Barkley Condominiums",
             "Ballston 880",
             "Gaslight Square",
             "2121",
             "Amelia, The",
             "Frederick at Courthouse, The",
             "Hilltop House 100",
             "Normandy House",
             "Rhodes Hills Square",
             "The Ridge House",
             "Berkeley at Ballston",
             "The Monroe",
             "Hartford Apartments",
             "Waterford House",
             "1633 Colonial Terrace",
             "Lyon Place at Clarendon Center",
             "Clarendon Apartments"]

for building in buildings:
    build = Building.query(Building.building_name==building).get()
    if not build:
        build = Building(building_name = building, online = False)
        build.put()

