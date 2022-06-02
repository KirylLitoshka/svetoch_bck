from aiohttp.web import json_response, View
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import sessionmaker
from .models import Renter
from .utils import pretty_json


class BaseView(View):
    def __init__(self, *args, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)
        self.session = sessionmaker(self.request.app["db"], class_=AsyncSession)


class RentersView(BaseView):
    async def get(self):
        async with self.session() as session:
            try:
                result = await session.execute(
                    select(Renter).order_by(Renter.id)
                )
                data = [row.as_dict() for row in result.scalars()]
            except NoResultFound:
                return json_response({"message": "Арендаторы не найдены"}, status=404)
            return json_response(data, status=200, dumps=pretty_json)

    async def post(self):
        form_data = await self.request.post()
        data = {key: form_data[key] for key in form_data.keys()}
        async with self.session() as session:
            try:
                session.add(Renter(**data))
                await session.commit()
            except IntegrityError:
                return json_response({"message": f"Такой арендатор уже существует"}, status=409,
                                     dumps=pretty_json)
            except Exception as e:
                # Debug Exception (will be replaced)
                return json_response({"message": str(e)})
            return json_response({"message": "создано"}, status=201, dumps=pretty_json)
