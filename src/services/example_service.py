from uuid import UUID

from fastapi import Response

from models.http_errors import HttpError
from models.repositories.entities import Example
from models.repositories.example_repository import ExampleRepository
from models.request_schemas import Schema


class ExampleService:
    @staticmethod
    async def list_examples(input: Schema.ListExamples):
        result = await ExampleRepository.select(
            limit=input.limit, skip=input.skip, before=input.before, after=input.after
        )
        examples = [
            {
                'id': example.id,
                'name': example.name,
                'created_at': example.created_at,
                'updated_at': example.updated_at,
            }
            for example in result['examples']
        ]
        return {'examples': examples, 'has_more': result['has_more']}

    @staticmethod
    async def create_example(input: Schema.UpsertExample):
        new_example = await ExampleRepository.insert(Example(name=input.name))
        return {
            'id': new_example.id,
            'name': new_example.name,
            'created_at': new_example.created_at,
            'updated_at': new_example.updated_at,
        }

    @staticmethod
    async def update_example(id: UUID, input: Schema.UpsertExample):
        example = await ExampleRepository.select_one_by_id(id)
        if not example:
            raise HttpError.example_not_found()

        await ExampleRepository.update_one_by_id(id, Example(name=input.name))

        return Response(status_code=204)

    @staticmethod
    async def delete_example(id: UUID):
        example = await ExampleRepository.select_one_by_id(id)
        if not example:
            raise HttpError.example_not_found()

        await ExampleRepository.delete_one_by_id(id)

        return Response(status_code=204)
