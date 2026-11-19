from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from models.request_schemas import Schema
from services.example_service import ExampleService

router = APIRouter()


@router.get('', status_code=200)
async def list_examples(query: Annotated[Schema.ListExamples, Query()]):
    return await ExampleService.list_examples(query)


@router.post('', status_code=201)
async def create_example(body: Schema.UpsertExample):
    return await ExampleService.create_example(body)


@router.patch('/{id}', status_code=204)
async def update_example(id: UUID, body: Schema.UpsertExample):
    return await ExampleService.update_example(id, body)


@router.delete('/{id}', status_code=204)
async def delete_example(id: UUID):
    return await ExampleService.delete_example(id)
