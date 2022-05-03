from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine

from .utils import construct_db_url
from .routes import routes


async def init_db(app):
    db_url = construct_db_url(app["config"]["postgres"])
    app["db"] = create_async_engine(db_url, echo=True)


async def close_db(app):
    await app["db"].dispose()


def init_app(config):
    app = web.Application()
    app["config"] = config
    app.add_routes(routes)
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    return app
