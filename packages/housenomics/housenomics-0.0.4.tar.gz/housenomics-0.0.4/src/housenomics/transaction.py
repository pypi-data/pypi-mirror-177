from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    date_of_movement: datetime
    description: str
    value: Optional[float]
