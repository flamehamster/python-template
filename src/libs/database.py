import asyncio

from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase

from config import (
    PG_DATABASE,
    PG_HOST,
    PG_PASSWORD,
    PG_PORT,
    PG_READ_HOST,
    PG_READ_PASSWORD,
    PG_READ_PORT,
    PG_READ_USER,
    PG_USER,
)


class Base(DeclarativeBase):
    def serialize(self):
        return {
            column.name: getattr(self, column.name)
            for column in inspect(self.__class__).columns
            if getattr(self, column.name) is not None
        }


writer_url = (
    f'postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'
)

reader_url = (
    f'postgresql+asyncpg://{PG_READ_USER}:{PG_READ_PASSWORD}'
    f'@{PG_READ_HOST}:{PG_READ_PORT}/{PG_DATABASE}'
)

writer_engine = create_async_engine(writer_url, pool_size=10)
reader_engine = create_async_engine(reader_url, pool_size=10)

PrimarySession = async_sessionmaker(writer_engine, expire_on_commit=False)
ReaderSession = async_sessionmaker(reader_engine, expire_on_commit=False)


async def run_database_migrations():
    alembic_cfg = Config('alembic.ini')
    await asyncio.to_thread(command.upgrade, alembic_cfg, 'head')


async def check_database_connections():
    async with writer_engine.connect() as connection:
        await connection.exec_driver_sql('SELECT 1')
    async with reader_engine.connect() as connection:
        await connection.exec_driver_sql('SELECT 1')
