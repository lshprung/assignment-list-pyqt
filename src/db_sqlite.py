import os
import sys
from time import strptime
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import src.globals as Globals
from src.group import Group
from src.entry import Entry

def initDB():
    """
    Check for existing database. If it doesn't exist, build it
    """
    if not os.path.exists(Globals.db_path) or not os.stat(Globals.db_path).st_size:
        createTables()

    loadFromTables()

def createTables():
    """
    Create database at a specified Globals.db_path
    """
    print(Globals.db_path)
    database = QSqlDatabase.addDatabase("QSQLITE") # SQlite version 3
    database.setDatabaseName(Globals.db_path)

    # Create database parent directory if necessary
    if not os.path.exists(os.path.dirname(Globals.db_path)):
        try:
            os.mkdir(os.path.dirname(Globals.db_path))
        except:
            print("Unable to open data source file.")
            sys.exit(1)

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
            color VARCHAR(255) DEFAULT NULL,
            highlight VARCHAR(255) DEFAULT NULL,
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

    # Load groups
    Globals.groups = [] # Reset local groups array
    query.exec_("SELECT * FROM groups")
    while query.next():
        record = query.record()
        Globals.groups.append(
                Group(
                    record.field("id").value(), 
                    record.field("name").value(), 
                    record.field("column").value(),
                    record.field("link").value(),
                    record.field("hidden").value()))

    # Load entries
    Globals.entries = [] # Reset local entries array
    query.exec_("SELECT * FROM entries")
    while query.next():
        record = query.record()
        # create a QDate if the due date is set
        if record.field("due_date").value():
            due_date_struct = strptime(record.field("due_date").value(), "%Y-%m-%d")
            due_date = QDate(due_date_struct.tm_year, due_date_struct.tm_mon, due_date_struct.tm_mday)
        else:
            due_date = ""
        Globals.entries.append(
                Entry(
                    record.field("id").value(),
                    record.field("parent_id").value(),
                    record.field("description").value(),
                    due_date,
                    record.field("alt_due_date").value(),
                    record.field("link").value(),
                    record.field("color").value(),
                    record.field("highlight").value(),
                    record.field("done").value(),
                    record.field("hidden").value()))

    database.close()

def insertGroup(new_group):
    """
    Insert group to the database at Globals.db_path
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

def insertEntry(new_entry):
    """
    Insert entry to the database at Globals.db_path
    """
    output = -1

    database = QSqlDatabase.addDatabase("QSQLITE") # SQlite version 3
    database.setDatabaseName(Globals.db_path)

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error out. TODO consider throwing a dialog instead

    query = QSqlQuery()

    query.prepare("""
        INSERT INTO entries (parent_id, description, due_date, alt_due_date, link, color, highlight) VALUES (:p_id, :desc, :due, :alt_due, :link, :color, :highlight)
        """)
    query.bindValue(":p_id", new_entry.parent_id)
    query.bindValue(":desc", new_entry.desc)
    if new_entry.due:
        query.bindValue(":due", "{0}-{1}-{2}".format( 
                                                     new_entry.due.year(), 
                                                     new_entry.due.month(), 
                                                     new_entry.due.day()))
    else:
        query.bindValue(":due", "")
    query.bindValue(":alt_due", new_entry.due_alt)
    query.bindValue(":link", new_entry.link)
    query.bindValue(":color", new_entry.color)
    query.bindValue(":highlight", new_entry.highlight)
    success = query.exec_()
    # DEBUG
    #print(query.lastError().text())
    #print(query.boundValues())
    #if success:
    #    print("Query succeeded")
    #else:
    #    print("Query failed")

    output = query.lastInsertId()

    database.close()

    return output

def updateGroup(group):
    """
    Update group by its id
    """
    database = QSqlDatabase.addDatabase("QSQLITE") # SQlite version 3
    database.setDatabaseName(Globals.db_path)

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error out. TODO consider throwing a dialog instead

    query = QSqlQuery()

    query.prepare("""
        UPDATE groups SET name = ?, column = ?, link = ?, hidden = ? WHERE id = ?
        """)
    query.addBindValue(group.name)
    query.addBindValue(group.column)
    query.addBindValue(group.link)
    query.addBindValue(group.hidden)
    query.addBindValue(group.id)
    query.exec_()

    database.close()

def updateEntry(entry):
    """
    Update entry by its id
    """
    database = QSqlDatabase.addDatabase("QSQLITE") # SQlite version 3
    database.setDatabaseName(Globals.db_path)

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error out. TODO consider throwing a dialog instead

    query = QSqlQuery()

    query.prepare("""
        UPDATE entries SET 
            description = :desc, 
            due_date = :due, 
            alt_due_date = :alt_due, 
            link = :link,
            color = :color,
            highlight = :highlight,
            done = :done,
            hidden = :hidden
            WHERE id = :id
        """)
    query.bindValue(":desc", entry.desc)
    if entry.due:
        query.bindValue(":due", "{0}-{1}-{2}".format( 
                                                     entry.due.year(), 
                                                     entry.due.month(), 
                                                     entry.due.day()))
    else:
        query.bindValue(":due", "")
    query.bindValue(":alt_due", entry.due_alt)
    query.bindValue(":link", entry.link)
    query.bindValue(":color", entry.color)
    query.bindValue(":highlight", entry.highlight)
    query.bindValue(":done", entry.done)
    query.bindValue(":hidden", entry.hidden)
    query.bindValue(":id", entry.id)
    query.exec_()

    database.close()

def removeGroup(group_id):
    """
    Remove a group by id from the database 
    (actually set hidden to true, don't permanently delete it)
    """

    database = QSqlDatabase.addDatabase("QSQLITE") # SQlite version 3
    database.setDatabaseName(Globals.db_path)

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error out. TODO consider throwing a dialog instead

    query = QSqlQuery()

    # First, set entries to hidden
    query.prepare("""
        UPDATE entries SET hidden = 1 WHERE parent_id = ?
        """)
    query.addBindValue(group_id)
    query.exec_()

    # Now, set the group to hidden
    query.prepare("""
        UPDATE groups SET hidden = 1 WHERE id = ?
        """)
    query.addBindValue(group_id)
    query.exec_()

    output = query.numRowsAffected()
    database.close()
    return output

def removeEntry(entry_id):
    """
    Remove a group by id from the database 
    (actually set hidden to true, don't permanently delete it)
    """
    database = QSqlDatabase.addDatabase("QSQLITE") # SQlite version 3
    database.setDatabaseName(Globals.db_path)

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error out. TODO consider throwing a dialog instead

    query = QSqlQuery()

    # Set entry to hidden
    query.prepare("""
        UPDATE entries SET hidden = 1 WHERE id = ?
        """)
    query.addBindValue(entry_id)
    query.exec_()

    output = query.numRowsAffected()
    database.close()
    return output

def cleanHidden():
    """
    Permanently delete removed/hidden groups and entries
    """
    database = QSqlDatabase.addDatabase("QSQLITE") # SQlite version 3
    database.setDatabaseName(Globals.db_path)

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error out. TODO consider throwing a dialog instead

    query = QSqlQuery()

    # Remove hidden entries
    query.exec_("""
        DELETE FROM entries WHERE hidden = 1
        """)

    # Remove hidden groups
    query.exec_("""
        DELETE FROM groups WHERE hidden = 1
        """)

    database.close()
