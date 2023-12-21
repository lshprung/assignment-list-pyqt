import os
import sys
from time import strptime
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import assignment_list_pyqt.globals as Globals
from assignment_list_pyqt.group import Group
from assignment_list_pyqt.entry import Entry
from assignment_list_pyqt.rule import Rule

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
    query.exec_("DROP TABLE rules")

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

    query.exec_("""
        CREATE TABLE rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            entry_id REFERENCES entries (id),
            before_after TINYINT(1) DEFAULT TRUE,
            date TEXT NOT NULL,
            color VARCHAR(255) DEFAULT NULL,
            highlight VARCHAR(255) DEFAULT NULL
        )
        """)

    print(database.lastError().text())
        
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

    # Load rules
    Globals.rules = [] # Reset local rules array
    query.exec_("SELECT * FROM rules")
    while query.next():
        record = query.record()
        date_struct = strptime(record.field("date").value(), "%Y-%m-%d")
        date = QDate(date_struct.tm_year, date_struct.tm_mon, date_struct.tm_mday)
        Globals.rules.append(
                Rule(
                    record.field("id").value(),
                    record.field("entry_id").value(),
                    "before" if record.field("before_after").value() == 0 else "after",
                    date,
                    record.field("color").value(),
                    record.field("highlight").value()))

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

def insertRule(new_rule):
    """
    Insert rule to the database at Globals.db_path
    """
    output = -1

    database = QSqlDatabase.addDatabase("QSQLITE") # SQlite version 3
    database.setDatabaseName(Globals.db_path)

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error out. TODO consider throwing a dialog instead

    query = QSqlQuery()

    query.prepare("""
        INSERT INTO rules (entry_id, before_after, date, color, highlight) VALUES (:e_id, :when, :date, :color, :highlight)
        """)
    query.bindValue(":e_id", new_rule.entry_id)
    query.bindValue(":when", 0 if new_rule.when.lower() == "before" else 1)
    query.bindValue(":date", "{0}-{1}-{2}".format(
        new_rule.date.year(),
        new_rule.date.month(),
        new_rule.date.day()))
    query.bindValue(":color", new_rule.color)
    query.bindValue(":highlight", new_rule.highlight)
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

def updateRule(rule):
    """
    Update rule by its id
    """
    database = QSqlDatabase.addDatabase("QSQLITE") # SQlite version 3
    database.setDatabaseName(Globals.db_path)

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error out. TODO consider throwing a dialog instead

    query = QSqlQuery()

    query.prepare("""
        UPDATE rules SET 
            before_after = :when, 
            date = :date, 
            color = :color,
            highlight = :highlight
            WHERE id = :id
        """)
    query.bindValue(":when", 0 if rule.when.lower() == "before" else 1)
    query.bindValue(":date", "{0}-{1}-{2}".format(
        rule.date.year(),
        rule.date.month(),
        rule.date.day()))
    query.bindValue(":color", rule.color)
    query.bindValue(":highlight", rule.highlight)
    query.bindValue(":id", rule.id)
    success = query.exec_()
    # DEBUG
    #print(query.lastError().text())
    #print(query.boundValues())
    #if success:
    #    print("Query succeeded")
    #else:
    #    print("Query failed")

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

def removeRule(rule_id):
    """
    Remove a rule by id from the database 
    (we do not preserve rules, unlike groups and entries)
    """
    database = QSqlDatabase.addDatabase("QSQLITE") # SQlite version 3
    database.setDatabaseName(Globals.db_path)

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error out. TODO consider throwing a dialog instead

    query = QSqlQuery()

    # Set entry to hidden
    query.prepare("""
        DELETE FROM rules WHERE id = ?
        """)
    query.addBindValue(rule_id)
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

    # Remove rules associated with hidden entries
    query.exec_("""
        DELETE FROM rules WHERE id IN (
            SELECT rules.id FROM rules 
            INNER JOIN entries ON rules.entry_id = entries.id
            WHERE entries.hidden = 1
        )""")

    # Remove hidden entries
    query.exec_("""
        DELETE FROM entries WHERE hidden = 1
        """)

    # Remove hidden groups
    query.exec_("""
        DELETE FROM groups WHERE hidden = 1
        """)

    database.close()
