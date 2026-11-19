from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, delete, desc, insert, update
from sqlalchemy.future import select

from libs.database import PrimarySession, ReaderSession
from models.repositories.entities import Example


class ExampleRepository:
    @staticmethod
    async def insert(example: Example):
        async with PrimarySession() as session, session.begin():
            query = insert(Example).values(example.serialize()).returning(Example)
            result = await session.scalars(query)
            return result.one_or_none()

    @staticmethod
    async def select(
        limit: int,
        skip: int,
        before: datetime | None = None,
        after: datetime | None = None,
    ):
        async with ReaderSession() as session:
            query = select(Example)

            conditions = []
            if before:
                conditions.append(Example.created_at < before)
            if after:
                conditions.append(Example.created_at > after)

            if conditions:
                query = query.where(and_(*conditions))

            query = (
                query.order_by(desc(Example.created_at)).limit(limit + 1).offset(skip)
            )

            result = await session.scalars(query)
            examples = result.all()
            has_more = len(examples) > limit

            return {
                'examples': examples[:limit] if has_more else examples,
                'has_more': has_more,
            }

    @staticmethod
    async def select_one_by_id(id: UUID):
        async with ReaderSession() as session:
            query = select(Example).where(Example.id == id)
            result = await session.scalars(query)
            return result.first()

    @staticmethod
    async def update_one_by_id(id: UUID, example: Example):
        async with PrimarySession() as session, session.begin():
            query = update(Example).where(Example.id == id).values(example.serialize())
            await session.execute(query)

    @staticmethod
    async def delete_one_by_id(id: UUID):
        async with PrimarySession() as session, session.begin():
            query = delete(Example).where(Example.id == id)
            await session.execute(query)
