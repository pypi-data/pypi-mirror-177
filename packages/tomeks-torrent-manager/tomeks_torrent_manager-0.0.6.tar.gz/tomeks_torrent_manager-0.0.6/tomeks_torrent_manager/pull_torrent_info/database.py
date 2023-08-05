import os
import sqlite3
import __main__
import sys

# db_filename = 'torrent_history.sqlite3.db'
# BASE_DIR = os.path.dirname(os.path.abspath(str(sys.modules['__main__'].__file__)))
# db_path = os.path.join(BASE_DIR, db_filename)
db_path = os.environ['SQLITE_DB']
# print(f"Using db file: {db_path}")

con = sqlite3.connect(db_path)
