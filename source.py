import string
from typing import List
from db import DatabaseIdentity
from user import UserIdentity


class Source:
    def __init__(
        self,
        database: DatabaseIdentity,
        schema: string,
        include_tables: List[str],
        exclude_tables: List[str]
    ) -> None:
        self.database = database
        self.schema = schema
        self.include_tables = include_tables
        self.exclude_tables = exclude_tables
