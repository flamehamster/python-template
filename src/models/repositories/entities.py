from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import Uuid

from libs.database import Base


class Example(Base):
    __tablename__ = 'examples'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    __table_args__ = (
        Index(
            'ix_examples_name_trgm',
            'name',
            postgresql_using='gin',
            postgresql_ops={'name': 'gin_trgm_ops'},
        ),
        Index('ix_examples_created_at', created_at.desc()),
        Index('ix_examples_updated_at', updated_at.desc()),
    )
