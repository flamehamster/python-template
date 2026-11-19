from models.http_errors import HttpError


async def method_not_allowed_handler(_, __):
    raise HttpError.method_not_allowed()
