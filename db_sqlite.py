import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
Globals = __import__("globals")

def CreateTables(db_path):
    """
    Create database at a specified directory
    """
    database = QSqlDatabase.addDatabase("QSQLITE") # SQlite version 3
    database.setDatabaseName(db_path)

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error out. TODO consider throwing a dialog instead

    query = QSqlQuery()
    # Erase database contents so that we don't have duplicates
    query.exec_("DROP TABLE groups")
    query.exec_("DROP TABLE entries")

    query.exec_("""
        CREATE TABLE groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            column TINYINT(1) DEFAULT FALSE,
            link VARCHAR(255) NOT NULL,
            hidden TINYINT(1) DEFAULT FALSE
        )
        """)

    query.exec_("""
        CREATE TABLE entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            parent_id REFERENCES groups (id),
            description VARCHAR(255) NOT NULL,
            due_date TEXT DEFAULT NULL,
            alt_due_date VARCHAR(255) DEFAULT NULL,
            link VARCHAR(255) DEFAULT NULL,
            done TINYINT(1) DEFAULT FALSE,
            hidden TINYINT(1) DEFAULT FALSE
        )
        """)
        
    database.close()
