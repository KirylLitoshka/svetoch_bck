from aiohttp.web import json_response, View
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import sessionmaker

from .models import Subsystem, Service
from .utils import pretty_json


class BaseView(View):
    def __init__(self, *args, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)
        self.session = sessionmaker(self.request.app["db"], class_=AsyncSession)


class SubsystemListView(BaseView):
    async def get(self):
        """
            ---
            description: description.
            tags:
            - SubSystems
            produces:
            - application/json
            responses:
                "200":
                    description: Successful operation. Return subsystem items
            """
        async with self.session() as session:
            result = await session.execute(
                select(Subsystem).order_by(Subsystem.id)
            )
            data = [item.to_json() for item in result.scalars()]
            return json_response(data, dumps=pretty_json)

    async def post(self):
        post_data = await self.request.post()
        async with self.session() as session:
            session.add(Subsystem(post_data["name"], post_data["alt_name"]))
            try:
                await session.commit()
                return json_response({"message": "new object has been created"}, status=201)
            except IntegrityError:
                return json_response({"message": f"object with {post_data['name']} already exists"}, status=409)


class SubsystemDetailView(BaseView):
    async def get(self):
        name = self.request.match_info["name"]
        async with self.session() as session:
            try:
                result = await session.execute(
                    select(Subsystem).where(Subsystem.name == name)
                )
                data = result.scalars().one().to_json()
            except NoResultFound:
                return json_response({"message": "Подсистема не найдена"}, status=404)
            return json_response(data, status=200, dumps=pretty_json)

    async def patch(self):
        pass

    async def post(self):
        pass

    async def delete(self):
        pass


class ServicesListView(BaseView):
    async def get(self):
        subsystem_name = self.request.match_info["name"]
        async with self.session() as session:
            result = await session.execute(
                select(Service).join(Subsystem).where(Subsystem.name == subsystem_name)
            )
            data = [item.to_json() for item in result.scalars()]
            if not data:
                return json_response(
                    {"message": f"Сервисы подсистемы {subsystem_name} не найдены"},
                    status=404,
                    dumps=pretty_json)
            return json_response(data=data, status=200, dumps=pretty_json)

    async def post(self):
        pass


class TestRun(BaseView):
    async def get(self):
        async with self.session() as session:
            result = await session.execute(
                """
                    SELECT
                        ss.id,
                        ss.name,
                        ss.alt_name,
                        ss."current_date",
                        json_agg(s.*) as services
                    FROM services s
                    JOIN subsystems ss  on ss.name = s.subsystem_name
                    group by ss.id
                    """
            )
            obj = result.scalars().first()
            return json_response(obj.to_json())
