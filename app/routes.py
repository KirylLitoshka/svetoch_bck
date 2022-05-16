from aiohttp import web
from .views import *

routes = [
    web.view("/api/v1/subsystems", SubsystemListView),
    web.view("/api/v1/subsystems/{name}", SubsystemDetailView),
    web.view("/api/v1/subsystems/{name}/menu", ServicesListView)
]
