import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import cx_Oracle
from sqlalchemy.ext.declarative import declarative_base

ORACLE_HOST = "52.78.17.220"
ORACLE_PORT = "1521"
ORACLE_SID = "ORCLCDB"
ORACLE_USER = "ZCGNLP"
ORACLE_PASSWORD = "ZCGNLP"
ORACLE_SCHEMA = "ZCGNLP"

dsn = cx_Oracle.makedsn(ORACLE_HOST, ORACLE_PORT, sid=ORACLE_SID)
link = f"oracle://{ORACLE_USER}:{ORACLE_PASSWORD}@{dsn}"
engine = create_engine(
    link,
    echo=False,
    pool_pre_ping=True,
    encoding="utf-8",
    convert_unicode=False,
    pool_recycle=3600,
    pool_size=50,
    max_overflow=20,
    max_identifier_length=30,
)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
Base.metadata.schema = ORACLE_SCHEMA


@pytest.fixture(scope="session")
def test_db_session() -> Generator:
    sess = Session()
    try:
        yield sess
    finally:
        sess.close()
