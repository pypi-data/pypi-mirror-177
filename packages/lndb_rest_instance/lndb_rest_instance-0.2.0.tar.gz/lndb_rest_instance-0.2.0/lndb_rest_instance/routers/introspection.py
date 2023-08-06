from typing import Any, Dict, List, Tuple

import lamindb as lamin
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/introspection")


class Column(BaseModel):
    key: str
    type: str
    primary_key: bool
    foreign_keys: List[Tuple[str, str]]
    nullable: bool
    default: Any


class Table(BaseModel):
    key: str
    primary_keys: List[str]
    foreign_keys: List[Tuple[str, str]]
    columns: Dict[str, Column]


class Database(BaseModel):
    key: str
    tables: Dict[str, Table]


@router.get("/", response_model=Database)
async def get_db_schema():
    schema = lamin.schema._core.get_db_metadata_as_dict()
    return schema


@router.get("/{table_name}")
async def get_table(table_name: str):
    # Rows
    table_df = lamin.select(getattr(lamin.schema, table_name)).df()
    rows = table_df.to_dict(orient="records")

    # Schema
    table_object = lamin.schema._core.get_table_object(table_name)
    schema = lamin.schema._core.get_table_metadata_as_dict(table_object)

    table_object

    return {"schema": schema, "rows": rows}
