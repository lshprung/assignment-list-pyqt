import os
import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
Globals = __import__("globals")
from group import Group

def initDB():
    """
    Check for existing database. If it doesn't exist, build it
    """
    if not os.path.exists(Globals.db_path):
        createTables()

    loadFromTables()

def createTables():
    """
    Create database at a specified Globals.db_path
    """
    database = QSqlDatabase.addDatabase("QSQLITE") # SQlite version 3
    database.setDatabaseName(Globals.db_path)

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

def loadFromTables():
    """
    Load groups and entries into global variables
    """
    database = QSqlDatabase.addDatabase("QSQLITE") # SQlite version 3
    database.setDatabaseName(Globals.db_path)

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error out. TODO consider throwing a dialog instead

    query = QSqlQuery()

    query.exec_("SELECT * FROM groups")
    while query.next():
        record = query.record()
        Globals.groups.append(
                Group(
                    record.field("id").value(), 
                    record.field("name").value(), 
                    record.field("column").value(),
                    record.field("link").value()))

    database.close()

def insertGroup(new_group):
    """
    Save groups and entries to the database at Globals.db_path
    """
    output = -1

    database = QSqlDatabase.addDatabase("QSQLITE") # SQlite version 3
    database.setDatabaseName(Globals.db_path)

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error out. TODO consider throwing a dialog instead

    query = QSqlQuery()

    query.prepare("""
        INSERT INTO groups (name, column, link) VALUES (?, ?, ?)
        """)
    query.addBindValue(new_group.name)
    query.addBindValue(new_group.column)
    query.addBindValue(new_group.link)
    query.exec_()

    output = query.lastInsertId()

    database.close()

    return output
