import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_PROD_CONNECTION = "mssql+pymssql://localhost/pycontacts"
DB_TEST_CONNECTION = "mssql+pymssql://localhost/pycontactstest"
logger = logging.getLogger(__name__)


class OrmBase(DeclarativeBase):
    pass


class Database():
    def __init__(self, connection_string: str = DB_PROD_CONNECTION, echo: bool = False):
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        self.echo = echo
        self.set_connection_string(connection_string)

    def set_connection_string(self, connection_string: str):
        self.engine = create_engine(connection_string, echo=self.echo)

    @property
    def SessionLocal(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_all(self):
        self.logger.info('Creating all tables')
        OrmBase.metadata.create_all(bind=self.engine)

    def drop_all(self):
        self.logger.info('Dropping all tables')
        OrmBase.metadata.drop_all(bind=self.engine)

    def get_db(self):
        self.logger.debug('Getting DB session')
        db = self.SessionLocal()
        try:
            yield db
        finally:
            self.logger.debug('Closing DB session')
            db.close()


db_instance = Database(DB_TEST_CONNECTION)


def connect_to_prod(with_echo: bool = False):
    global db_instance
    logger.debug(f'Connecting to prod DB (echo={with_echo})')
    db_instance.echo = with_echo
    db_instance.set_connection_string(DB_PROD_CONNECTION)


def connect_to_test(with_echo: bool = False):
    global db_instance
    logger.debug(f'Connecting to test DB (echo={with_echo})')
    db_instance.echo = with_echo
    db_instance.set_connection_string(DB_TEST_CONNECTION)
