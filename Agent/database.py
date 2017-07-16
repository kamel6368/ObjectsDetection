import sqlite3
import os.path
from Common.config import config


def connect():
    db_path = config('Database/path')
    if not os.path.isfile(db_path):
        connection = sqlite3.connect(db_path)
        _create_schema(connection)
    else:
        connection = sqlite3.connect(db_path)
    _enable_foreign_keys(connection)
    return connection


def _create_schema(connection):
    script = open(config('Database/create_schema_sql'), 'r')
    create_schema_sql = script.read()
    connection.cursor().executescript(create_schema_sql)
    connection.commit()


def _enable_foreign_keys(connection):
    connection.cursor().execute('PRAGMA foreign_keys = ON')
