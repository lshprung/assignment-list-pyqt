#!/usr/bin/python3
import os
import sys
import time
from PyQt5 import uic
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QMenu, QMessageBox, QVBoxLayout
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QDate, Qt
from assignment_list_pyqt.config import Config
from assignment_list_pyqt.preferences_dialog import PreferencesDialog
from assignment_list_pyqt.add_group_form import addGroupForm
from assignment_list_pyqt.edit_group_form import editGroupForm
from assignment_list_pyqt.add_entry_form import addEntryForm
from assignment_list_pyqt.edit_entry_form import editEntryForm
import assignment_list_pyqt.globals as Globals
import assignment_list_pyqt.db_sqlite as DB
from assignment_list_pyqt.rules_dialog import RulesDialog

class AssignmentList(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                   "main.ui"), self)

        self.initializeUI()

    def initializeUI(self):
        self.createMenu()
        self.createToolbar()
        Config()
        self.setupDB()
        self.displayWidgets()
        self.show()

    def createMenu(self):
        self.actionPreferences.triggered.connect(self.preferences)
        self.actionReload.triggered.connect(self.reload)
        self.actionExit.triggered.connect(self.close)

        self.actionAdd_Group.triggered.connect(self.addGroup)
        self.actionClean_Hidden.triggered.connect(self.cleanHidden)

        self.actionAbout.triggered.connect(self.aboutDialog)

    def createToolbar(self):
        self.toolBar.addAction(self.actionAdd_Group)

    def setupDB(self):
        DB.initDB()

    def displayWidgets(self):
        self.title.setText(time.strftime("%A, %b %d %Y"))
        self.drawGroups()

    def addGroup(self):
        """
        Open the 'addGroup' form
        """
        old_count = len(Globals.groups)
        self.create_new_group_dialog = addGroupForm()
        if old_count != len(Globals.groups):
            self.drawGroups()

    def editGroup(self, id):
        """
        Open the 'editGroup' form
        """
        self.create_edit_group_dialog = editGroupForm(id)
        self.drawGroups()

    def removeGroup(self, id):
        """
        Delete a group with a given id
        """
        # TODO might want to add a warning
        # TODO might want to make part of the a destructor in the Group class
        removed = DB.removeGroup(id)
        if removed > 0:
            Globals.entries = list(filter(lambda e: e.parent_id != id, Globals.entries))
            Globals.groups = list(filter(lambda g: g.id != id, Globals.groups))
            self.drawGroups()

    def groupContextMenu(self, group_id):
        menu = QMenu()

        add_entry_act = QAction("Add Entry")
        add_entry_act.triggered.connect((lambda id: lambda: self.addEntry(id))(group_id))
        menu.addAction(add_entry_act)

        edit_group_act = QAction("Edit Group")
        edit_group_act.triggered.connect((lambda id: lambda: self.editGroup(id))(group_id))
        menu.addAction(edit_group_act)

        del_group_act = QAction("Remove Group")
        del_group_act.triggered.connect((lambda id: lambda: self.removeGroup(id))(group_id))
        menu.addAction(del_group_act)

        menu.exec_(QCursor.pos())

    def addEntry(self, parent):
        """
        Open the 'addEntry' form
        """
        old_count = len(Globals.entries)
        self.create_new_entry_dialog = addEntryForm(parent)
        if old_count != len(Globals.entries):
            self.drawGroups() # TODO see if we can do this with only redrawing a single group

    def editEntry(self, id):
        """
        Open the 'editEntry' form
        """
        self.create_edit_entry_dialog = editEntryForm(id)
        self.drawGroups()

    def toggleDoneEntry(self, id):
        """
        Toggle the 'done' flag on the entry with the given id
        """
        entry = list(filter(lambda e: e.id == id, Globals.entries))[0]
        if entry.done:
            entry.done = False
        else:
            entry.done = True
        DB.updateEntry(entry)
        Globals.entries = list(filter(lambda e: e.id != id, Globals.entries))
        Globals.entries.append(entry)
        self.drawGroups()

    def removeEntry(self, id):
        """
        Delete an entry with a given id
        """
        # TODO might want to add a warning
        # TODO might want to make part of the a destructor in the Entry class
        removed = DB.removeEntry(id)
        if removed > 0:
            Globals.entries = list(filter(lambda e: e.id != id, Globals.entries))
            self.drawGroups()

    def editRules(self, id):
        pass
        need_reload = RulesDialog(id)
        if need_reload:
            self.reload()

    def entryContextMenu(self, entry_id):
        menu = QMenu()

        edit_entry_act = QAction("Edit Entry")
        edit_entry_act.triggered.connect((lambda id: lambda: self.editEntry(id))(entry_id))
        menu.addAction(edit_entry_act)

        rules_act = QAction("Rules")
        rules_act.triggered.connect((lambda id: lambda: self.editRules(id))(entry_id))
        menu.addAction(rules_act)

        mark_done_act = QAction("Done", checkable=True)
        if list(filter(lambda e: e.id == entry_id, Globals.entries))[0].done:
            mark_done_act.setChecked(True)
        mark_done_act.triggered.connect((lambda id: lambda: self.toggleDoneEntry(id))(entry_id))
        menu.addAction(mark_done_act)

        del_entry_act = QAction("Remove Entry")
        del_entry_act.triggered.connect((lambda id: lambda: self.removeEntry(id))(entry_id))
        menu.addAction(del_entry_act)

        menu.exec_(QCursor.pos())

    def preferences(self):
        # TODO not sure if this is working exactly how I think it does, but it works
        need_reload = PreferencesDialog()
        if need_reload:
            self.reload()

    def cleanHidden(self):
        """
        Permanently delete removed groups and entries from db
        """
        # TODO consider creating a warning dialogue for this
        DB.cleanHidden()

    def drawGroups(self):
        """
        Redraw the groups_layout
        """
        # Remove all children from layout
        def recursiveClear(layout):
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
                elif child.layout():
                    recursiveClear(child)

        recursiveClear(self.groups_layout)

        # Sort the groups
        Globals.groups = sorted(Globals.groups, key=lambda g: g.id)

        # Sort the entries
        Globals.entries = sorted(Globals.entries, key=lambda e: (e.parent_id, (e.due if e.due else QDate.currentDate()), e.done, e.id))

        # Sort the rules
        Globals.rules = sorted(Globals.rules, key=lambda r: (r.id))

        # Create columns as vertical boxes
        column_left = QVBoxLayout()
        column_right = QVBoxLayout()

        for g in Globals.groups:
            # skip if this group is set to hidden
            if g.hidden:
                continue

            g_layout = g.buildLayout()

            # Create custom context menu
            g_layout.itemAt(0).widget().setToolTip("Right-Click for actions")
            g_layout.itemAt(0).widget().setContextMenuPolicy(Qt.CustomContextMenu)
            g_layout.itemAt(0).widget().customContextMenuRequested.connect((lambda id: lambda: self.groupContextMenu(id))(g.id))
            
            # Draw entries belonging to this group
            g_layout.addLayout(self.drawEntries(g.id))

            if g.column.lower() == "left":
                column_left.addLayout(g_layout)
            else:
                column_right.addLayout(g_layout)

        column_left.addStretch()
        column_right.addStretch()

        self.groups_layout.addLayout(column_left, 0, 0)
        self.groups_layout.addLayout(column_right, 0, 1)

    def drawEntries(self, group_id):
        """
        Redraw the entries of a specific group
        """
        # TODO consider having code to remove existing widgets to make this function more modular
        entries = list(filter(lambda e: e.parent_id == group_id, Globals.entries))
        entries_vbox = QVBoxLayout()
        entries_vbox.setContentsMargins(5, 0, 0, 0)

        for e in entries:
            # skip if this entry is set to hidden
            if e.hidden:
                continue

            e_layout = e.buildLayout()
            entries_vbox.addLayout(e_layout)

            # Create custom context menu
            e_layout.itemAt(1).widget().setContextMenuPolicy(Qt.CustomContextMenu)
            e_layout.itemAt(1).widget().customContextMenuRequested.connect((lambda id: lambda: self.entryContextMenu(id))(e.id))

        return entries_vbox

    def reload(self):
        Config()
        self.setupDB()
        self.drawGroups()

    def aboutDialog(self):
        QMessageBox.about(self, "About Assignment List",
                          "Created by Louie S. - 2023")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AssignmentList()
    sys.exit(app.exec_())

