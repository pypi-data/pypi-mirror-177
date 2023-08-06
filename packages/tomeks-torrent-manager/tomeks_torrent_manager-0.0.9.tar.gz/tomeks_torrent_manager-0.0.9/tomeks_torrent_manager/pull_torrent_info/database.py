import os
import sqlite3
import __main__
import sys

db_path = os.environ['SQLITE_DB']

def get_con():
    return sqlite3.connect(db_path)
