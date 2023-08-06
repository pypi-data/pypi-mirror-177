import urllib
from lr.Models.entities.db_config import DBConfig
from lr.Libs.log import LogWrapping
from sqlalchemy import orm
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from sqlalchemy_utils import database_exists, create_database


class DbSqlA():
    base        = declarative_base()
    def __init__(self,ConnectionString):
        self.engine             = sa.create_engine(ConnectionString, pool_size=40, max_overflow=40)
        self.session            = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=self.engine))
        self.base.query         = self.session.query_property()
        self.orm_session        = orm.scoped_session(orm.sessionmaker())(bind=self.engine)
        self.base.metadata.bind = self.engine    

    def create_all(self):
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        self.base.metadata.create_all(self.engine)


class Database:
    _engines = {
            "SQL Server": "mssql+pyodbc://{}:{}@{}/{}?driver={}",
            "Oracle": "mssql+pyodbc://{}:{}@{}/{}?driver={}"
        }

    def __init__(self, config: DBConfig) -> None:
        pwd = urllib.parse.quote_plus(config.PASSWORD)
        self._connection_string = self._engines[config.db_engine]
        self._connection_string = self._connection_string.format(
            config.USER, pwd, config.SERVER, config.DB_NAME, config.DRIVER
        )
        
    LogWrapping()
    def connect(self):
        db = DbSqlA(self._connection_string)
        return db
