from dataclasses import dataclass
from lr_etl.Models.entities.db_config import DBConfig

@dataclass
class GeneralConfig:
    apiBaseUrl: str
    clienteName: str
    linkDownload: str
    tablename: str
    dataVersion: str
    weekday: int
    dbConfig: DBConfig