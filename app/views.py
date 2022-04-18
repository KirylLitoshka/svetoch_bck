import re
from aiohttp.web import json_response

async def index(request):
    data = {"message": "hello world", "request method": request.method}
    return json_response(data)