from aiohttp import web
from aiohttp_swagger import setup_swagger
from app.main import init_app
from app.utils import get_config
from app.settings import CONFIG_DIR


def main():
    config = get_config(CONFIG_DIR)
    app = init_app(config)
    setup_swagger(app, swagger_url="api/v1/doc")
    web.run_app(app, host=config["host"], port=config["port"])


if __name__ == '__main__':
    main()
