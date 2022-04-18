from aiohttp import web
from .views import *

routes = [
    web.get("/api/v1/", index, name="index")
]