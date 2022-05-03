from aiohttp import web
from .views import *

routes = [
    web.view("/api/v1/subsystems", SubsystemListView),
]
