from base64 import urlsafe_b64decode
from typing import Annotated
from uuid import UUID

from fastapi import Header
from pydantic import BaseModel

from models.http_errors import HttpError


class AccountContext(BaseModel):
    account_id: UUID


async def validate_account_context(
    header: Annotated[str | None, Header(alias='Account-Context')] = None,
) -> AccountContext:
    if not header:
        raise HttpError.invalid_request()

    try:
        return AccountContext.model_validate_json(urlsafe_b64decode(header))
    except ValueError:
        raise HttpError.invalid_request() from None
