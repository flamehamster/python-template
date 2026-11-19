import json
import sys

from fastapi.responses import JSONResponse

from config import IS_LOCAL
from models.http_errors import ApplicationException, HttpError


async def error_handler(_, error):
    if not isinstance(error, ApplicationException):
        error = HttpError.unknown_error(error)

    error_response = error.response
    stack = error_response.get('stack')

    if stack:
        print(
            json.dumps(
                {
                    'status': 'error',
                    'message': error_response.get('message', 'Application Error'),
                    'status_code': error_response['status_code'],
                    'stack': stack,
                },
                separators=(',', ':'),
            ),
            file=sys.stderr,
            flush=True,
        )

        if not IS_LOCAL:
            del error_response['stack']

    return JSONResponse(
        status_code=error_response['status_code'], content=error_response
    )
