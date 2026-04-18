from models.connection import Connection


class ConnectionManager:
    _instance: "ConnectionManager | None" = None

    def __new__(cls) -> "ConnectionManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connections = []
        return cls._instance

    @property
    def connections(self) -> list[Connection]:
        return self._connections

    def add(self, connection: Connection) -> None:
        self._connections.append(connection)

    def remove(self, connection: Connection) -> None:
        self._connections.remove(connection)

    def get_by_username(self, username: str) -> Connection | None:
        for connection in self._connections:
            if connection.username.lower() == username.lower():
                return connection
        return None


manager = ConnectionManager()
