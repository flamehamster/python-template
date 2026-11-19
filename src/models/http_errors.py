import traceback

from fastapi.exceptions import RequestValidationError


class ApplicationException(Exception):
    def __init__(self, error):
        super().__init__()
        self.response = error.copy()


class HttpError:
    @staticmethod
    def invalid_request():
        return ApplicationException({'status_code': 400, 'type': 'invalid_request'})

    @staticmethod
    def resource_not_found():
        return ApplicationException({'status_code': 404, 'type': 'resource_not_found'})

    @staticmethod
    def method_not_allowed():
        return ApplicationException({'status_code': 405, 'type': 'method_not_allowed'})

    @staticmethod
    def validation_error(exception: RequestValidationError):
        detail = [
            {
                'path': error.get('loc', [])[1:],
                'message': error.get('msg', 'Validation error'),
            }
            for error in exception.errors()
        ]

        return ApplicationException(
            {'status_code': 422, 'type': 'validation_error', 'detail': detail}
        )

    @staticmethod
    def unknown_error(error):
        return ApplicationException(
            {
                'status_code': 500,
                'type': 'server_error',
                'stack': ''.join(
                    traceback.format_exception(type(error), error, error.__traceback__)
                ),
            }
        )

    @staticmethod
    def example_not_found():
        return ApplicationException({'status_code': 404, 'type': 'example_not_found'})
