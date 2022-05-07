import string
from typing import List
from db import DatabaseIdentity
from user import UserIdentity


class Source:
    def __init__(
        self,
        database: DatabaseIdentity,
        schema: string,
        tables: List[str],
    ) -> None:
        self.database = database
        self.schema = schema
        self.tables = tables
