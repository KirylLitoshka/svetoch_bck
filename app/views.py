from .utils import pretty_json
from .models import Subsystem
from aiohttp.web import json_response, View
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select


class BaseView(View):
    def __init__(self, *args, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)
        self.session = sessionmaker(self.request.app["db"], class_=AsyncSession)


class SubsystemListView(BaseView):
    async def get(self):
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
