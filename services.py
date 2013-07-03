__author__ = 'aparbane'

from web.joinhour.services.companion_ship_rating_service import CompanionShipRatingService
from protorpc.wsgi import service

app = service.service_mappings([('/companion_ship_rating_service', CompanionShipRatingService)])