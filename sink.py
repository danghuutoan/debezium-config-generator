from db import DatabaseIdentity

class Sink:
    def __init__(self, database: DatabaseIdentity) -> None:
        self.database = database
