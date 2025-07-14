from sqlmodel import Field, SQLModel, Column
from sqlalchemy.dialects.postgresql import JSONB

class TableLabeling(SQLModel, table=True):
    __tablename__ = "table_labeling"
    __table_args__ = {"extend_existing": True}

    id: int | None = Field(default=None, primary_key=True)
    labels: list[str] | None = Field(default=None, sa_column=Column(JSONB))
    table: list[list[str]] = Field(sa_column=Column(JSONB))
    done: bool = Field(default=False)
