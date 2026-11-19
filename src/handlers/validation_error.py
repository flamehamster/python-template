from fastapi.exceptions import RequestValidationError

from models.http_errors import HttpError


async def validation_error_handler(_, exception: RequestValidationError):
    for error in exception.errors():
        type = error.get('type')
        if type == 'json_invalid':
            raise HttpError.invalid_request()
        if type == 'type_error.uuid':
            loc = error.get('loc', ())
            if loc and loc[0] == 'path':
                raise HttpError.resource_not_found()

    raise HttpError.validation_error(exception)
