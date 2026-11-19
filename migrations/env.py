import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from alembic.autogenerate import rewriter
from alembic.autogenerate.render import _render_potential_expr, renderers
from alembic.operations import ops as alembic_ops
from sqlalchemy import pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncConnection, async_engine_from_config

# Allow revision files to import migrations/_helpers.py.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from libs.database import Base, writer_url
from models.repositories.entities import *


# ---------------------------------------------------------------------------
# Autogenerate rewriter for indexes
# ---------------------------------------------------------------------------
class _ConcurrentCreateIndexOp(alembic_ops.CreateIndexOp):
    """Same shape as CreateIndexOp; rendered by a dedicated dispatcher below."""


class _ConcurrentDropIndexOp(alembic_ops.DropIndexOp):
    """Same shape as DropIndexOp; rendered by a dedicated dispatcher below."""


def _render_concurrent_create_index(autogen_context, op):
    cols = ', '.join(
        _render_potential_expr(column, autogen_context, is_index=True)
        for column in op.columns
    )
    args = [f'{op.index_name!r}', f'{op.table_name!r}', f'[{cols}]']

    if op.schema:
        args.append(f'schema={op.schema!r}')

    if op.unique:
        args.append('unique=True')

    for key, value in op.kw.items():
        if key != 'postgresql_concurrently':
            rendered_value = _render_potential_expr(value, autogen_context)
            args.append(f'{key}={rendered_value}')

    return f'create_index_concurrently({", ".join(args)})'


def _render_concurrent_drop_index(autogen_context, op):
    args = [f'{op.index_name!r}']
    if op.schema:
        args.append(f'schema={op.schema!r}')
    return f'drop_index_concurrently({", ".join(args)})'


renderers.dispatch_for(_ConcurrentCreateIndexOp)(_render_concurrent_create_index)
renderers.dispatch_for(_ConcurrentDropIndexOp)(_render_concurrent_drop_index)


_rewriter = rewriter.Rewriter()


@_rewriter.rewrites(alembic_ops.CreateIndexOp)
def _rewrite_create_index(context, revision, op_):
    new_op = _ConcurrentCreateIndexOp(
        index_name=op_.index_name,
        table_name=op_.table_name,
        columns=list(op_.columns),
        unique=op_.unique,
        schema=op_.schema,
        **op_.kw,
    )
    return [new_op]


@_rewriter.rewrites(alembic_ops.DropIndexOp)
def _rewrite_drop_index(context, revision, op_):
    new_op = _ConcurrentDropIndexOp(
        index_name=op_.index_name,
        table_name=op_.table_name,
        schema=op_.schema,
        **op_.kw,
    )
    return [new_op]


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# this will overwrite the ini-file sqlalchemy.url path
# with the path given in the config of the main code
config.set_main_option('sqlalchemy.url', writer_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

MIGRATION_LOCK_ID = 0x4D494752
MIGRATION_LOCK_RETRY_SECONDS = 0.1
MIGRATION_LOCK_TIMEOUT_SECONDS = 300

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
        transaction_per_migration=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        process_revision_directives=_rewriter,
        transaction_per_migration=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def acquire_migration_lock(connection: AsyncConnection) -> None:
    loop = asyncio.get_running_loop()
    timeout_at = loop.time() + MIGRATION_LOCK_TIMEOUT_SECONDS

    while loop.time() < timeout_at:
        acquired = await connection.scalar(
            text('SELECT pg_try_advisory_lock(:lock_id)'),
            {'lock_id': MIGRATION_LOCK_ID},
        )
        await connection.commit()

        if acquired:
            return

        await asyncio.sleep(MIGRATION_LOCK_RETRY_SECONDS)

    raise TimeoutError('Timed out waiting for the migration lock')


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await acquire_migration_lock(connection)

        try:
            await connection.run_sync(do_run_migrations)
        finally:
            await connection.rollback()
            await connection.execute(
                text('SELECT pg_advisory_unlock(:lock_id)'),
                {'lock_id': MIGRATION_LOCK_ID},
            )
            await connection.commit()

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
