from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_CONNECTION = "mssql+pymssql://localhost/pycontacts"
DB_TEST_CONNECTION = "mssql+pymssql://localhost/pycontactstest"


class OrmBase(DeclarativeBase):
    pass


class Database():
    def __init__(self, connection_string: str = DB_CONNECTION, echo: bool = True):
        self.engine = create_engine(connection_string, echo=echo)
        print(f"Database connected to {connection_string}")

    def set_connection_string(self, connection_string: str):
        print(f"Database connected to {connection_string}")
        self.engine = create_engine(connection_string)

    @property
    def SessionLocal(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_all(self):
        OrmBase.metadata.create_all(bind=self.engine)

    def drop_all(self):
        OrmBase.metadata.drop_all(bind=self.engine)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


db_instance = Database(DB_TEST_CONNECTION)


def create_db_prod_instance(with_echo: bool = True):
    global db_instance
    db_instance.set_connection_string(DB_CONNECTION)


def create_db_test_instance(with_echo: bool = True):
    global db_instance
    db_instance.set_connection_string(DB_TEST_CONNECTION)
