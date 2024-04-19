from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:admin123@localhost:5432/lab4_2021"
DB_CONNECTION = "mssql+pymssql://localhost/pycontacts"
DB_TEST_CONNECTION = "mssql+pymssql://localhost/pycontactstest"

Base = declarative_base()

class Database():
    def __init__(self, connection_string: str = DB_CONNECTION, echo: bool = True):
        self.engine = create_engine(connection_string, echo=echo)

    @property
    def SessionLocal(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_all(self):
        Base.metadata.create_all(bind=self.engine)

    def drop_all(self):
        Base.metadata.drop_all(bind=self.engine)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


db_instance = Database()

def create_db_prod(with_echo: bool = True):
    db_instance = Database(DB_CONNECTION, with_echo)

def create_db_test(with_echo: bool = True):
    db_instance = Database(DB_TEST_CONNECTION, with_echo)
