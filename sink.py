from typing import List
from db import DatabaseIdentity


class Sink:
    def __init__(self, database: DatabaseIdentity, topics: List[str] = None) -> None:
        self.database = database
        if topics is None:
            topics = []
        self.topics = topics
