from sqlmodel import Field, SQLModel, Column
from sqlalchemy.dialects.postgresql import JSONB

class Table(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    labels: list[str] | None = Field(default=None, sa_column=Column(JSONB))
    table: list[list[str]] = Field(sa_column=Column(JSONB))
    done: bool = Field(default=False)
