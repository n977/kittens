from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field

import sqlalchemy as sa


class BaseModel(SQLModel):
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={"server_default": sa.func.now(), "nullable": False},
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={
            "onupdate": sa.func.now(),
            "server_default": sa.func.now(),
            "nullable": False,
        },
    )
