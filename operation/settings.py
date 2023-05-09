import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# DBに接続
DIALECT = "mariadb"
DRIVER = "pymysql"
HOST = "mariadb"
USER = os.environ["MARIADB_USER"]
PASSWORD = os.environ["MARIADB_PASSWORD"]
DB_NAME = os.environ["MARIADB_DATABASE"]

Engine = create_engine(
    "{}+{}://{}:{}@{}:3306/{}?charset=utf8mb4".format(DIALECT, DRIVER, USER, PASSWORD, HOST, DB_NAME),
    echo = False
)

# Sessionの作成
Session = scoped_session(
    sessionmaker(
        autocommit = False,
        autoflush = True,
        bind = Engine
    )
)

Base = declarative_base()
Base.query = Session.query_property()