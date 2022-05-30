import asyncio
import json
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.settings import CONFIG_DIR
from app.utils import get_config, construct_db_url
from app.models import Base, Renter

test_config = get_config(CONFIG_DIR)
DB_URL = construct_db_url(test_config["postgres"])


async def create_sample_data(obj, session):
    async with session.begin():
        with open(f"sample_data/{obj.__tablename__}.json") as file:
            objects_list = json.load(file)
            if not objects_list:
                raise

        for item in objects_list:
            session.add(obj(**item))


async def init_db():
    engine = create_async_engine(DB_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with session() as session:
        await create_sample_data(Renter, session)

    await session.commit()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
