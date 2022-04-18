from yaml import safe_load


def get_config(path):
    with open(path) as config_file:
        config = safe_load(config_file)
    return config


def construct_db_url(config):
    dsn = "postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
    return dsn.format(**config)
