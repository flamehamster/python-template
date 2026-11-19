from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from handlers.error_handler import error_handler
from handlers.method_not_allowed import method_not_allowed_handler
from handlers.resource_not_found import resource_not_found_handler
from handlers.validation_error import validation_error_handler
from libs.database import run_database_migrations
from routers.example_router import router as example_router
from routers.rpc_router import router as rpc_router


@asynccontextmanager
async def lifespan(app_: FastAPI):
    print('Running database migrations')
    await run_database_migrations()
    print('Server started')
    yield
    print('Shutting down...')


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(404, resource_not_found_handler)
app.add_exception_handler(405, method_not_allowed_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, error_handler)


@app.get('/')
def root():
    return {'status': 'ok'}


app.include_router(example_router, prefix='/examples')
app.include_router(rpc_router, prefix='/rpc')
