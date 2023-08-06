from dataclasses import dataclass

@dataclass
class DBConfig:
    db_engine: str = None
    USER: str = None
    PASSWORD: str = None
    SERVER: str = None
    DB_NAME: str = None
    DRIVER: str = None