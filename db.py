from user import UserIdentity


class DatabaseIdentity:
    def __init__(self, host, port, name, type, user: UserIdentity) -> None:
        self.host = host
        self.port = port
        self.name = name
        self.type = type
        self.user = user
