import json
from .utils import pretty_json
from aiohttp.web import json_response

async def index(request):
    data = {"message": "hello world", "request_method": request.method}
    return json_response(data, dumps=pretty_json)