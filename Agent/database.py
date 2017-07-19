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


def insert_symbol(symbol, connection, parent_id):
    if parent_id is None:
        raise ValueError('parent_id is None. Symbol cannot exists on it\'s own')
    cursor = connection.cursor()
    command_script = open(config('Database/insert_to_symbol'), 'r')
    command = command_script.read()
    command_script.close()
    cursor.execute(command, (symbol.shape, symbol.width, symbol.height, symbol.color, parent_id))
    connection.commit()
    return cursor.lastrowid


def insert_simple_object(simple_object, connection, parent_id=None):
    cursor = connection.cursor()
    command_file = open(config('Database/insert_to_simple_object'), 'r')
    command = command_file.read()
    command_file.close()
    cursor.execute(command, (simple_object.shape, simple_object.width, simple_object.height, simple_object.color,
                             simple_object.pattern, simple_object.pattern_color, parent_id))
    simple_object_id = cursor.lastrowid
    for symbol in simple_object.symbols:
        insert_symbol(symbol, connection, simple_object_id)
    connection.commit()
    return simple_object_id


def insert_combined_object(combined_object, connection):
    cursor = connection.cursor()
    command_file = open(config('Database/insert_to_combined_object'), 'r')
    command = command_file.read()
    command_file.close()
    cursor.execute(command, (combined_object.shape, combined_object.width, combined_object.height))
    combined_object_id = cursor.lastrowid
    for simple_object in combined_object.parts:
        insert_simple_object(simple_object, connection, combined_object_id)
    connection.commit()
    return combined_object_id


def _create_schema(connection):
    script = open(config('Database/create_schema_sql'), 'r')
    create_schema_sql = script.read()
    script.close()
    connection.cursor().executescript(create_schema_sql)
    connection.commit()


def _enable_foreign_keys(connection):
    connection.cursor().execute('PRAGMA foreign_keys = ON')
