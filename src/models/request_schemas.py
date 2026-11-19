from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class Schema:
    class ListExamples(BaseModel):
        limit: Annotated[int, Field(ge=1)] = 50
        skip: Annotated[int, Field(ge=0)] = 0
        before: datetime | None = None
        after: datetime | None = None

        model_config = {'extra': 'forbid'}

    class UpsertExample(BaseModel):
        name: Annotated[str, StringConstraints(min_length=3, max_length=50)]

        model_config = {'extra': 'forbid'}
