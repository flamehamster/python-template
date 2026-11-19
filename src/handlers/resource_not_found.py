from models.http_errors import HttpError


async def resource_not_found_handler(_, __):
    raise HttpError.resource_not_found()
