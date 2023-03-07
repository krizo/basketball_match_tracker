from sqlmodel import create_engine, Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///db/{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


class DbConnection:
    _connection = None

    @property
    def connection(self) -> Session:
        if self._connection is None:
            self._connection = Session(engine)
        return self._connection

    def get_db(self) -> Session:
        return self.connection
