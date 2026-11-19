import os

from dotenv import load_dotenv

load_dotenv()

PYTHON_ENV = os.getenv('PYTHON_ENV')
APP_ENV = os.getenv('APP_ENV')
SERVICE_NAME = os.getenv('SERVICE_NAME')
PORT = os.getenv('PORT')

IS_LOCAL = PYTHON_ENV != 'production'

PG_DATABASE = os.getenv('PG_DATABASE')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')

PG_READ_HOST = os.getenv('PG_READ_HOST') or PG_HOST
PG_READ_PORT = os.getenv('PG_READ_PORT') or PG_PORT
PG_READ_USER = os.getenv('PG_READ_USER') or PG_USER
PG_READ_PASSWORD = os.getenv('PG_READ_PASSWORD') or PG_PASSWORD
