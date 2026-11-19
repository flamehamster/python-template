from collections.abc import Sequence
from typing import Any

from alembic import op
from sqlalchemy.sql.elements import ColumnElement, TextClause

IndexColumn = str | TextClause | ColumnElement[Any]


def create_index_concurrently(
    index_name: str,
    table_name: str,
    columns: Sequence[IndexColumn],
    *,
    unique: bool = False,
    schema: str | None = None,
    **dialect_options: Any,
) -> None:
    dialect_options['postgresql_concurrently'] = True

    with op.get_context().autocommit_block():
        op.create_index(
            index_name,
            table_name,
            columns,
            unique=unique,
            schema=schema,
            **dialect_options,
        )


def drop_index_concurrently(index_name: str, *, schema: str | None = None) -> None:
    with op.get_context().autocommit_block():
        op.drop_index(
            index_name, schema=schema, if_exists=True, postgresql_concurrently=True
        )
