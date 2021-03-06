import asyncio
import json
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.settings import CONFIG_DIR
from app.utils import get_config, construct_db_url
from app.models import Base, Subsystem, Service

test_config = get_config(CONFIG_DIR)
DB_URL = construct_db_url(test_config["postgres"])


async def create_subsystem_data(session):
    async with session.begin():
        with open("test_data/subsystems.json") as data_file:
            subsystem_list = json.load(data_file)
        if not subsystem_list:
            raise

        for subsystem in subsystem_list:
            session.add(Subsystem(**subsystem))


async def create_services_data(session):
    async with session.begin():
        with open("test_data/services.json") as data_file:
            service_list = json.load(data_file)
        if not service_list:
            raise

        for service in service_list:
            session.add(Service(**service))


async def init_db():
    engine = create_async_engine(DB_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with session() as session:
        await create_subsystem_data(session)
        await create_services_data(session)

    await session.commit()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
